from datasette import hookimpl, Response
from datasette.resources import DatabaseResource, TableResource
from dataclasses import dataclass, field
import json
import sqlite3
import threading
import time
import uuid as uuid_module
from typing import Optional, Set

MAX_TRANSACTIONS_PER_DATABASE = 5


@dataclass
class TransactionState:
    """Holds state for an active transaction."""
    database: str
    connection: object  # sqlite3.Connection
    read_tables: Set[str]
    write_tables: Set[str]
    timeout_ms: Optional[int] = None
    savepoints: Set[str] = field(default_factory=set)
    transaction_id: str = field(default_factory=lambda: str(uuid_module.uuid4()))
    created_at: float = field(default_factory=time.time)
    lock: threading.Lock = field(default_factory=threading.Lock)

    def is_expired(self) -> bool:
        """Check if this transaction has timed out."""
        if self.timeout_ms is None:
            return False
        elapsed_ms = (time.time() - self.created_at) * 1000
        return elapsed_ms > self.timeout_ms


class TransactionManager:
    """Thread-safe storage for active transactions."""

    def __init__(self):
        self._transactions: dict[str, TransactionState] = {}
        self._lock = threading.Lock()

    def add(self, state: TransactionState) -> None:
        """Add a transaction to storage."""
        with self._lock:
            self._transactions[state.transaction_id] = state

    def get(self, transaction_id: str) -> Optional[TransactionState]:
        """Get a transaction by ID, or None if not found."""
        with self._lock:
            return self._transactions.get(transaction_id)

    def remove(self, transaction_id: str) -> Optional[TransactionState]:
        """Remove and return a transaction, or None if not found."""
        with self._lock:
            return self._transactions.pop(transaction_id, None)

    def count_for_database(self, database: str) -> int:
        """Count active transactions for a specific database."""
        with self._lock:
            return sum(1 for t in self._transactions.values() if t.database == database)


# Global transaction manager instance
_manager = TransactionManager()


@hookimpl
def register_routes():
    return [
        (r"^/-/transactions/begin/(?P<database>[^/]+)$", begin_transaction),
        (r"^/-/transactions/(?P<uuid>[^/]+)$", execute_sql),
        (r"^/-/transactions/(?P<uuid>[^/]+)/savepoint$", create_savepoint),
        (r"^/-/transactions/(?P<uuid>[^/]+)/release$", release_savepoint),
        (r"^/-/transactions/(?P<uuid>[^/]+)/rollback-to$", rollback_to_savepoint),
        (r"^/-/transactions/commit/(?P<uuid>[^/]+)$", commit_transaction),
        (r"^/-/transactions/rollback/(?P<uuid>[^/]+)$", rollback_transaction),
    ]


async def begin_transaction(request, datasette):
    """POST /-/transactions/begin/<dbname> - Start a new transaction."""
    if request.method != "POST":
        return Response.text("Method not allowed", status=405)

    database_name = request.url_vars["database"]

    # Check if database exists
    try:
        db = datasette.get_database(database_name)
    except KeyError:
        return Response.json(
            {"ok": False, "error": f"Database not found: {database_name}"},
            status=404
        )

    # Check if database is mutable
    if not db.is_mutable:
        return Response.json(
            {"ok": False, "error": f"Database is immutable: {database_name}"},
            status=400
        )

    # Parse request body
    try:
        body = await request.post_body()
        data = json.loads(body) if body else {}
    except json.JSONDecodeError:
        return Response.json(
            {"ok": False, "error": "Invalid JSON"},
            status=400
        )

    read_tables = set(data.get("read", []))
    write_tables = set(data.get("write", []))
    timeout_ms = data.get("timeout_ms")

    # Check execute-sql permission
    if not await datasette.allowed(
        actor=request.actor, action="execute-sql",
        resource=DatabaseResource(database=database_name)
    ):
        return Response.json(
            {"ok": False, "error": "Permission denied: execute-sql"},
            status=403
        )

    # Check view-table permission for each read table
    for table in read_tables:
        if not await datasette.allowed(
            actor=request.actor, action="view-table",
            resource=TableResource(database=database_name, table=table)
        ):
            return Response.json(
                {"ok": False, "error": f"Permission denied: view-table on {table}"},
                status=403
            )

    # Check insert-row and update-row permissions for each write table
    for table in write_tables:
        if not await datasette.allowed(
            actor=request.actor, action="insert-row",
            resource=TableResource(database=database_name, table=table)
        ):
            return Response.json(
                {"ok": False, "error": f"Permission denied: insert-row on {table}"},
                status=403
            )
        if not await datasette.allowed(
            actor=request.actor, action="update-row",
            resource=TableResource(database=database_name, table=table)
        ):
            return Response.json(
                {"ok": False, "error": f"Permission denied: update-row on {table}"},
                status=403
            )

    # Check concurrency limit
    if _manager.count_for_database(database_name) >= MAX_TRANSACTIONS_PER_DATABASE:
        return Response.json(
            {"ok": False, "error": "Too many concurrent transactions"},
            status=429
        )

    # Create connection and set up authorizer
    # Use DEFERRED for read-only, IMMEDIATE for write transactions
    isolation_level = "IMMEDIATE" if write_tables else "DEFERRED"
    conn = sqlite3.connect(db.path, isolation_level=None, check_same_thread=False)
    conn.row_factory = sqlite3.Row

    # Create authorizer callback
    def authorizer(action, arg1, arg2, db_name, trigger_name):
        # SQLite action codes
        SQLITE_READ = 20
        SQLITE_INSERT = 18
        SQLITE_UPDATE = 23
        SQLITE_DELETE = 9
        SQLITE_ATTACH = 24

        if action == SQLITE_ATTACH:
            return sqlite3.SQLITE_DENY

        if action == SQLITE_READ:
            # arg1 is table name, arg2 is column name
            if arg1 and arg1 not in read_tables and arg1 not in write_tables:
                # Allow reading sqlite_ internal tables
                if not arg1.startswith("sqlite_"):
                    return sqlite3.SQLITE_DENY

        if action in (SQLITE_INSERT, SQLITE_UPDATE, SQLITE_DELETE):
            # arg1 is table name
            if arg1 and arg1 not in write_tables:
                return sqlite3.SQLITE_DENY

        return sqlite3.SQLITE_OK

    conn.set_authorizer(authorizer)

    # Begin transaction with appropriate isolation level
    conn.execute(f"BEGIN {isolation_level}")

    # Create and store transaction state
    state = TransactionState(
        database=database_name,
        connection=conn,
        read_tables=read_tables,
        write_tables=write_tables,
        timeout_ms=timeout_ms,
    )
    _manager.add(state)

    return Response.json({
        "ok": True,
        "transaction_id": state.transaction_id
    })


async def execute_sql(request, datasette):
    """POST /-/transactions/<uuid> - Execute SQL within transaction."""
    if request.method != "POST":
        return Response.text("Method not allowed", status=405)

    transaction_id = request.url_vars["uuid"]
    state = _manager.get(transaction_id)

    if state is None:
        return Response.json(
            {"ok": False, "error": "Transaction not found"},
            status=404
        )

    # Check if transaction has expired
    if state.is_expired():
        # Rollback and remove the transaction
        try:
            state.connection.rollback()
            state.connection.close()
        except Exception:
            pass
        _manager.remove(transaction_id)
        return Response.json(
            {"ok": False, "error": "Transaction expired"},
            status=410
        )

    # Parse request body
    try:
        body = await request.post_body()
        data = json.loads(body) if body else {}
    except json.JSONDecodeError:
        return Response.json(
            {"ok": False, "error": "Invalid JSON"},
            status=400
        )

    sql = data.get("sql")
    if not sql:
        return Response.json(
            {"ok": False, "error": "Missing 'sql' parameter"},
            status=400
        )

    params = data.get("params", {})

    # Execute SQL within the transaction
    try:
        with state.lock:
            cursor = state.connection.execute(sql, params)
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description] if cursor.description else []

            # Convert rows to list of dicts
            rows_as_dicts = [dict(row) for row in rows]

            return Response.json({
                "ok": True,
                "rows": rows_as_dicts,
                "columns": columns,
                "truncated": False
            })
    except sqlite3.DatabaseError as e:
        error_msg = str(e)
        # Check if this is an authorization error
        if "not authorized" in error_msg.lower() or "prohibited" in error_msg.lower():
            return Response.json(
                {"ok": False, "error": f"Access denied: {error_msg}"},
                status=403
            )
        return Response.json(
            {"ok": False, "error": f"SQL error: {error_msg}"},
            status=400
        )


async def create_savepoint(request, datasette):
    """POST /-/transactions/<uuid>/savepoint - Create a savepoint."""
    if request.method != "POST":
        return Response.text("Method not allowed", status=405)

    transaction_id = request.url_vars["uuid"]
    state = _manager.get(transaction_id)

    if state is None:
        return Response.json(
            {"ok": False, "error": "Transaction not found"},
            status=404
        )

    if state.is_expired():
        try:
            state.connection.rollback()
            state.connection.close()
        except Exception:
            pass
        _manager.remove(transaction_id)
        return Response.json(
            {"ok": False, "error": "Transaction expired"},
            status=410
        )

    # Parse request body
    try:
        body = await request.post_body()
        data = json.loads(body) if body else {}
    except json.JSONDecodeError:
        return Response.json(
            {"ok": False, "error": "Invalid JSON"},
            status=400
        )

    name = data.get("name")
    if not name:
        return Response.json(
            {"ok": False, "error": "Missing 'name' parameter"},
            status=400
        )

    # Check for duplicate savepoint name
    if name in state.savepoints:
        return Response.json(
            {"ok": False, "error": f"Savepoint '{name}' already exists"},
            status=400
        )

    # Create savepoint
    try:
        with state.lock:
            state.connection.execute(f"SAVEPOINT [{name}]")
            state.savepoints.add(name)
    except sqlite3.DatabaseError as e:
        return Response.json(
            {"ok": False, "error": f"SQL error: {e}"},
            status=400
        )

    return Response.json({
        "ok": True,
        "savepoint": name
    })


async def release_savepoint(request, datasette):
    """POST /-/transactions/<uuid>/release - Release a savepoint."""
    if request.method != "POST":
        return Response.text("Method not allowed", status=405)

    transaction_id = request.url_vars["uuid"]
    state = _manager.get(transaction_id)

    if state is None:
        return Response.json(
            {"ok": False, "error": "Transaction not found"},
            status=404
        )

    if state.is_expired():
        try:
            state.connection.rollback()
            state.connection.close()
        except Exception:
            pass
        _manager.remove(transaction_id)
        return Response.json(
            {"ok": False, "error": "Transaction expired"},
            status=410
        )

    # Parse request body
    try:
        body = await request.post_body()
        data = json.loads(body) if body else {}
    except json.JSONDecodeError:
        return Response.json(
            {"ok": False, "error": "Invalid JSON"},
            status=400
        )

    name = data.get("name")
    if not name:
        return Response.json(
            {"ok": False, "error": "Missing 'name' parameter"},
            status=400
        )

    # Check savepoint exists
    if name not in state.savepoints:
        return Response.json(
            {"ok": False, "error": f"Savepoint '{name}' not found"},
            status=404
        )

    # Release savepoint
    try:
        with state.lock:
            state.connection.execute(f"RELEASE SAVEPOINT [{name}]")
            state.savepoints.discard(name)
    except sqlite3.DatabaseError as e:
        return Response.json(
            {"ok": False, "error": f"SQL error: {e}"},
            status=400
        )

    return Response.json({"ok": True})


async def rollback_to_savepoint(request, datasette):
    """POST /-/transactions/<uuid>/rollback-to - Rollback to savepoint."""
    if request.method != "POST":
        return Response.text("Method not allowed", status=405)

    transaction_id = request.url_vars["uuid"]
    state = _manager.get(transaction_id)

    if state is None:
        return Response.json(
            {"ok": False, "error": "Transaction not found"},
            status=404
        )

    if state.is_expired():
        try:
            state.connection.rollback()
            state.connection.close()
        except Exception:
            pass
        _manager.remove(transaction_id)
        return Response.json(
            {"ok": False, "error": "Transaction expired"},
            status=410
        )

    # Parse request body
    try:
        body = await request.post_body()
        data = json.loads(body) if body else {}
    except json.JSONDecodeError:
        return Response.json(
            {"ok": False, "error": "Invalid JSON"},
            status=400
        )

    name = data.get("name")
    if not name:
        return Response.json(
            {"ok": False, "error": "Missing 'name' parameter"},
            status=400
        )

    # Check savepoint exists
    if name not in state.savepoints:
        return Response.json(
            {"ok": False, "error": f"Savepoint '{name}' not found"},
            status=404
        )

    # Rollback to savepoint
    try:
        with state.lock:
            state.connection.execute(f"ROLLBACK TO SAVEPOINT [{name}]")
    except sqlite3.DatabaseError as e:
        return Response.json(
            {"ok": False, "error": f"SQL error: {e}"},
            status=400
        )

    return Response.json({"ok": True})


async def commit_transaction(request, datasette):
    """POST /-/transactions/commit/<uuid> - Commit transaction."""
    if request.method != "POST":
        return Response.text("Method not allowed", status=405)

    transaction_id = request.url_vars["uuid"]
    state = _manager.get(transaction_id)

    if state is None:
        return Response.json(
            {"ok": False, "error": "Transaction not found"},
            status=404
        )

    if state.is_expired():
        try:
            state.connection.rollback()
            state.connection.close()
        except Exception:
            pass
        _manager.remove(transaction_id)
        return Response.json(
            {"ok": False, "error": "Transaction expired"},
            status=410
        )

    # Commit and close
    try:
        with state.lock:
            state.connection.commit()
            state.connection.close()
    except sqlite3.DatabaseError as e:
        return Response.json(
            {"ok": False, "error": f"Commit failed: {e}"},
            status=400
        )

    _manager.remove(transaction_id)
    return Response.json({"ok": True})


async def rollback_transaction(request, datasette):
    """POST /-/transactions/rollback/<uuid> - Rollback transaction."""
    if request.method != "POST":
        return Response.text("Method not allowed", status=405)

    transaction_id = request.url_vars["uuid"]
    state = _manager.get(transaction_id)

    if state is None:
        return Response.json(
            {"ok": False, "error": "Transaction not found"},
            status=404
        )

    if state.is_expired():
        try:
            state.connection.rollback()
            state.connection.close()
        except Exception:
            pass
        _manager.remove(transaction_id)
        return Response.json(
            {"ok": False, "error": "Transaction already rolled back (expired)"},
            status=410
        )

    # Rollback and close
    try:
        with state.lock:
            state.connection.rollback()
            state.connection.close()
    except sqlite3.DatabaseError as e:
        return Response.json(
            {"ok": False, "error": f"Rollback failed: {e}"},
            status=400
        )

    _manager.remove(transaction_id)
    return Response.json({"ok": True})
