"""
PostgreSQL API client.

This module provides a read-only PostgreSQL client wrapper.
All write operations are blocked by design for safety.
"""

import os
import re
from dataclasses import dataclass
from typing import Any

import psycopg


@dataclass
class PostgreSQLResponse:
    """Response from PostgreSQL query."""

    success: bool
    data: list[dict[str, Any]] | dict[str, Any] | None
    error: str | None
    rows_affected: int = 0
    columns: list[str] | None = None


class PostgreSQLClient:
    """
    Read-only PostgreSQL client wrapper.

    This client only supports SELECT statements and read-only operations.
    All write operations (INSERT, UPDATE, DELETE, DROP, etc.) are blocked.

    Connection options (environment variables):
    - POSTGRES_URI or DATABASE_URL: Full connection string
    - POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DATABASE
    - POSTGRES_USER, POSTGRES_PASSWORD
    - POSTGRES_SSLMODE: disable, require, verify-full
    """

    # SQL commands that are blocked (write operations)
    BLOCKED_COMMANDS = {
        "INSERT", "UPDATE", "DELETE", "DROP", "CREATE", "ALTER",
        "TRUNCATE", "GRANT", "REVOKE", "VACUUM", "ANALYZE",
        "REINDEX", "CLUSTER", "COPY", "LOCK", "SET"
    }

    # Allowed read-only commands
    ALLOWED_COMMANDS = {
        "SELECT", "EXPLAIN", "SHOW", "WITH"
    }

    def __init__(
        self,
        uri: str | None = None,
        host: str | None = None,
        port: int | None = None,
        database: str | None = None,
        user: str | None = None,
        password: str | None = None,
        sslmode: str | None = None,
        timeout: int = 30,
    ) -> None:
        """
        Initialize PostgreSQL client.

        Args:
            uri: Full connection string (postgresql://user:pass@host:port/db)
            host: Database host
            port: Database port (default: 5432)
            database: Database name
            user: Database user
            password: Database password
            sslmode: SSL mode (disable, require, verify-full)
            timeout: Connection timeout in seconds
        """
        # Try connection URI first
        self.uri = (
            uri
            or os.environ.get("POSTGRES_URI")
            or os.environ.get("DATABASE_URL")
        )

        # Individual connection parameters
        self.host = host or os.environ.get("POSTGRES_HOST") or "localhost"
        self.port = port or int(os.environ.get("POSTGRES_PORT", "5432"))
        self.database = database or os.environ.get("POSTGRES_DATABASE") or "postgres"
        self.user = user or os.environ.get("POSTGRES_USER") or "postgres"
        self.password = password or os.environ.get("POSTGRES_PASSWORD", "")
        self.sslmode = sslmode or os.environ.get("POSTGRES_SSLMODE", "prefer")
        self.timeout = timeout

        self._conn: psycopg.Connection | None = None

    @property
    def connection(self) -> psycopg.Connection:
        """Get or create database connection."""
        if self._conn is None or self._conn.closed:
            if self.uri:
                # Use connection URI
                self._conn = psycopg.connect(
                    self.uri,
                    connect_timeout=self.timeout,
                    options=f"-c statement_timeout={self.timeout * 1000}"
                )
            else:
                # Build connection from parameters
                self._conn = psycopg.connect(
                    host=self.host,
                    port=self.port,
                    dbname=self.database,
                    user=self.user,
                    password=self.password,
                    sslmode=self.sslmode,
                    connect_timeout=self.timeout,
                    options=f"-c statement_timeout={self.timeout * 1000}"
                )

            # Set read-only transaction mode for safety
            self._conn.autocommit = False
            with self._conn.cursor() as cur:
                cur.execute("SET TRANSACTION READ ONLY")
                self._conn.commit()

        return self._conn

    def _validate_query(self, query: str) -> None:
        """
        Validate that query is read-only.

        Args:
            query: SQL query to validate

        Raises:
            ValueError: If query contains write operations
        """
        # Normalize query for checking
        query_upper = query.strip().upper()

        # Remove comments
        query_upper = re.sub(r'--.*$', '', query_upper, flags=re.MULTILINE)
        query_upper = re.sub(r'/\*.*?\*/', '', query_upper, flags=re.DOTALL)

        # Extract first command
        first_word = query_upper.split()[0] if query_upper.split() else ""

        # Check for blocked commands
        for blocked in self.BLOCKED_COMMANDS:
            if blocked in query_upper:
                # Allow EXPLAIN ANALYZE even though it contains "ANALYZE"
                if blocked == "ANALYZE" and query_upper.startswith("EXPLAIN"):
                    continue
                raise ValueError(
                    f"Query contains blocked command: {blocked}. "
                    f"Only SELECT, EXPLAIN, SHOW, and WITH queries are allowed."
                )

        # Ensure query starts with allowed command
        if first_word not in self.ALLOWED_COMMANDS:
            raise ValueError(
                f"Query must start with one of: {', '.join(self.ALLOWED_COMMANDS)}. "
                f"Got: {first_word}"
            )

    def execute_query(
        self,
        query: str,
        params: tuple | dict | None = None,
    ) -> PostgreSQLResponse:
        """
        Execute a read-only SQL query.

        Args:
            query: SQL query to execute (must be SELECT/EXPLAIN/SHOW/WITH)
            params: Query parameters (tuple for %s, dict for %(name)s)

        Returns:
            PostgreSQLResponse with results or error
        """
        try:
            # Validate query is read-only
            self._validate_query(query)

            with self.connection.cursor() as cur:
                cur.execute(query, params)

                # Check if query returns rows
                if cur.description:
                    columns = [desc[0] for desc in cur.description]
                    rows = cur.fetchall()

                    # Convert to list of dicts
                    data = [
                        dict(zip(columns, row, strict=False))
                        for row in rows
                    ]

                    return PostgreSQLResponse(
                        success=True,
                        data=data,
                        error=None,
                        rows_affected=len(data),
                        columns=columns,
                    )
                else:
                    # Query executed but returned no rows (e.g., SHOW)
                    return PostgreSQLResponse(
                        success=True,
                        data=[],
                        error=None,
                        rows_affected=0,
                    )

        except ValueError as e:
            # Query validation failed
            return PostgreSQLResponse(
                success=False,
                data=None,
                error=str(e),
            )
        except psycopg.Error as e:
            # Database error
            return PostgreSQLResponse(
                success=False,
                data=None,
                error=f"Database error: {e}",
            )
        except Exception as e:
            # Other errors
            return PostgreSQLResponse(
                success=False,
                data=None,
                error=f"Error: {e}",
            )

    def close(self) -> None:
        """Close database connection."""
        if self._conn and not self._conn.closed:
            self._conn.close()
            self._conn = None

    def __enter__(self) -> "PostgreSQLClient":
        return self

    def __exit__(self, *args) -> None:
        self.close()
