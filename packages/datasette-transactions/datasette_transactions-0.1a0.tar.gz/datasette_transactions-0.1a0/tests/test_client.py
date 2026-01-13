"""Tests for the Python client library.

The sync and async clients share the same API structure.
Integration tests use the async client with Datasette's built-in test client.
"""
import pytest
from datasette.app import Datasette
from datasette.permissions import PermissionSQL
from datasette import hookimpl
from datasette.plugins import pm

from datasette_transactions.client import (
    TransactionsClient,
    AsyncTransactionsClient,
    Transaction,
    AsyncTransaction,
    TransactionError,
    TransactionNotFoundError,
    TransactionExpiredError,
    PermissionDeniedError,
    TooManyTransactionsError,
    DatabaseNotFoundError,
    DatabaseImmutableError,
    SQLError,
    SavepointExistsError,
    SavepointNotFoundError,
    ExecuteResult,
)


class AllowAllPlugin:
    """Plugin that allows all permissions for testing."""
    __name__ = "AllowAllClientTestPlugin"

    @hookimpl
    def permission_resources_sql(self, datasette, actor, action):
        return PermissionSQL.allow(reason="test allows all")


@pytest.fixture
def allow_all_plugin():
    """Register and unregister the allow-all plugin."""
    plugin = AllowAllPlugin()
    pm.register(plugin)
    yield plugin
    pm.unregister(plugin)


@pytest.fixture
def ds(tmp_path, allow_all_plugin):
    """Create a Datasette instance with test database."""
    db_path = tmp_path / "test.db"
    import sqlite3
    conn = sqlite3.connect(str(db_path))
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("CREATE TABLE posts (id INTEGER PRIMARY KEY, title TEXT, user_id INTEGER)")
    conn.close()
    return Datasette([str(db_path)])


# --- Async Client Tests ---

class TestAsyncClient:
    """Tests for the asynchronous client using Datasette's built-in client."""

    @pytest.mark.asyncio
    async def test_begin_transaction(self, ds):
        """Test beginning a transaction."""
        client = AsyncTransactionsClient(ds.client)
        tx_id = await client.begin("test", read=["users"], write=["users"])
        assert tx_id is not None
        assert len(tx_id) == 36  # UUID length
        await client.rollback(tx_id)

    @pytest.mark.asyncio
    async def test_execute_sql(self, ds):
        """Test executing SQL in a transaction."""
        client = AsyncTransactionsClient(ds.client)
        tx_id = await client.begin("test", read=["users"], write=["users"])

        # Insert a row
        result = await client.execute(tx_id, "INSERT INTO users (id, name) VALUES (1, 'Alice')")
        assert result.ok is True
        assert result.rows == []

        # Select it back
        result = await client.execute(tx_id, "SELECT * FROM users WHERE id = 1")
        assert result.ok is True
        assert len(result.rows) == 1
        assert result.rows[0]["name"] == "Alice"
        assert result.columns == ["id", "name"]

        await client.rollback(tx_id)

    @pytest.mark.asyncio
    async def test_execute_with_params(self, ds):
        """Test executing SQL with parameters."""
        client = AsyncTransactionsClient(ds.client)
        tx_id = await client.begin("test", read=["users"], write=["users"])

        result = await client.execute(
            tx_id,
            "INSERT INTO users (id, name) VALUES (:id, :name)",
            params={"id": 1, "name": "Bob"}
        )
        assert result.ok is True

        result = await client.execute(tx_id, "SELECT name FROM users WHERE id = :id", params={"id": 1})
        assert result.rows[0]["name"] == "Bob"

        await client.rollback(tx_id)

    @pytest.mark.asyncio
    async def test_commit(self, ds):
        """Test committing a transaction."""
        client = AsyncTransactionsClient(ds.client)
        tx_id = await client.begin("test", read=["users"], write=["users"])
        await client.execute(tx_id, "INSERT INTO users (id, name) VALUES (100, 'Committed')")
        await client.commit(tx_id)

        # Verify data persisted - start new transaction to read
        tx_id2 = await client.begin("test", read=["users"])
        result = await client.execute(tx_id2, "SELECT * FROM users WHERE id = 100")
        assert len(result.rows) == 1
        assert result.rows[0]["name"] == "Committed"
        await client.rollback(tx_id2)

    @pytest.mark.asyncio
    async def test_rollback(self, ds):
        """Test rolling back a transaction."""
        client = AsyncTransactionsClient(ds.client)
        tx_id = await client.begin("test", read=["users"], write=["users"])
        await client.execute(tx_id, "INSERT INTO users (id, name) VALUES (200, 'Rolled Back')")
        await client.rollback(tx_id)

        # Verify data was not persisted
        tx_id2 = await client.begin("test", read=["users"])
        result = await client.execute(tx_id2, "SELECT * FROM users WHERE id = 200")
        assert len(result.rows) == 0
        await client.rollback(tx_id2)

    @pytest.mark.asyncio
    async def test_savepoint(self, ds):
        """Test creating and using savepoints."""
        client = AsyncTransactionsClient(ds.client)
        tx_id = await client.begin("test", read=["users"], write=["users"])

        await client.execute(tx_id, "INSERT INTO users (id, name) VALUES (1, 'First')")
        await client.savepoint(tx_id, "sp1")
        await client.execute(tx_id, "INSERT INTO users (id, name) VALUES (2, 'Second')")

        # Rollback to savepoint
        await client.rollback_to(tx_id, "sp1")

        # Second insert should be gone
        result = await client.execute(tx_id, "SELECT * FROM users")
        assert len(result.rows) == 1
        assert result.rows[0]["id"] == 1

        await client.rollback(tx_id)

    @pytest.mark.asyncio
    async def test_release_savepoint(self, ds):
        """Test releasing a savepoint."""
        client = AsyncTransactionsClient(ds.client)
        tx_id = await client.begin("test", read=["users"], write=["users"])

        await client.savepoint(tx_id, "sp1")
        await client.release(tx_id, "sp1")

        # Trying to rollback to released savepoint should fail
        with pytest.raises(SavepointNotFoundError):
            await client.rollback_to(tx_id, "sp1")

        await client.rollback(tx_id)

    @pytest.mark.asyncio
    async def test_transaction_not_found(self, ds):
        """Test accessing non-existent transaction."""
        client = AsyncTransactionsClient(ds.client)

        with pytest.raises(TransactionNotFoundError):
            await client.execute("non-existent-uuid", "SELECT 1")

    @pytest.mark.asyncio
    async def test_database_not_found(self, ds):
        """Test beginning transaction on non-existent database."""
        client = AsyncTransactionsClient(ds.client)

        with pytest.raises(DatabaseNotFoundError):
            await client.begin("nonexistent")

    @pytest.mark.asyncio
    async def test_savepoint_exists(self, ds):
        """Test creating duplicate savepoint."""
        client = AsyncTransactionsClient(ds.client)
        tx_id = await client.begin("test", read=["users"])

        await client.savepoint(tx_id, "sp1")
        with pytest.raises(SavepointExistsError):
            await client.savepoint(tx_id, "sp1")

        await client.rollback(tx_id)

    @pytest.mark.asyncio
    async def test_sql_error(self, ds):
        """Test SQL syntax error."""
        client = AsyncTransactionsClient(ds.client)
        tx_id = await client.begin("test", read=["users"])

        with pytest.raises(SQLError):
            await client.execute(tx_id, "INVALID SQL SYNTAX")

        await client.rollback(tx_id)


# --- Async Transaction Context Manager Tests ---

class TestAsyncTransactionContextManager:
    """Tests for the async Transaction context manager."""

    @pytest.mark.asyncio
    async def test_context_manager_commits_on_success(self, ds):
        """Test that context manager commits on successful exit."""
        client = AsyncTransactionsClient(ds.client)

        async with client.transaction("test", read=["users"], write=["users"]) as tx:
            await tx.execute("INSERT INTO users (id, name) VALUES (300, 'Context')")

        # Verify committed
        async with client.transaction("test", read=["users"]) as tx:
            result = await tx.execute("SELECT * FROM users WHERE id = 300")
            assert len(result.rows) == 1

    @pytest.mark.asyncio
    async def test_context_manager_rollbacks_on_exception(self, ds):
        """Test that context manager rolls back on exception."""
        client = AsyncTransactionsClient(ds.client)

        with pytest.raises(ValueError):
            async with client.transaction("test", read=["users"], write=["users"]) as tx:
                await tx.execute("INSERT INTO users (id, name) VALUES (400, 'Rollback')")
                raise ValueError("Test error")

        # Verify rolled back
        async with client.transaction("test", read=["users"]) as tx:
            result = await tx.execute("SELECT * FROM users WHERE id = 400")
            assert len(result.rows) == 0

    @pytest.mark.asyncio
    async def test_context_manager_savepoints(self, ds):
        """Test savepoints within context manager."""
        client = AsyncTransactionsClient(ds.client)

        async with client.transaction("test", read=["users"], write=["users"]) as tx:
            await tx.execute("INSERT INTO users (id, name) VALUES (1, 'First')")
            await tx.savepoint("sp1")
            await tx.execute("INSERT INTO users (id, name) VALUES (2, 'Second')")
            await tx.rollback_to("sp1")

            result = await tx.execute("SELECT COUNT(*) as cnt FROM users")
            assert result.rows[0]["cnt"] == 1

    @pytest.mark.asyncio
    async def test_transaction_id_accessible(self, ds):
        """Test that transaction_id is accessible."""
        client = AsyncTransactionsClient(ds.client)

        async with client.transaction("test", read=["users"]) as tx:
            assert tx.transaction_id is not None
            assert len(tx.transaction_id) == 36


# --- Sync Client Unit Tests ---
# These test the sync client's API matches async, without full integration tests
# since ASGI apps can't be called synchronously without extra infrastructure.

class TestSyncClientAPI:
    """Unit tests verifying sync client has same API as async client."""

    def test_sync_client_has_same_methods(self):
        """Verify sync client exposes same methods as async client."""
        async_methods = {
            m for m in dir(AsyncTransactionsClient)
            if not m.startswith('_') and callable(getattr(AsyncTransactionsClient, m))
        }
        sync_methods = {
            m for m in dir(TransactionsClient)
            if not m.startswith('_') and callable(getattr(TransactionsClient, m))
        }
        assert async_methods == sync_methods

    def test_sync_transaction_has_same_methods(self):
        """Verify sync Transaction exposes same methods as AsyncTransaction."""
        # Get public methods (excluding dunder methods)
        async_methods = {
            m for m in dir(AsyncTransaction)
            if not m.startswith('_') and callable(getattr(AsyncTransaction, m))
        }
        sync_methods = {
            m for m in dir(Transaction)
            if not m.startswith('_') and callable(getattr(Transaction, m))
        }
        assert async_methods == sync_methods

    def test_execute_result_dataclass(self):
        """Test ExecuteResult can be created."""
        result = ExecuteResult(
            ok=True,
            rows=[{"id": 1, "name": "Test"}],
            columns=["id", "name"],
            truncated=False
        )
        assert result.ok is True
        assert len(result.rows) == 1
        assert result.columns == ["id", "name"]
        assert result.truncated is False


# --- Exception Tests ---

class TestExceptions:
    """Tests for exception classes."""

    def test_transaction_error_base(self):
        """Test TransactionError base exception."""
        err = TransactionError("test error", 500)
        assert str(err) == "test error"
        assert err.message == "test error"
        assert err.status_code == 500

    def test_all_exceptions_inherit_from_base(self):
        """All specific exceptions should inherit from TransactionError."""
        exceptions = [
            TransactionNotFoundError,
            TransactionExpiredError,
            PermissionDeniedError,
            TooManyTransactionsError,
            DatabaseNotFoundError,
            DatabaseImmutableError,
            SQLError,
            SavepointExistsError,
            SavepointNotFoundError,
        ]
        for exc_class in exceptions:
            assert issubclass(exc_class, TransactionError)

    def test_exceptions_can_be_caught_by_base(self):
        """Specific exceptions should be catchable as TransactionError."""
        try:
            raise DatabaseNotFoundError("Not found", 404)
        except TransactionError as e:
            assert "Not found" in str(e)
            assert e.status_code == 404
