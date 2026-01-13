"""
Python client library for datasette-transactions.

Provides both synchronous and asynchronous clients for interacting with
the datasette-transactions API endpoints.

Usage (sync):
    import httpx
    from datasette_transactions.client import TransactionsClient

    with httpx.Client(base_url="http://localhost:8001") as http:
        client = TransactionsClient(http)

        # Using context manager (recommended)
        with client.transaction("mydb", read=["users"], write=["users"]) as tx:
            tx.execute("INSERT INTO users (name) VALUES (:name)", {"name": "Alice"})
            result = tx.execute("SELECT * FROM users")
            print(result.rows)
        # Auto-commits on success, auto-rolls back on exception

        # Manual transaction management
        tx_id = client.begin("mydb", read=["users"], write=["users"])
        client.execute(tx_id, "INSERT INTO users (name) VALUES ('Bob')")
        client.commit(tx_id)

Usage (async):
    import httpx
    from datasette_transactions.client import AsyncTransactionsClient

    async with httpx.AsyncClient(base_url="http://localhost:8001") as http:
        client = AsyncTransactionsClient(http)

        async with client.transaction("mydb", read=["users"], write=["users"]) as tx:
            await tx.execute("INSERT INTO users (name) VALUES (:name)", {"name": "Alice"})
            result = await tx.execute("SELECT * FROM users")
            print(result.rows)
"""
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union
import httpx


# --- Exceptions ---

class TransactionError(Exception):
    """Base exception for transaction errors."""

    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class TransactionNotFoundError(TransactionError):
    """Transaction does not exist (404)."""
    pass


class TransactionExpiredError(TransactionError):
    """Transaction has expired/timed out (410)."""
    pass


class PermissionDeniedError(TransactionError):
    """Permission denied for operation (403)."""
    pass


class TooManyTransactionsError(TransactionError):
    """Too many concurrent transactions (429)."""
    pass


class DatabaseNotFoundError(TransactionError):
    """Database does not exist (404)."""
    pass


class DatabaseImmutableError(TransactionError):
    """Database is immutable (400)."""
    pass


class SQLError(TransactionError):
    """SQL execution error (400)."""
    pass


class SavepointExistsError(TransactionError):
    """Savepoint already exists (400)."""
    pass


class SavepointNotFoundError(TransactionError):
    """Savepoint not found (404)."""
    pass


# --- Response Models ---

@dataclass
class ExecuteResult:
    """Result from executing SQL within a transaction."""
    ok: bool
    rows: List[Dict[str, Any]]
    columns: List[str]
    truncated: bool


# --- Helper Functions ---

def _raise_for_error(response: httpx.Response, context: str = "") -> None:
    """Raise appropriate exception based on response status and content."""
    if response.status_code >= 400:
        try:
            data = response.json()
            error_msg = data.get("error", "Unknown error")
        except Exception:
            error_msg = response.text or "Unknown error"

        status = response.status_code

        # Map status codes and error messages to exceptions
        if status == 404:
            if "database" in error_msg.lower() or "Database not found" in error_msg:
                raise DatabaseNotFoundError(error_msg, status)
            elif "savepoint" in error_msg.lower():
                raise SavepointNotFoundError(error_msg, status)
            else:
                raise TransactionNotFoundError(error_msg, status)
        elif status == 410:
            raise TransactionExpiredError(error_msg, status)
        elif status == 403:
            raise PermissionDeniedError(error_msg, status)
        elif status == 429:
            raise TooManyTransactionsError(error_msg, status)
        elif status == 400:
            if "immutable" in error_msg.lower():
                raise DatabaseImmutableError(error_msg, status)
            elif "savepoint" in error_msg.lower() and "exists" in error_msg.lower():
                raise SavepointExistsError(error_msg, status)
            else:
                raise SQLError(error_msg, status)
        else:
            raise TransactionError(error_msg, status)


# --- Synchronous Client ---

class TransactionsClient:
    """Synchronous client for datasette-transactions API."""

    def __init__(self, client: httpx.Client):
        """
        Initialize the transactions client.

        Args:
            client: An httpx.Client instance configured with base_url
        """
        self._client = client

    def begin(
        self,
        database: str,
        read: Optional[List[str]] = None,
        write: Optional[List[str]] = None,
        timeout_ms: Optional[int] = None,
    ) -> str:
        """
        Begin a new transaction.

        Args:
            database: Name of the database
            read: List of tables to allow reading from
            write: List of tables to allow writing to
            timeout_ms: Optional timeout in milliseconds

        Returns:
            The transaction ID (UUID string)

        Raises:
            DatabaseNotFoundError: If database doesn't exist
            DatabaseImmutableError: If database is immutable
            PermissionDeniedError: If actor lacks required permissions
            TooManyTransactionsError: If max concurrent transactions reached
        """
        payload: Dict[str, Any] = {}
        if read is not None:
            payload["read"] = read
        if write is not None:
            payload["write"] = write
        if timeout_ms is not None:
            payload["timeout_ms"] = timeout_ms

        response = self._client.post(
            f"/-/transactions/begin/{database}",
            json=payload,
        )
        _raise_for_error(response)

        data = response.json()
        return data["transaction_id"]

    def execute(
        self,
        transaction_id: str,
        sql: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> ExecuteResult:
        """
        Execute SQL within a transaction.

        Args:
            transaction_id: The transaction ID
            sql: SQL statement to execute
            params: Optional named parameters

        Returns:
            ExecuteResult with rows, columns, etc.

        Raises:
            TransactionNotFoundError: If transaction doesn't exist
            TransactionExpiredError: If transaction has expired
            PermissionDeniedError: If table access denied
            SQLError: If SQL execution fails
        """
        payload: Dict[str, Any] = {"sql": sql}
        if params is not None:
            payload["params"] = params

        response = self._client.post(
            f"/-/transactions/{transaction_id}",
            json=payload,
        )
        _raise_for_error(response)

        data = response.json()
        return ExecuteResult(
            ok=data.get("ok", True),
            rows=data.get("rows", []),
            columns=data.get("columns", []),
            truncated=data.get("truncated", False),
        )

    def savepoint(self, transaction_id: str, name: str) -> None:
        """
        Create a savepoint within the transaction.

        Args:
            transaction_id: The transaction ID
            name: Name for the savepoint

        Raises:
            TransactionNotFoundError: If transaction doesn't exist
            TransactionExpiredError: If transaction has expired
            SavepointExistsError: If savepoint name already exists
        """
        response = self._client.post(
            f"/-/transactions/{transaction_id}/savepoint",
            json={"name": name},
        )
        _raise_for_error(response)

    def release(self, transaction_id: str, name: str) -> None:
        """
        Release (remove) a savepoint.

        Args:
            transaction_id: The transaction ID
            name: Name of the savepoint to release

        Raises:
            TransactionNotFoundError: If transaction doesn't exist
            TransactionExpiredError: If transaction has expired
            SavepointNotFoundError: If savepoint doesn't exist
        """
        response = self._client.post(
            f"/-/transactions/{transaction_id}/release",
            json={"name": name},
        )
        _raise_for_error(response)

    def rollback_to(self, transaction_id: str, name: str) -> None:
        """
        Rollback to a savepoint without ending the transaction.

        Args:
            transaction_id: The transaction ID
            name: Name of the savepoint to rollback to

        Raises:
            TransactionNotFoundError: If transaction doesn't exist
            TransactionExpiredError: If transaction has expired
            SavepointNotFoundError: If savepoint doesn't exist
        """
        response = self._client.post(
            f"/-/transactions/{transaction_id}/rollback-to",
            json={"name": name},
        )
        _raise_for_error(response)

    def commit(self, transaction_id: str) -> None:
        """
        Commit and close the transaction.

        Args:
            transaction_id: The transaction ID

        Raises:
            TransactionNotFoundError: If transaction doesn't exist
            TransactionExpiredError: If transaction has expired
        """
        response = self._client.post(
            f"/-/transactions/commit/{transaction_id}",
        )
        _raise_for_error(response)

    def rollback(self, transaction_id: str) -> None:
        """
        Rollback and close the transaction.

        Args:
            transaction_id: The transaction ID

        Raises:
            TransactionNotFoundError: If transaction doesn't exist
            TransactionExpiredError: If transaction has expired
        """
        response = self._client.post(
            f"/-/transactions/rollback/{transaction_id}",
        )
        _raise_for_error(response)

    def transaction(
        self,
        database: str,
        read: Optional[List[str]] = None,
        write: Optional[List[str]] = None,
        timeout_ms: Optional[int] = None,
    ) -> "Transaction":
        """
        Create a transaction context manager.

        Usage:
            with client.transaction("mydb", write=["users"]) as tx:
                tx.execute("INSERT INTO users ...")
            # Auto-commits on success, auto-rolls back on exception

        Args:
            database: Name of the database
            read: List of tables to allow reading from
            write: List of tables to allow writing to
            timeout_ms: Optional timeout in milliseconds

        Returns:
            A Transaction context manager
        """
        return Transaction(self, database, read, write, timeout_ms)


class Transaction:
    """
    Context manager for a database transaction.

    Automatically commits on successful exit, rolls back on exception.
    """

    def __init__(
        self,
        client: TransactionsClient,
        database: str,
        read: Optional[List[str]] = None,
        write: Optional[List[str]] = None,
        timeout_ms: Optional[int] = None,
    ):
        self._client = client
        self._database = database
        self._read = read
        self._write = write
        self._timeout_ms = timeout_ms
        self._transaction_id: Optional[str] = None

    @property
    def transaction_id(self) -> Optional[str]:
        """The transaction ID, or None if not yet started."""
        return self._transaction_id

    def __enter__(self) -> "Transaction":
        self._transaction_id = self._client.begin(
            self._database,
            read=self._read,
            write=self._write,
            timeout_ms=self._timeout_ms,
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if self._transaction_id is None:
            return False

        if exc_type is None:
            # No exception - commit
            self._client.commit(self._transaction_id)
        else:
            # Exception occurred - rollback
            try:
                self._client.rollback(self._transaction_id)
            except TransactionError:
                # Ignore errors during rollback (transaction may have expired)
                pass

        return False  # Don't suppress the exception

    def execute(
        self,
        sql: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> ExecuteResult:
        """Execute SQL within this transaction."""
        if self._transaction_id is None:
            raise TransactionError("Transaction not started")
        return self._client.execute(self._transaction_id, sql, params)

    def savepoint(self, name: str) -> None:
        """Create a savepoint."""
        if self._transaction_id is None:
            raise TransactionError("Transaction not started")
        self._client.savepoint(self._transaction_id, name)

    def release(self, name: str) -> None:
        """Release a savepoint."""
        if self._transaction_id is None:
            raise TransactionError("Transaction not started")
        self._client.release(self._transaction_id, name)

    def rollback_to(self, name: str) -> None:
        """Rollback to a savepoint."""
        if self._transaction_id is None:
            raise TransactionError("Transaction not started")
        self._client.rollback_to(self._transaction_id, name)


# --- Asynchronous Client ---

class AsyncTransactionsClient:
    """Asynchronous client for datasette-transactions API."""

    def __init__(self, client: httpx.AsyncClient):
        """
        Initialize the async transactions client.

        Args:
            client: An httpx.AsyncClient instance configured with base_url
        """
        self._client = client

    async def begin(
        self,
        database: str,
        read: Optional[List[str]] = None,
        write: Optional[List[str]] = None,
        timeout_ms: Optional[int] = None,
    ) -> str:
        """
        Begin a new transaction.

        Args:
            database: Name of the database
            read: List of tables to allow reading from
            write: List of tables to allow writing to
            timeout_ms: Optional timeout in milliseconds

        Returns:
            The transaction ID (UUID string)

        Raises:
            DatabaseNotFoundError: If database doesn't exist
            DatabaseImmutableError: If database is immutable
            PermissionDeniedError: If actor lacks required permissions
            TooManyTransactionsError: If max concurrent transactions reached
        """
        payload: Dict[str, Any] = {}
        if read is not None:
            payload["read"] = read
        if write is not None:
            payload["write"] = write
        if timeout_ms is not None:
            payload["timeout_ms"] = timeout_ms

        response = await self._client.post(
            f"/-/transactions/begin/{database}",
            json=payload,
        )
        _raise_for_error(response)

        data = response.json()
        return data["transaction_id"]

    async def execute(
        self,
        transaction_id: str,
        sql: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> ExecuteResult:
        """
        Execute SQL within a transaction.

        Args:
            transaction_id: The transaction ID
            sql: SQL statement to execute
            params: Optional named parameters

        Returns:
            ExecuteResult with rows, columns, etc.

        Raises:
            TransactionNotFoundError: If transaction doesn't exist
            TransactionExpiredError: If transaction has expired
            PermissionDeniedError: If table access denied
            SQLError: If SQL execution fails
        """
        payload: Dict[str, Any] = {"sql": sql}
        if params is not None:
            payload["params"] = params

        response = await self._client.post(
            f"/-/transactions/{transaction_id}",
            json=payload,
        )
        _raise_for_error(response)

        data = response.json()
        return ExecuteResult(
            ok=data.get("ok", True),
            rows=data.get("rows", []),
            columns=data.get("columns", []),
            truncated=data.get("truncated", False),
        )

    async def savepoint(self, transaction_id: str, name: str) -> None:
        """
        Create a savepoint within the transaction.

        Args:
            transaction_id: The transaction ID
            name: Name for the savepoint

        Raises:
            TransactionNotFoundError: If transaction doesn't exist
            TransactionExpiredError: If transaction has expired
            SavepointExistsError: If savepoint name already exists
        """
        response = await self._client.post(
            f"/-/transactions/{transaction_id}/savepoint",
            json={"name": name},
        )
        _raise_for_error(response)

    async def release(self, transaction_id: str, name: str) -> None:
        """
        Release (remove) a savepoint.

        Args:
            transaction_id: The transaction ID
            name: Name of the savepoint to release

        Raises:
            TransactionNotFoundError: If transaction doesn't exist
            TransactionExpiredError: If transaction has expired
            SavepointNotFoundError: If savepoint doesn't exist
        """
        response = await self._client.post(
            f"/-/transactions/{transaction_id}/release",
            json={"name": name},
        )
        _raise_for_error(response)

    async def rollback_to(self, transaction_id: str, name: str) -> None:
        """
        Rollback to a savepoint without ending the transaction.

        Args:
            transaction_id: The transaction ID
            name: Name of the savepoint to rollback to

        Raises:
            TransactionNotFoundError: If transaction doesn't exist
            TransactionExpiredError: If transaction has expired
            SavepointNotFoundError: If savepoint doesn't exist
        """
        response = await self._client.post(
            f"/-/transactions/{transaction_id}/rollback-to",
            json={"name": name},
        )
        _raise_for_error(response)

    async def commit(self, transaction_id: str) -> None:
        """
        Commit and close the transaction.

        Args:
            transaction_id: The transaction ID

        Raises:
            TransactionNotFoundError: If transaction doesn't exist
            TransactionExpiredError: If transaction has expired
        """
        response = await self._client.post(
            f"/-/transactions/commit/{transaction_id}",
        )
        _raise_for_error(response)

    async def rollback(self, transaction_id: str) -> None:
        """
        Rollback and close the transaction.

        Args:
            transaction_id: The transaction ID

        Raises:
            TransactionNotFoundError: If transaction doesn't exist
            TransactionExpiredError: If transaction has expired
        """
        response = await self._client.post(
            f"/-/transactions/rollback/{transaction_id}",
        )
        _raise_for_error(response)

    def transaction(
        self,
        database: str,
        read: Optional[List[str]] = None,
        write: Optional[List[str]] = None,
        timeout_ms: Optional[int] = None,
    ) -> "AsyncTransaction":
        """
        Create an async transaction context manager.

        Usage:
            async with client.transaction("mydb", write=["users"]) as tx:
                await tx.execute("INSERT INTO users ...")
            # Auto-commits on success, auto-rolls back on exception

        Args:
            database: Name of the database
            read: List of tables to allow reading from
            write: List of tables to allow writing to
            timeout_ms: Optional timeout in milliseconds

        Returns:
            An AsyncTransaction context manager
        """
        return AsyncTransaction(self, database, read, write, timeout_ms)


class AsyncTransaction:
    """
    Async context manager for a database transaction.

    Automatically commits on successful exit, rolls back on exception.
    """

    def __init__(
        self,
        client: AsyncTransactionsClient,
        database: str,
        read: Optional[List[str]] = None,
        write: Optional[List[str]] = None,
        timeout_ms: Optional[int] = None,
    ):
        self._client = client
        self._database = database
        self._read = read
        self._write = write
        self._timeout_ms = timeout_ms
        self._transaction_id: Optional[str] = None

    @property
    def transaction_id(self) -> Optional[str]:
        """The transaction ID, or None if not yet started."""
        return self._transaction_id

    async def __aenter__(self) -> "AsyncTransaction":
        self._transaction_id = await self._client.begin(
            self._database,
            read=self._read,
            write=self._write,
            timeout_ms=self._timeout_ms,
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> bool:
        if self._transaction_id is None:
            return False

        if exc_type is None:
            # No exception - commit
            await self._client.commit(self._transaction_id)
        else:
            # Exception occurred - rollback
            try:
                await self._client.rollback(self._transaction_id)
            except TransactionError:
                # Ignore errors during rollback (transaction may have expired)
                pass

        return False  # Don't suppress the exception

    async def execute(
        self,
        sql: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> ExecuteResult:
        """Execute SQL within this transaction."""
        if self._transaction_id is None:
            raise TransactionError("Transaction not started")
        return await self._client.execute(self._transaction_id, sql, params)

    async def savepoint(self, name: str) -> None:
        """Create a savepoint."""
        if self._transaction_id is None:
            raise TransactionError("Transaction not started")
        await self._client.savepoint(self._transaction_id, name)

    async def release(self, name: str) -> None:
        """Release a savepoint."""
        if self._transaction_id is None:
            raise TransactionError("Transaction not started")
        await self._client.release(self._transaction_id, name)

    async def rollback_to(self, name: str) -> None:
        """Rollback to a savepoint."""
        if self._transaction_id is None:
            raise TransactionError("Transaction not started")
        await self._client.rollback_to(self._transaction_id, name)
