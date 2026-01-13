from datasette.app import Datasette
from datasette.permissions import PermissionSQL
from datasette import hookimpl
from datasette_transactions import TransactionState, TransactionManager
import pytest
import threading


# Test plugin that grants all permissions
class AllowAllPlugin:
    __name__ = "allow_all_plugin"

    @hookimpl
    def permission_resources_sql(self, datasette, actor, action):
        # Allow all actions for testing
        return PermissionSQL.allow(reason="test allows all")


@pytest.fixture
def ds():
    """Create a Datasette instance with a test database."""
    return Datasette(memory=True)


@pytest.fixture
def manager():
    """Create a fresh TransactionManager."""
    return TransactionManager()


@pytest.mark.asyncio
async def test_plugin_is_installed(ds):
    response = await ds.client.get("/-/plugins.json")
    assert response.status_code == 200
    installed_plugins = {p["name"] for p in response.json()}
    assert "datasette-transactions" in installed_plugins


# Phase 1: Core Infrastructure Tests

@pytest.mark.asyncio
async def test_begin_route_exists(ds):
    """Test that the begin transaction route is registered."""
    # Should return 405 Method Not Allowed for GET (route exists but wrong method)
    # or 400/403 for POST without proper auth - but not 404
    response = await ds.client.post("/-/transactions/begin/_memory")
    assert response.status_code != 404, "Route should be registered"


def test_transaction_state_creation():
    """Test TransactionState can be created with required fields."""
    import sqlite3
    conn = sqlite3.connect(":memory:")
    state = TransactionState(
        database="test_db",
        connection=conn,
        read_tables={"table1", "table2"},
        write_tables={"table1"},
        timeout_ms=5000,
    )
    assert state.database == "test_db"
    assert state.connection is conn
    assert state.read_tables == {"table1", "table2"}
    assert state.write_tables == {"table1"}
    assert state.timeout_ms == 5000
    assert state.savepoints == set()
    assert state.transaction_id is not None
    conn.close()


def test_transaction_manager_add_and_get(manager):
    """Test adding and retrieving transactions."""
    import sqlite3
    conn = sqlite3.connect(":memory:")
    state = TransactionState(
        database="test_db",
        connection=conn,
        read_tables=set(),
        write_tables=set(),
    )
    manager.add(state)

    retrieved = manager.get(state.transaction_id)
    assert retrieved is state

    # Non-existent transaction returns None
    assert manager.get("nonexistent-uuid") is None
    conn.close()


def test_transaction_manager_remove(manager):
    """Test removing transactions."""
    import sqlite3
    conn = sqlite3.connect(":memory:")
    state = TransactionState(
        database="test_db",
        connection=conn,
        read_tables=set(),
        write_tables=set(),
    )
    manager.add(state)

    removed = manager.remove(state.transaction_id)
    assert removed is state
    assert manager.get(state.transaction_id) is None
    conn.close()


def test_transaction_manager_count_for_database(manager):
    """Test counting transactions per database."""
    import sqlite3

    # Add 3 transactions for db1
    for _ in range(3):
        conn = sqlite3.connect(":memory:")
        state = TransactionState(
            database="db1",
            connection=conn,
            read_tables=set(),
            write_tables=set(),
        )
        manager.add(state)

    # Add 2 transactions for db2
    for _ in range(2):
        conn = sqlite3.connect(":memory:")
        state = TransactionState(
            database="db2",
            connection=conn,
            read_tables=set(),
            write_tables=set(),
        )
        manager.add(state)

    assert manager.count_for_database("db1") == 3
    assert manager.count_for_database("db2") == 2
    assert manager.count_for_database("db3") == 0


# Phase 2: Begin Transaction Tests

@pytest.fixture
def ds_with_table():
    """Create a Datasette instance with a mutable database and table, no default permissions."""
    import sqlite3
    import tempfile
    import os

    # Create a temp db file
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("INSERT INTO test_table (name) VALUES ('alice')")
    conn.commit()
    conn.close()

    # Create datasette with restrictive permissions (no default execute-sql)
    ds = Datasette(
        [path],
        settings={"default_allow_sql": False}
    )
    yield ds

    # Cleanup
    os.unlink(path)


@pytest.mark.asyncio
async def test_begin_transaction_requires_post(ds_with_table):
    """Test that begin endpoint requires POST method."""
    response = await ds_with_table.client.get("/-/transactions/begin/test")
    assert response.status_code == 405


@pytest.mark.asyncio
async def test_begin_transaction_database_not_found(ds_with_table):
    """Test that begin returns 404 for non-existent database."""
    response = await ds_with_table.client.post(
        "/-/transactions/begin/nonexistent",
        json={"read": [], "write": []}
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_begin_transaction_requires_execute_sql_permission(ds_with_table):
    """Test that begin requires execute-sql permission."""
    # Get all database names
    dbs = [db.name for db in ds_with_table.databases.values()]
    # Use the first non-internal database
    db_name = [n for n in dbs if not n.startswith("_")][0]

    # Without any actor, should get 403
    response = await ds_with_table.client.post(
        f"/-/transactions/begin/{db_name}",
        json={"read": ["test_table"], "write": []}
    )
    assert response.status_code == 403


@pytest.fixture
def ds_with_permissions():
    """Create a Datasette instance with full permissions for anonymous users."""
    import sqlite3
    import tempfile
    import os
    from datasette.plugins import pm

    # Create a temp db file
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("CREATE TABLE other_table (id INTEGER PRIMARY KEY, value TEXT)")
    conn.execute("INSERT INTO test_table (name) VALUES ('alice')")
    conn.commit()
    conn.close()

    # Register the allow-all plugin
    allow_all = AllowAllPlugin()
    pm.register(allow_all)

    ds = Datasette([path])
    yield ds, path

    # Cleanup
    pm.unregister(allow_all)
    os.unlink(path)


@pytest.mark.asyncio
async def test_begin_transaction_success(ds_with_permissions):
    """Test successful transaction begin with proper permissions."""
    ds, path = ds_with_permissions

    # Get the database name from the path
    import os
    db_name = os.path.basename(path).replace(".db", "")

    response = await ds.client.post(
        f"/-/transactions/begin/{db_name}",
        json={"read": ["test_table"], "write": []},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert "transaction_id" in data
    assert len(data["transaction_id"]) == 36  # UUID format


@pytest.mark.asyncio
async def test_begin_transaction_max_concurrent(ds_with_permissions):
    """Test that max 5 concurrent transactions per database is enforced."""
    ds, path = ds_with_permissions
    import os
    db_name = os.path.basename(path).replace(".db", "")

    # Create 5 transactions
    transaction_ids = []
    for i in range(5):
        response = await ds.client.post(
            f"/-/transactions/begin/{db_name}",
            json={"read": ["test_table"], "write": []},
        )
        assert response.status_code == 200
        transaction_ids.append(response.json()["transaction_id"])

    # 6th should fail with 429
    response = await ds.client.post(
        f"/-/transactions/begin/{db_name}",
        json={"read": ["test_table"], "write": []},
    )
    assert response.status_code == 429
    assert "Too many concurrent transactions" in response.json()["error"]


# Phase 3: Execute SQL Tests

@pytest.mark.asyncio
async def test_execute_sql_transaction_not_found(ds_with_permissions):
    """Test execute SQL returns 404 for non-existent transaction."""
    ds, path = ds_with_permissions

    response = await ds.client.post(
        "/-/transactions/nonexistent-uuid",
        json={"sql": "SELECT 1"}
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_execute_sql_select(ds_with_permissions):
    """Test executing a SELECT query within a transaction."""
    ds, path = ds_with_permissions
    import os
    db_name = os.path.basename(path).replace(".db", "")

    # Begin transaction with read access
    response = await ds.client.post(
        f"/-/transactions/begin/{db_name}",
        json={"read": ["test_table"], "write": []}
    )
    assert response.status_code == 200
    tx_id = response.json()["transaction_id"]

    # Execute SELECT
    response = await ds.client.post(
        f"/-/transactions/{tx_id}",
        json={"sql": "SELECT * FROM test_table"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert "rows" in data
    assert "columns" in data
    assert len(data["rows"]) == 1
    assert data["rows"][0]["name"] == "alice"


@pytest.mark.asyncio
async def test_execute_sql_with_params(ds_with_permissions):
    """Test executing SQL with named parameters."""
    ds, path = ds_with_permissions
    import os
    db_name = os.path.basename(path).replace(".db", "")

    # Begin transaction with read access
    response = await ds.client.post(
        f"/-/transactions/begin/{db_name}",
        json={"read": ["test_table"], "write": []}
    )
    tx_id = response.json()["transaction_id"]

    # Execute SELECT with params
    response = await ds.client.post(
        f"/-/transactions/{tx_id}",
        json={"sql": "SELECT * FROM test_table WHERE name = :name", "params": {"name": "alice"}}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["rows"]) == 1


@pytest.mark.asyncio
async def test_execute_sql_insert(ds_with_permissions):
    """Test executing an INSERT within a transaction."""
    ds, path = ds_with_permissions
    import os
    db_name = os.path.basename(path).replace(".db", "")

    # Begin transaction with write access
    response = await ds.client.post(
        f"/-/transactions/begin/{db_name}",
        json={"read": ["test_table"], "write": ["test_table"]}
    )
    tx_id = response.json()["transaction_id"]

    # Execute INSERT
    response = await ds.client.post(
        f"/-/transactions/{tx_id}",
        json={"sql": "INSERT INTO test_table (name) VALUES (:name)", "params": {"name": "bob"}}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True

    # Verify the insert within same transaction
    response = await ds.client.post(
        f"/-/transactions/{tx_id}",
        json={"sql": "SELECT * FROM test_table WHERE name = 'bob'"}
    )
    assert response.status_code == 200
    assert len(response.json()["rows"]) == 1


@pytest.mark.asyncio
async def test_execute_sql_unauthorized_table_read(ds_with_permissions):
    """Test that reading from unauthorized table is blocked."""
    ds, path = ds_with_permissions
    import os
    db_name = os.path.basename(path).replace(".db", "")

    # Begin transaction with access only to test_table
    response = await ds.client.post(
        f"/-/transactions/begin/{db_name}",
        json={"read": ["test_table"], "write": []}
    )
    tx_id = response.json()["transaction_id"]

    # Try to read from other_table (not authorized)
    response = await ds.client.post(
        f"/-/transactions/{tx_id}",
        json={"sql": "SELECT * FROM other_table"}
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_execute_sql_unauthorized_table_write(ds_with_permissions):
    """Test that writing to unauthorized table is blocked."""
    ds, path = ds_with_permissions
    import os
    db_name = os.path.basename(path).replace(".db", "")

    # Begin transaction with read-only access
    response = await ds.client.post(
        f"/-/transactions/begin/{db_name}",
        json={"read": ["test_table"], "write": []}
    )
    tx_id = response.json()["transaction_id"]

    # Try to INSERT (not authorized for writes)
    response = await ds.client.post(
        f"/-/transactions/{tx_id}",
        json={"sql": "INSERT INTO test_table (name) VALUES ('hacker')"}
    )
    assert response.status_code == 403


# Phase 4: Savepoint Tests

@pytest.mark.asyncio
async def test_create_savepoint(ds_with_permissions):
    """Test creating a savepoint."""
    ds, path = ds_with_permissions
    import os
    db_name = os.path.basename(path).replace(".db", "")

    # Begin transaction
    response = await ds.client.post(
        f"/-/transactions/begin/{db_name}",
        json={"read": ["test_table"], "write": ["test_table"]}
    )
    tx_id = response.json()["transaction_id"]

    # Create savepoint
    response = await ds.client.post(
        f"/-/transactions/{tx_id}/savepoint",
        json={"name": "sp1"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert data["savepoint"] == "sp1"


@pytest.mark.asyncio
async def test_savepoint_uniqueness(ds_with_permissions):
    """Test that duplicate savepoint names return error."""
    ds, path = ds_with_permissions
    import os
    db_name = os.path.basename(path).replace(".db", "")

    # Begin transaction
    response = await ds.client.post(
        f"/-/transactions/begin/{db_name}",
        json={"read": ["test_table"], "write": []}
    )
    tx_id = response.json()["transaction_id"]

    # Create savepoint
    response = await ds.client.post(
        f"/-/transactions/{tx_id}/savepoint",
        json={"name": "sp1"}
    )
    assert response.status_code == 200

    # Try to create same savepoint again
    response = await ds.client.post(
        f"/-/transactions/{tx_id}/savepoint",
        json={"name": "sp1"}
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["error"]


@pytest.mark.asyncio
async def test_release_savepoint(ds_with_permissions):
    """Test releasing a savepoint."""
    ds, path = ds_with_permissions
    import os
    db_name = os.path.basename(path).replace(".db", "")

    # Begin transaction
    response = await ds.client.post(
        f"/-/transactions/begin/{db_name}",
        json={"read": ["test_table"], "write": []}
    )
    tx_id = response.json()["transaction_id"]

    # Create savepoint
    await ds.client.post(
        f"/-/transactions/{tx_id}/savepoint",
        json={"name": "sp1"}
    )

    # Release savepoint
    response = await ds.client.post(
        f"/-/transactions/{tx_id}/release",
        json={"name": "sp1"}
    )
    assert response.status_code == 200
    assert response.json()["ok"] is True


@pytest.mark.asyncio
async def test_release_nonexistent_savepoint(ds_with_permissions):
    """Test releasing a non-existent savepoint returns error."""
    ds, path = ds_with_permissions
    import os
    db_name = os.path.basename(path).replace(".db", "")

    # Begin transaction
    response = await ds.client.post(
        f"/-/transactions/begin/{db_name}",
        json={"read": ["test_table"], "write": []}
    )
    tx_id = response.json()["transaction_id"]

    # Try to release non-existent savepoint
    response = await ds.client.post(
        f"/-/transactions/{tx_id}/release",
        json={"name": "nonexistent"}
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_rollback_to_savepoint(ds_with_permissions):
    """Test rolling back to a savepoint."""
    ds, path = ds_with_permissions
    import os
    db_name = os.path.basename(path).replace(".db", "")

    # Begin transaction with write access
    response = await ds.client.post(
        f"/-/transactions/begin/{db_name}",
        json={"read": ["test_table"], "write": ["test_table"]}
    )
    tx_id = response.json()["transaction_id"]

    # Create savepoint
    await ds.client.post(
        f"/-/transactions/{tx_id}/savepoint",
        json={"name": "before_insert"}
    )

    # Insert a row
    await ds.client.post(
        f"/-/transactions/{tx_id}",
        json={"sql": "INSERT INTO test_table (name) VALUES ('temp')"}
    )

    # Verify the row exists
    response = await ds.client.post(
        f"/-/transactions/{tx_id}",
        json={"sql": "SELECT COUNT(*) as cnt FROM test_table WHERE name = 'temp'"}
    )
    assert response.json()["rows"][0]["cnt"] == 1

    # Rollback to savepoint
    response = await ds.client.post(
        f"/-/transactions/{tx_id}/rollback-to",
        json={"name": "before_insert"}
    )
    assert response.status_code == 200
    assert response.json()["ok"] is True

    # Verify the row is gone
    response = await ds.client.post(
        f"/-/transactions/{tx_id}",
        json={"sql": "SELECT COUNT(*) as cnt FROM test_table WHERE name = 'temp'"}
    )
    assert response.json()["rows"][0]["cnt"] == 0


# Phase 5: Commit/Rollback Tests

@pytest.mark.asyncio
async def test_commit_transaction(ds_with_permissions):
    """Test committing a transaction persists changes."""
    ds, path = ds_with_permissions
    import os
    import sqlite3
    db_name = os.path.basename(path).replace(".db", "")

    # Begin transaction with write access
    response = await ds.client.post(
        f"/-/transactions/begin/{db_name}",
        json={"read": ["test_table"], "write": ["test_table"]}
    )
    tx_id = response.json()["transaction_id"]

    # Insert a row
    await ds.client.post(
        f"/-/transactions/{tx_id}",
        json={"sql": "INSERT INTO test_table (name) VALUES ('committed')"}
    )

    # Commit
    response = await ds.client.post(f"/-/transactions/commit/{tx_id}")
    assert response.status_code == 200
    assert response.json()["ok"] is True

    # Verify committed outside transaction
    conn = sqlite3.connect(path)
    cursor = conn.execute("SELECT COUNT(*) FROM test_table WHERE name = 'committed'")
    assert cursor.fetchone()[0] == 1
    conn.close()


@pytest.mark.asyncio
async def test_commit_removes_transaction(ds_with_permissions):
    """Test that commit removes the transaction from manager."""
    ds, path = ds_with_permissions
    import os
    db_name = os.path.basename(path).replace(".db", "")

    # Begin transaction
    response = await ds.client.post(
        f"/-/transactions/begin/{db_name}",
        json={"read": ["test_table"], "write": []}
    )
    tx_id = response.json()["transaction_id"]

    # Commit
    await ds.client.post(f"/-/transactions/commit/{tx_id}")

    # Try to use transaction again - should be 404
    response = await ds.client.post(
        f"/-/transactions/{tx_id}",
        json={"sql": "SELECT 1"}
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_commit_transaction_not_found(ds_with_permissions):
    """Test commit on non-existent transaction returns 404."""
    ds, path = ds_with_permissions

    response = await ds.client.post("/-/transactions/commit/nonexistent-uuid")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_rollback_transaction(ds_with_permissions):
    """Test rolling back a transaction discards changes."""
    ds, path = ds_with_permissions
    import os
    import sqlite3
    db_name = os.path.basename(path).replace(".db", "")

    # Begin transaction with write access
    response = await ds.client.post(
        f"/-/transactions/begin/{db_name}",
        json={"read": ["test_table"], "write": ["test_table"]}
    )
    tx_id = response.json()["transaction_id"]

    # Insert a row
    await ds.client.post(
        f"/-/transactions/{tx_id}",
        json={"sql": "INSERT INTO test_table (name) VALUES ('rolled_back')"}
    )

    # Rollback
    response = await ds.client.post(f"/-/transactions/rollback/{tx_id}")
    assert response.status_code == 200
    assert response.json()["ok"] is True

    # Verify NOT committed outside transaction
    conn = sqlite3.connect(path)
    cursor = conn.execute("SELECT COUNT(*) FROM test_table WHERE name = 'rolled_back'")
    assert cursor.fetchone()[0] == 0
    conn.close()


@pytest.mark.asyncio
async def test_rollback_removes_transaction(ds_with_permissions):
    """Test that rollback removes the transaction from manager."""
    ds, path = ds_with_permissions
    import os
    db_name = os.path.basename(path).replace(".db", "")

    # Begin transaction
    response = await ds.client.post(
        f"/-/transactions/begin/{db_name}",
        json={"read": ["test_table"], "write": []}
    )
    tx_id = response.json()["transaction_id"]

    # Rollback
    await ds.client.post(f"/-/transactions/rollback/{tx_id}")

    # Try to use transaction again - should be 404
    response = await ds.client.post(
        f"/-/transactions/{tx_id}",
        json={"sql": "SELECT 1"}
    )
    assert response.status_code == 404


# Phase 6: Timeout Tests

@pytest.mark.asyncio
async def test_transaction_timeout(ds_with_permissions):
    """Test that expired transactions return 410."""
    ds, path = ds_with_permissions
    import os
    import time
    db_name = os.path.basename(path).replace(".db", "")

    # Begin transaction with very short timeout (1ms)
    response = await ds.client.post(
        f"/-/transactions/begin/{db_name}",
        json={"read": ["test_table"], "write": [], "timeout_ms": 1}
    )
    tx_id = response.json()["transaction_id"]

    # Wait for timeout
    time.sleep(0.01)  # 10ms

    # Try to execute SQL - should return 410
    response = await ds.client.post(
        f"/-/transactions/{tx_id}",
        json={"sql": "SELECT 1"}
    )
    assert response.status_code == 410
    assert "expired" in response.json()["error"].lower()


@pytest.mark.asyncio
async def test_transaction_no_timeout(ds_with_permissions):
    """Test that transactions without timeout don't expire."""
    ds, path = ds_with_permissions
    import os
    import time
    db_name = os.path.basename(path).replace(".db", "")

    # Begin transaction without timeout
    response = await ds.client.post(
        f"/-/transactions/begin/{db_name}",
        json={"read": ["test_table"], "write": []}
    )
    tx_id = response.json()["transaction_id"]

    # Wait a bit
    time.sleep(0.01)

    # Should still work
    response = await ds.client.post(
        f"/-/transactions/{tx_id}",
        json={"sql": "SELECT 1"}
    )
    assert response.status_code == 200
