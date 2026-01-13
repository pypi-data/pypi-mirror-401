from __future__ import annotations

import io
import json
import math
import re
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple, List

import pandas as pd
import sqlalchemy as sa

from AnyQt.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from AnyQt import QtWidgets, QtCore

from orangewidget import gui
from orangewidget.settings import Setting
from Orange.widgets.widget import OWWidget, Input, Output, Msg
from Orange.data import Table


# -----------------------------
# Helpers
# -----------------------------

def unwrap_engine(conn_input: Any) -> sa.Engine:
    if conn_input is None:
        raise ValueError("DB Connection kosong.")
    if isinstance(conn_input, sa.Engine):
        return conn_input
    if isinstance(conn_input, dict) and isinstance(conn_input.get("engine"), sa.Engine):
        return conn_input["engine"]
    raise TypeError("Format DB Connection tidak dikenali (harus SQLAlchemy Engine atau dict berisi 'engine').")


def dialect_name(engine: sa.Engine) -> str:
    try:
        return (engine.dialect.name or "").lower()
    except Exception:
        return ""


def default_schema_for_engine(engine: sa.Engine) -> Optional[str]:
    return "dbo" if "mssql" in dialect_name(engine) else None


def target_fullname(schema: Optional[str], table: str) -> str:
    t = (table or "").strip()
    s = (schema or "").strip()
    return f"{s}.{t}" if s else t


def sanitize_columns(cols: List[str]) -> List[str]:
    seen: Dict[str, int] = {}
    out: List[str] = []
    for c in cols:
        c0 = (c or "").strip().lower()
        c0 = re.sub(r"[^a-z0-9_]+", "_", c0)
        c0 = re.sub(r"_+", "_", c0).strip("_")
        if not c0:
            c0 = "col"
        if c0[0].isdigit():
            c0 = f"col_{c0}"

        base = c0
        k = seen.get(base, 0) + 1
        seen[base] = k
        if k > 1:
            c0 = f"{base}_{k}"
        out.append(c0)
    return out


def orange_table_to_df(data: Table) -> pd.DataFrame:
    # kompatibel lintas versi Orange
    if hasattr(data, "to_pandas_df"):
        return data.to_pandas_df()
    if hasattr(data, "to_pandas"):
        return data.to_pandas()
    from Orange.data.pandas_compat import table_to_frame
    return table_to_frame(data)


def normalize_df_for_db(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [str(c) for c in out.columns]

    # memastikan kolom unique
    if len(set(out.columns)) != len(out.columns):
        out.columns = sanitize_columns(out.columns)

    # timezone-aware datetime -> naive
    for c in out.columns:
        if pd.api.types.is_datetime64_any_dtype(out[c]):
            try:
                # drop tz if any
                if getattr(out[c].dt, "tz", None) is not None:
                    out[c] = out[c].dt.tz_convert(None)
            except Exception:
                pass

    def _is_na(v: Any) -> bool:
        try:
            return pd.isna(v)
        except Exception:
            return False

    for c in out.columns:
        if out[c].dtype == "object":
            def _norm(v: Any) -> Any:
                if v is None or _is_na(v):
                    return None
                if isinstance(v, (dict, list, tuple, set)):
                    try:
                        return json.dumps(v, ensure_ascii=False)
                    except Exception:
                        return str(v)
                return v
            out[c] = out[c].map(_norm)

    return out


def parse_type(type_str: str) -> sa.types.TypeEngine:
    t = type_str.strip().upper()

    if t in ("TEXT",):
        return sa.Text()
    if t in ("DATE",):
        return sa.Date()
    if t in ("DATETIME", "TIMESTAMP"):
        return sa.DateTime()
    if t in ("BOOLEAN", "BOOL"):
        return sa.Boolean()
    if t in ("INT", "INTEGER"):
        return sa.Integer()
    if t in ("BIGINT",):
        return sa.BigInteger()
    if t in ("FLOAT", "DOUBLE"):
        return sa.Float()

    m = re.match(r"^VARCHAR\((\d+)\)$", t)
    if m:
        return sa.String(int(m.group(1)))

    m = re.match(r"^NUMERIC\((\d+),(\d+)\)$", t)
    if m:
        return sa.Numeric(int(m.group(1)), int(m.group(2)))

    m = re.match(r"^DECIMAL\((\d+),(\d+)\)$", t)
    if m:
        return sa.Numeric(int(m.group(1)), int(m.group(2)))

    return sa.Text()


def default_sqlalchemy_dtype_map(df: pd.DataFrame) -> Dict[str, sa.types.TypeEngine]:
    m: Dict[str, sa.types.TypeEngine] = {}
    for col in df.columns:
        s = df[col]
        if pd.api.types.is_integer_dtype(s):
            m[col] = sa.BigInteger()
        elif pd.api.types.is_float_dtype(s):
            m[col] = sa.Float()
        elif pd.api.types.is_bool_dtype(s):
            m[col] = sa.Boolean()
        elif pd.api.types.is_datetime64_any_dtype(s):
            m[col] = sa.DateTime()
        else:
            try:
                max_len = int(s.astype(str).map(len).max())
            except Exception:
                max_len = 0
            if 1 <= max_len <= 255:
                m[col] = sa.String(length=max_len)
            else:
                m[col] = sa.Text()
    return m


def merge_dtype_overrides(
    base: Dict[str, sa.types.TypeEngine],
    overrides_json: str
) -> Tuple[Dict[str, sa.types.TypeEngine], Dict[str, str]]:
    overrides_json = (overrides_json or "").strip()
    if not overrides_json:
        return base, {}

    try:
        obj = json.loads(overrides_json)
        if not isinstance(obj, dict):
            raise ValueError("Override JSON harus object/dict.")
    except Exception as e:
        raise ValueError(
            f"Override JSON tidak valid: {e}. "
            r'Contoh benar: {"nilai_kontrak":"NUMERIC(18,2)","tgl_sp2d":"DATE"}'
        )

    merged = dict(base)
    readable: Dict[str, str] = {}
    for k, v in obj.items():
        if isinstance(k, str) and isinstance(v, str):
            kk = k.strip()
            vv = v.strip()
            if kk:
                merged[kk] = parse_type(vv)
                readable[kk] = vv
    return merged, readable


def pythonize_records(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Convert dataframe chunk -> list[dict] with Python-native scalars.
    This helps pyodbc avoid weird parameter issues.
    """
    # replace NaN/NaT with None
    cdf = df.where(pd.notna(df), None)

    # convert numpy scalars -> python scalars
    records: List[Dict[str, Any]] = []
    for row in cdf.to_dict(orient="records"):
        r2 = {}
        for k, v in row.items():
            if hasattr(v, "item"):  # numpy scalar
                try:
                    v = v.item()
                except Exception:
                    pass
            r2[k] = v
        records.append(r2)
    return records


# -----------------------------
# Insert Strategies
# -----------------------------

class InsertStrategy:
    def insert(
        self,
        df: pd.DataFrame,
        engine: sa.Engine,
        table: str,
        schema: Optional[str],
        if_exists: str,
        chunksize: int,
        dtype_map: Dict[str, sa.types.TypeEngine],
        index: bool,
        status_cb,
        progress_cb,
        cancel_cb,
    ) -> int:
        raise NotImplementedError


class MSSQLCoreStrategy(InsertStrategy):
    """
    SQL Server stable path:
    - (replace/fail/append) handled explicitly
    - create table with SQLAlchemy Table + dtype_map
    - insert executemany via conn.execute(table.insert(), records)
    """
    def _enable_fast_executemany(self, engine: sa.Engine) -> None:
        try:
            from sqlalchemy import event

            @event.listens_for(engine, "before_cursor_execute")
            def _fast_exec(conn, cursor, statement, parameters, context, executemany):
                if executemany:
                    try:
                        cursor.fast_executemany = True
                    except Exception:
                        pass
        except Exception:
            pass

    def _build_table(self, metadata: sa.MetaData, table: str, schema: Optional[str], dtype_map: Dict[str, sa.types.TypeEngine]) -> sa.Table:
        cols = []
        for name, tp in dtype_map.items():
            cols.append(sa.Column(name, tp))
        return sa.Table(table, metadata, *cols, schema=schema)

    def insert(self, df, engine, table, schema, if_exists, chunksize, dtype_map, index,
               status_cb, progress_cb, cancel_cb) -> int:
        self._enable_fast_executemany(engine)

        total = len(df)
        if total == 0:
            return 0

        chunk = max(1, int(chunksize))
        n = (total + chunk - 1) // chunk
        inserted = 0

        meta = sa.MetaData()
        insp = sa.inspect(engine)

        has_tbl = insp.has_table(table_name=table, schema=schema)

        # handle if_exists
        if if_exists == "fail" and has_tbl:
            raise ValueError(f"Tabel {target_fullname(schema, table)} sudah ada (if_exists=fail).")

        with engine.begin() as conn:
            if if_exists == "replace" and has_tbl:
                status_cb(f"Dropping table {target_fullname(schema, table)}…")
                t = sa.Table(table, meta, schema=schema)
                t.drop(conn, checkfirst=True)
                has_tbl = False

            if not has_tbl:
                status_cb(f"Creating table {target_fullname(schema, table)}…")
                meta2 = sa.MetaData()
                tcreate = self._build_table(meta2, table, schema, dtype_map)
                tcreate.create(conn, checkfirst=False)

        # reflect for insert (so names match db)
        meta3 = sa.MetaData()
        t_ins = sa.Table(table, meta3, schema=schema, autoload_with=engine)

        for i in range(n):
            if cancel_cb():
                break
            start = i * chunk
            end = min((i + 1) * chunk, total)
            cdf = df.iloc[start:end]

            status_cb(f"MSSQL bulk insert chunk {i+1}/{n} rows {start+1}-{end}")
            records = pythonize_records(cdf)

            with engine.begin() as conn:
                conn.execute(t_ins.insert(), records)

            inserted += len(records)
            pct = int((inserted / total) * 100)
            progress_cb(min(100, max(0, pct)))

        return inserted


class GenericToSQLStrategy(InsertStrategy):
    """
    Fallback to pandas.to_sql for non-MSSQL (or dialects where core strategy isn't needed).
    """
    def insert(self, df, engine, table, schema, if_exists, chunksize, dtype_map, index,
               status_cb, progress_cb, cancel_cb) -> int:
        total = len(df)
        if total == 0:
            return 0

        chunk = max(1, int(chunksize))
        n = (total + chunk - 1) // chunk
        inserted = 0

        for i in range(n):
            if cancel_cb():
                break
            start = i * chunk
            end = min((i + 1) * chunk, total)
            df_chunk = df.iloc[start:end]

            chunk_if_exists = if_exists
            if if_exists == "replace":
                chunk_if_exists = "replace" if i == 0 else "append"

            status_cb(f"Insert chunk {i+1}/{n} rows {start+1}-{end}")

            with engine.begin() as conn:
                df_chunk.to_sql(
                    name=table,
                    con=conn,
                    schema=schema,
                    if_exists=chunk_if_exists,
                    index=index,
                    method="multi",
                    dtype=dtype_map,
                    chunksize=None,
                )

            inserted += len(df_chunk)
            pct = int((inserted / total) * 100)
            progress_cb(min(100, max(0, pct)))

        return inserted


class PostgresCopyStrategy(InsertStrategy):
    """
    Try COPY for append; fallback generic if unsupported.
    """
    def insert(self, df, engine, table, schema, if_exists, chunksize, dtype_map, index,
               status_cb, progress_cb, cancel_cb) -> int:
        if if_exists in ("replace", "fail"):
            return GenericToSQLStrategy().insert(df, engine, table, schema, if_exists, chunksize, dtype_map, index,
                                                status_cb, progress_cb, cancel_cb)

        total = len(df)
        if total == 0:
            return 0

        chunk = max(1, int(chunksize))
        n = (total + chunk - 1) // chunk

        # ensure table exists
        with engine.begin() as conn:
            df.head(0).to_sql(table, conn, schema=schema, if_exists="append", index=index, dtype=dtype_map)

        inserted = 0
        raw = engine.raw_connection()
        try:
            cur = raw.cursor()
            full = f"{schema}.{table}" if schema else table
            cols = list(df.columns)
            col_list = ", ".join([f'"{c}"' for c in cols])

            for i in range(n):
                if cancel_cb():
                    break

                start = i * chunk
                end = min((i + 1) * chunk, total)
                cdf = df.iloc[start:end]

                status_cb(f"COPY chunk {i+1}/{n} rows {start+1}-{end}")

                buf = io.StringIO()
                cdf.to_csv(buf, index=False, header=False, sep="\t", na_rep="\\N")
                buf.seek(0)

                sql = f'COPY {full} ({col_list}) FROM STDIN WITH (FORMAT csv, DELIMITER E\'\\t\', NULL \'\\N\')'
                cur.copy_expert(sql, buf)  # psycopg2
                raw.commit()

                inserted += len(cdf)
                pct = int((inserted / total) * 100)
                progress_cb(min(100, max(0, pct)))

        finally:
            try:
                raw.close()
            except Exception:
                pass

        return inserted


def pick_strategy(engine: sa.Engine) -> InsertStrategy:
    d = dialect_name(engine)
    if "mssql" in d:
        return MSSQLCoreStrategy()
    if d in ("postgresql", "postgres"):
        return PostgresCopyStrategy()
    return GenericToSQLStrategy()


# -----------------------------
# Worker
# -----------------------------

@dataclass
class RestoreJobConfig:
    table_name: str
    schema: Optional[str]
    if_exists: str
    chunk_size: int
    sanitize_cols: bool
    dtype_overrides_json: str
    write_index: bool


class RestoreWorker(QObject):
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(dict)
    failed = pyqtSignal(str)

    def __init__(self, data: Table, conn_input: Any, cfg: RestoreJobConfig):
        super().__init__()
        self.data = data
        self.conn_input = conn_input
        self.cfg = cfg
        self._cancel = False

    def cancel(self):
        self._cancel = True

    def _cancelled(self) -> bool:
        return self._cancel

    @pyqtSlot()
    def run(self):
        t0 = time.time()
        try:
            engine = unwrap_engine(self.conn_input)
            dname = dialect_name(engine)

            if not self.cfg.table_name.strip():
                raise ValueError("Nama table tujuan belum diisi.")

            schema = self.cfg.schema or default_schema_for_engine(engine)

            self.status.emit("Menyiapkan data…")
            df = orange_table_to_df(self.data)

            # sanitize
            original_cols = [str(c) for c in df.columns]
            col_map: Dict[str, str] = {}
            if self.cfg.sanitize_cols:
                new_cols = sanitize_columns([str(c) for c in df.columns])
                col_map = dict(zip(original_cols, new_cols))
                df.columns = new_cols
            else:
                df.columns = [str(c) for c in df.columns]

            # normalize
            df = normalize_df_for_db(df)

            # dtype mapping
            base_dtype = default_sqlalchemy_dtype_map(df)
            dtype_map, overrides_readable = merge_dtype_overrides(base_dtype, self.cfg.dtype_overrides_json)

            total_rows = int(len(df))
            if total_rows == 0:
                raise ValueError("Data kosong (0 baris).")

            self.progress.emit(0)
            self.status.emit(
                f"Mulai restore ke {target_fullname(schema, self.cfg.table_name)} "
                f"(dialect={dname}, cols={len(df.columns)}, rows={total_rows})…"
            )

            strategy = pick_strategy(engine)

            inserted = 0
            try:
                inserted = strategy.insert(
                    df=df,
                    engine=engine,
                    table=self.cfg.table_name.strip(),
                    schema=(schema.strip() if schema else None),
                    if_exists=self.cfg.if_exists,
                    chunksize=int(self.cfg.chunk_size),
                    dtype_map=dtype_map,
                    index=bool(self.cfg.write_index),
                    status_cb=self.status.emit,
                    progress_cb=self.progress.emit,
                    cancel_cb=self._cancelled,
                )
            except Exception as e:
                # fallback if Postgres COPY fails
                if isinstance(strategy, PostgresCopyStrategy):
                    self.status.emit(f"COPY gagal ({e}), fallback to generic…")
                    inserted = GenericToSQLStrategy().insert(
                        df=df,
                        engine=engine,
                        table=self.cfg.table_name.strip(),
                        schema=(schema.strip() if schema else None),
                        if_exists=self.cfg.if_exists,
                        chunksize=int(self.cfg.chunk_size),
                        dtype_map=dtype_map,
                        index=bool(self.cfg.write_index),
                        status_cb=self.status.emit,
                        progress_cb=self.progress.emit,
                        cancel_cb=self._cancelled,
                    )
                else:
                    raise

            if self._cancelled():
                self.status.emit("Dibatalkan oleh user.")
                ok = False
                cancelled = True
            else:
                self.progress.emit(100)
                self.status.emit("Selesai.")
                ok = True
                cancelled = False

            t1 = time.time()
            dur = max(0.0001, t1 - t0)
            rps = inserted / dur

            report = {
                "ok": ok,
                "cancelled": cancelled,
                "dialect": dname,
                "target": target_fullname(schema, self.cfg.table_name),
                "inserted_rows": int(inserted),
                "total_rows": int(total_rows),
                "chunk_size": int(self.cfg.chunk_size),
                "if_exists": self.cfg.if_exists,
                "sanitize_cols": bool(self.cfg.sanitize_cols),
                "column_rename_map": col_map,
                "dtype_overrides": overrides_readable,
                "duration_sec": float(dur),
                "rows_per_sec": float(rps),
                "columns": list(df.columns),
            }
            self.finished.emit(report)

        except Exception as e:
            self.failed.emit(f"{type(e).__name__}: {e}")


# -----------------------------
# Widget
# -----------------------------

class OWDBRestore(OWWidget):
    name = "Restore to Database"
    id = "datahelpers-restore-to-db"
    description = "Restore/Load data dari Table ke DB Connection (batch + progress)."
    icon = "icons/restore.png"
    priority = 1200
    want_main_area = False

    class Inputs:
        data = Input("Data", Table)
        connection = Input("Connection", object, auto_summary=False)

    class Outputs:
        report = Output("Report", dict, auto_summary=False)

    class Error(OWWidget.Error):
        missing_inputs = Msg("Butuh input Data dan Connection.")
        restore_failed = Msg("Restore gagal: {}")
        bad_dtype_override = Msg("{}")

    class Warning(OWWidget.Warning):
        cancelled = Msg("Restore dibatalkan.")

    table_name: str = Setting("")
    schema: str = Setting("")  # MSSQL default dbo if empty
    if_exists: int = Setting(1)  # 0 fail, 1 append, 2 replace
    chunk_size: int = Setting(5000)  # default
    sanitize_cols: bool = Setting(True)
    write_index: bool = Setting(False)
    dtype_override_json: str = Setting("")

    def __init__(self):
        super().__init__()
        self.data: Optional[Table] = None
        self.conn_input: Any = None

        self._thread: Optional[QThread] = None
        self._worker: Optional[RestoreWorker] = None

        box = gui.widgetBox(self.controlArea, "Target", spacing=8)
        gui.lineEdit(box, self, "table_name", label="Table name:")
        gui.lineEdit(box, self, "schema", label="Schema (kosong = auto dbo untuk MSSQL):")

        box2 = gui.widgetBox(self.controlArea, "Options", spacing=8)
        gui.comboBox(
            box2, self, "if_exists",
            label="If exists:",
            items=["fail", "append", "replace"],
            orientation=QtCore.Qt.Horizontal
        )
        gui.spin(box2, self, "chunk_size", minv=100, maxv=500_000, step=1000, label="Chunk size:")
        gui.checkBox(box2, self, "sanitize_cols", "Sanitasi nama kolom (recommended)")
        gui.checkBox(box2, self, "write_index", "Tulis index DataFrame")

        box3 = gui.widgetBox(self.controlArea, "Type mapping (opsional)", spacing=6)
        gui.label(box3, self,
                  'Override JSON (contoh: {"nilai_kontrak":"NUMERIC(18,2)","tgl_sp2d":"DATE"})')
        self._dtype_editor = QtWidgets.QPlainTextEdit()
        self._dtype_editor.setPlaceholderText('{"nilai_kontrak":"NUMERIC(18,2)","tgl_sp2d":"DATE"}')
        self._dtype_editor.setPlainText(self.dtype_override_json or "")
        self._dtype_editor.textChanged.connect(self._on_dtype_changed)
        box3.layout().addWidget(self._dtype_editor)

        box4 = gui.widgetBox(self.controlArea, "Run", spacing=8)
        self.btn_start = gui.button(box4, self, "Start Restore", callback=self.start_restore)
        self.btn_cancel = gui.button(box4, self, "Cancel", callback=self.cancel_restore)
        self.btn_cancel.setEnabled(False)

        self.lbl_status = gui.label(box4, self, "Status: -")

        self.progressBarInit()
        self.progressBarSet(0)

    def _on_dtype_changed(self):
        self.dtype_override_json = self._dtype_editor.toPlainText()

    @Inputs.data
    def set_data(self, data: Optional[Table]) -> None:
        self.data = data

    @Inputs.connection
    def set_connection(self, conn: Any) -> None:
        self.conn_input = conn
        try:
            engine = unwrap_engine(conn) if conn is not None else None
            if engine is not None and not (self.schema or "").strip():
                if "mssql" in dialect_name(engine):
                    self.schema = "dbo"
        except Exception:
            pass

    def _cfg(self) -> RestoreJobConfig:
        if_exists_str = ["fail", "append", "replace"][int(self.if_exists)]
        schema = (self.schema or "").strip() or None
        return RestoreJobConfig(
            table_name=(self.table_name or "").strip(),
            schema=schema,
            if_exists=if_exists_str,
            chunk_size=int(self.chunk_size),
            sanitize_cols=bool(self.sanitize_cols),
            dtype_overrides_json=(self.dtype_override_json or "").strip(),
            write_index=bool(self.write_index),
        )

    def start_restore(self):
        self.Error.clear()
        self.Warning.clear()

        if self.data is None or self.conn_input is None:
            self.Error.missing_inputs()
            return

        try:
            _ = merge_dtype_overrides({}, (self.dtype_override_json or "").strip())
        except Exception as e:
            self.Error.bad_dtype_override(str(e))
            return

        if self._thread is not None:
            return

        cfg = self._cfg()
        if not cfg.table_name:
            self.Error.restore_failed("Nama table tujuan belum diisi.")
            return

        self.progressBarSet(0)
        self.lbl_status.setText("Status: Menjalankan…")

        self._thread = QThread(self)
        self._worker = RestoreWorker(self.data, self.conn_input, cfg)
        self._worker.moveToThread(self._thread)

        self._thread.started.connect(self._worker.run)
        self._worker.status.connect(self._on_status)
        self._worker.progress.connect(self._on_progress)
        self._worker.finished.connect(self._on_finished)
        self._worker.failed.connect(self._on_failed)

        self._worker.finished.connect(self._thread.quit)
        self._worker.failed.connect(self._thread.quit)
        self._thread.finished.connect(self._cleanup)

        self.btn_start.setEnabled(False)
        self.btn_cancel.setEnabled(True)
        self._thread.start()

    def cancel_restore(self):
        if self._worker:
            self._worker.cancel()
            self.lbl_status.setText("Status: Membatalkan…")

    def _cleanup(self):
        self.btn_start.setEnabled(True)
        self.btn_cancel.setEnabled(False)
        if self._worker:
            self._worker.deleteLater()
        self._worker = None
        if self._thread:
            self._thread.deleteLater()
        self._thread = None

    def _on_progress(self, pct: int):
        self.progressBarSet(int(pct))

    def _on_status(self, text: str):
        self.lbl_status.setText(f"Status: {text}")

    def _on_finished(self, report: dict):
        if report.get("cancelled"):
            self.Warning.cancelled()
        self.Outputs.report.send(report)

    def _on_failed(self, msg: str):
        self.Error.restore_failed(msg)
        self.lbl_status.setText("Status: Gagal.")
        self.Outputs.report.send({"ok": False, "error": msg})
