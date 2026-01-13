"""
Command-line interface for PostgreSQL MCP Server.

Provides a Click-based CLI for running the MCP server and testing
all PostgreSQL tools directly from the command line.
"""

import json
import sys
from collections.abc import Callable
from functools import wraps
from typing import Any

import click

from postgresql_mcp_server.server import create_server
from postgresql_mcp_server.utils.client import PostgreSQLClient


def common_options(func: Callable) -> Callable:
    """Decorator to add common PostgreSQL connection options."""

    @click.option(
        "--uri",
        envvar=["POSTGRES_URI", "DATABASE_URL"],
        default=None,
        help="Full PostgreSQL connection string (postgresql://user:pass@host:port/db).",
        show_envvar=True,
    )
    @click.option(
        "--host",
        envvar="POSTGRES_HOST",
        default="localhost",
        help="PostgreSQL host.",
        show_default=True,
        show_envvar=True,
    )
    @click.option(
        "--port",
        envvar="POSTGRES_PORT",
        type=int,
        default=5432,
        help="PostgreSQL port.",
        show_default=True,
        show_envvar=True,
    )
    @click.option(
        "--database",
        envvar="POSTGRES_DATABASE",
        default="postgres",
        help="Database name.",
        show_default=True,
        show_envvar=True,
    )
    @click.option(
        "--user",
        envvar="POSTGRES_USER",
        default="postgres",
        help="Database user.",
        show_default=True,
        show_envvar=True,
    )
    @click.option(
        "--password",
        envvar="POSTGRES_PASSWORD",
        default="",
        help="Database password.",
        show_envvar=True,
    )
    @click.option(
        "--sslmode",
        envvar="POSTGRES_SSLMODE",
        type=click.Choice(["disable", "require", "verify-full"]),
        default="prefer",
        help="SSL mode.",
        show_default=True,
        show_envvar=True,
    )
    @click.option(
        "--timeout",
        envvar="POSTGRES_TIMEOUT",
        type=int,
        default=30,
        help="Query timeout in seconds.",
        show_default=True,
    )
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def get_client(
    uri: str | None,
    host: str,
    port: int,
    database: str,
    user: str,
    password: str,
    sslmode: str,
    timeout: int,
) -> PostgreSQLClient:
    """Create a PostgreSQL client with the given options."""
    return PostgreSQLClient(
        uri=uri,
        host=host,
        port=port,
        database=database,
        user=user,
        password=password,
        sslmode=sslmode,
        timeout=timeout,
    )


def output_response(response: Any) -> None:
    """Output response in formatted JSON."""
    if response.success:
        result = {
            "data": response.data,
            "rows": response.rows_affected
        }
        if response.columns:
            result["columns"] = response.columns
        click.echo(json.dumps(result, indent=2, default=str))
    else:
        click.echo(
            click.style(f"Error: {response.error}", fg="red"),
            err=True,
        )
        sys.exit(1)


# ============================================================
# Main CLI Group
# ============================================================


@click.group()
@click.version_option(package_name="msrashed-postgresql-mcp-server")
def cli() -> None:
    """PostgreSQL MCP Server - Read-only database inspection and analysis.

    A Model Context Protocol (MCP) server that provides safe, read-only access
    to PostgreSQL databases. All operations are non-destructive.

    \b
    COMMAND GROUPS:
      run       Start the MCP server (stdio, HTTP, SSE transports)
      db        Database and schema discovery
      schema    Schema inspection (tables, views, columns)
      tables    Table operations (describe, size, samples)
      query     Execute and explain queries
      analyze   Performance analysis (indexes, bloat, slow queries)
      status    Monitor connections, locks, replication
      check     Test database connection
      info      Show tool/CLI mapping

    \b
    AUTHENTICATION:
      Set via options or environment variables:
        --uri / POSTGRES_URI          Full connection string
        --host / POSTGRES_HOST        Database host
        --port / POSTGRES_PORT        Database port
        --database / POSTGRES_DATABASE  Database name
        --user / POSTGRES_USER        Database user
        --password / POSTGRES_PASSWORD  Database password

    \b
    QUICK START:
      # Check connection
      postgresql-mcp-server check --uri postgresql://localhost/mydb

      # List databases
      postgresql-mcp-server db list

      # Execute query
      postgresql-mcp-server query execute "SELECT * FROM users LIMIT 10"

      # Start MCP server
      postgresql-mcp-server run
    """
    pass


# ============================================================
# Server Commands
# ============================================================


@cli.command()
@common_options
@click.option(
    "--transport",
    type=click.Choice(["stdio", "http", "sse", "streamable-http"]),
    default="stdio",
    help="MCP transport mechanism.",
    show_default=True,
)
@click.option(
    "--host-bind",
    default="127.0.0.1",
    help="Bind address for HTTP/SSE transport.",
    show_default=True,
)
@click.option(
    "--port-bind",
    type=int,
    default=8000,
    help="Port for HTTP/SSE transport.",
    show_default=True,
)
def run(
    uri: str | None,
    host: str,
    port: int,
    database: str,
    user: str,
    password: str,
    sslmode: str,
    timeout: int,
    transport: str,
    host_bind: str,
    port_bind: int,
) -> None:
    """Run the PostgreSQL MCP server.

    Starts the MCP server that AI agents can connect to for querying PostgreSQL.
    The server provides 27 read-only tools for database inspection and analysis.

    \b
    TRANSPORTS:
      stdio           Standard I/O (default) - for CLI tools and local agents
      http            HTTP POST - for web integrations
      sse             Server-Sent Events - for real-time streaming
      streamable-http Streamable HTTP - for large responses

    \b
    EXAMPLES:
      # Run with stdio (default, for desktop apps)
      postgresql-mcp-server run

      # Run with HTTP transport
      postgresql-mcp-server run --transport http --port-bind 8000

      # Run with custom database
      postgresql-mcp-server run --uri postgresql://user:pass@localhost/mydb
    """
    server = create_server(
        uri=uri,
        host=host,
        port=port,
        database=database,
        user=user,
        password=password,
        sslmode=sslmode,
        timeout=timeout,
    )

    if transport == "stdio":
        server.run(transport="stdio")
    elif transport == "http":
        server.run(transport="http", host=host_bind, port=port_bind)
    elif transport == "sse":
        server.run(transport="sse", host=host_bind, port=port_bind)
    elif transport == "streamable-http":
        server.run(transport="streamable-http", host=host_bind, port=port_bind)


# ============================================================
# Database Commands Group
# ============================================================


@cli.group()
def db() -> None:
    """Database and schema discovery commands.

    List databases, schemas, and get database-level statistics.
    """
    pass


@db.command("list")
@common_options
def db_list(
    uri: str | None,
    host: str,
    port: int,
    database: str,
    user: str,
    password: str,
    sslmode: str,
    timeout: int,
) -> None:
    """List all databases with size and connection info."""
    query = """
    SELECT
        d.datname,
        pg_catalog.pg_get_userbyid(d.datdba) as owner,
        pg_catalog.pg_encoding_to_char(d.encoding) as encoding,
        pg_catalog.pg_size_pretty(pg_catalog.pg_database_size(d.datname)) as size,
        (SELECT count(*) FROM pg_stat_activity WHERE datname = d.datname) as connections
    FROM pg_catalog.pg_database d
    WHERE d.datistemplate = false
    ORDER BY d.datname;
    """

    with get_client(uri, host, port, database, user, password, sslmode, timeout) as client:
        response = client.execute_query(query)
        output_response(response)


@db.command("stats")
@common_options
@click.option("--database-name", default=None, help="Specific database name (default: current).")
def db_stats(
    uri: str | None,
    host: str,
    port: int,
    database: str,
    user: str,
    password: str,
    sslmode: str,
    timeout: int,
    database_name: str | None,
) -> None:
    """Get statistics for current or specified database."""
    if database_name:
        query = "SELECT * FROM pg_stat_database WHERE datname = %s;"
        params = (database_name,)
    else:
        query = "SELECT * FROM pg_stat_database WHERE datname = current_database();"
        params = None

    with get_client(uri, host, port, database, user, password, sslmode, timeout) as client:
        response = client.execute_query(query, params)
        output_response(response)


# ============================================================
# Schema Commands Group
# ============================================================


@cli.group()
def schema() -> None:
    """Schema inspection commands.

    List schemas, tables, views, and get column information.
    """
    pass


@schema.command("list")
@common_options
def schema_list(
    uri: str | None,
    host: str,
    port: int,
    database: str,
    user: str,
    password: str,
    sslmode: str,
    timeout: int,
) -> None:
    """List all schemas in the database."""
    query = """
    SELECT
        n.nspname as schema_name,
        pg_catalog.pg_get_userbyid(n.nspowner) as owner
    FROM pg_catalog.pg_namespace n
    WHERE n.nspname !~ '^pg_' AND n.nspname <> 'information_schema'
    ORDER BY n.nspname;
    """

    with get_client(uri, host, port, database, user, password, sslmode, timeout) as client:
        response = client.execute_query(query)
        output_response(response)


# ============================================================
# Tables Commands Group
# ============================================================


@cli.group()
def tables() -> None:
    """Table operations.

    List tables, describe structure, get sizes, and sample data.
    """
    pass


@tables.command("list")
@common_options
@click.option("--schema", default="public", help="Schema name.", show_default=True)
def tables_list(
    uri: str | None,
    host: str,
    port: int,
    database: str,
    user: str,
    password: str,
    sslmode: str,
    timeout: int,
    schema: str,
) -> None:
    """List all tables in a schema."""
    query = """
    SELECT
        c.relname as table_name,
        pg_catalog.pg_get_userbyid(c.relowner) as owner,
        pg_catalog.pg_size_pretty(pg_catalog.pg_total_relation_size(c.oid)) as total_size,
        c.reltuples::bigint as row_estimate
    FROM pg_catalog.pg_class c
    LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
    WHERE c.relkind = 'r' AND n.nspname = %s
    ORDER BY pg_catalog.pg_total_relation_size(c.oid) DESC;
    """

    with get_client(uri, host, port, database, user, password, sslmode, timeout) as client:
        response = client.execute_query(query, (schema,))
        output_response(response)


@tables.command("describe")
@common_options
@click.argument("table")
@click.option("--schema", default="public", help="Schema name.", show_default=True)
def tables_describe(
    uri: str | None,
    host: str,
    port: int,
    database: str,
    user: str,
    password: str,
    sslmode: str,
    timeout: int,
    table: str,
    schema: str,
) -> None:
    """Get detailed table structure including columns and constraints."""
    query = """
    SELECT
        a.attname as column_name,
        pg_catalog.format_type(a.atttypid, a.atttypmod) as data_type,
        a.attnotnull as not_null,
        (SELECT pg_catalog.pg_get_expr(d.adbin, d.adrelid)
         FROM pg_catalog.pg_attrdef d
         WHERE d.adrelid = a.attrelid AND d.adnum = a.attnum AND a.atthasdef) as default_value
    FROM pg_catalog.pg_attribute a
    JOIN pg_catalog.pg_class c ON a.attrelid = c.oid
    JOIN pg_catalog.pg_namespace n ON c.relnamespace = n.oid
    WHERE c.relname = %s AND n.nspname = %s AND a.attnum > 0 AND NOT a.attisdropped
    ORDER BY a.attnum;
    """

    with get_client(uri, host, port, database, user, password, sslmode, timeout) as client:
        response = client.execute_query(query, (table, schema))
        output_response(response)


@tables.command("size")
@common_options
@click.argument("table")
@click.option("--schema", default="public", help="Schema name.", show_default=True)
def tables_size(
    uri: str | None,
    host: str,
    port: int,
    database: str,
    user: str,
    password: str,
    sslmode: str,
    timeout: int,
    table: str,
    schema: str,
) -> None:
    """Get detailed size information for a table."""
    query = """
    SELECT
        pg_catalog.pg_size_pretty(pg_catalog.pg_table_size(c.oid)) as table_size,
        pg_catalog.pg_size_pretty(pg_catalog.pg_indexes_size(c.oid)) as indexes_size,
        pg_catalog.pg_size_pretty(pg_catalog.pg_total_relation_size(c.oid)) as total_size
    FROM pg_catalog.pg_class c
    JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
    WHERE c.relname = %s AND n.nspname = %s;
    """

    with get_client(uri, host, port, database, user, password, sslmode, timeout) as client:
        response = client.execute_query(query, (table, schema))
        output_response(response)


# ============================================================
# Query Commands Group
# ============================================================


@cli.group()
def query() -> None:
    """Execute and analyze queries.

    Run SELECT queries and get execution plans.
    """
    pass


@query.command("execute")
@common_options
@click.argument("sql")
@click.option("--limit", type=int, default=100, help="Row limit.", show_default=True)
def query_execute(
    uri: str | None,
    host: str,
    port: int,
    database: str,
    user: str,
    password: str,
    sslmode: str,
    timeout: int,
    sql: str,
    limit: int,
) -> None:
    """Execute a SELECT query (READ-ONLY).

    \b
    Examples:
      postgresql-mcp-server query execute "SELECT * FROM users LIMIT 10"
      postgresql-mcp-server query execute "SELECT COUNT(*) FROM orders WHERE status = 'pending'"
    """
    # Add LIMIT if not present
    if "LIMIT" not in sql.upper():
        sql = f"{sql.rstrip(';')} LIMIT {limit}"

    with get_client(uri, host, port, database, user, password, sslmode, timeout) as client:
        response = client.execute_query(sql)
        output_response(response)


@query.command("explain")
@common_options
@click.argument("sql")
@click.option("--analyze", is_flag=True, help="Run EXPLAIN ANALYZE (executes query).")
def query_explain(
    uri: str | None,
    host: str,
    port: int,
    database: str,
    user: str,
    password: str,
    sslmode: str,
    timeout: int,
    sql: str,
    analyze: bool,
) -> None:
    """Get query execution plan.

    \b
    Examples:
      postgresql-mcp-server query explain "SELECT * FROM users WHERE email = 'test@example.com'"
      postgresql-mcp-server query explain --analyze "SELECT * FROM orders WHERE status = 'pending'"
    """
    if analyze:
        explain_sql = f"EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) {sql}"
    else:
        explain_sql = f"EXPLAIN (FORMAT JSON) {sql}"

    with get_client(uri, host, port, database, user, password, sslmode, timeout) as client:
        response = client.execute_query(explain_sql)
        output_response(response)


# ============================================================
# Analyze Commands Group
# ============================================================


@cli.group()
def analyze() -> None:
    """Performance analysis commands.

    Find missing indexes, bloat, and slow queries.
    """
    pass


@analyze.command("indexes")
@common_options
def analyze_indexes(
    uri: str | None,
    host: str,
    port: int,
    database: str,
    user: str,
    password: str,
    sslmode: str,
    timeout: int,
) -> None:
    """Suggest missing indexes based on sequential scans."""
    query = """
    SELECT
        schemaname as schema,
        tablename as table,
        seq_scan,
        seq_tup_read,
        idx_scan,
        CASE WHEN seq_scan + idx_scan > 0
            THEN ROUND((100.0 * seq_scan / (seq_scan + idx_scan))::numeric, 2)
            ELSE 0
        END as seq_scan_percent
    FROM pg_stat_user_tables
    WHERE seq_scan > 0
    ORDER BY seq_tup_read DESC
    LIMIT 20;
    """

    with get_client(uri, host, port, database, user, password, sslmode, timeout) as client:
        response = client.execute_query(query)
        output_response(response)


@analyze.command("bloat")
@common_options
def analyze_bloat(
    uri: str | None,
    host: str,
    port: int,
    database: str,
    user: str,
    password: str,
    sslmode: str,
    timeout: int,
) -> None:
    """Find tables with significant bloat."""
    query = """
    SELECT
        schemaname as schema,
        tablename as table,
        n_dead_tup,
        n_live_tup,
        CASE WHEN n_live_tup > 0
            THEN ROUND((n_dead_tup::float / n_live_tup::float)::numeric, 4)
            ELSE 0
        END as bloat_ratio
    FROM pg_stat_user_tables
    WHERE n_dead_tup > 1000
    ORDER BY n_dead_tup DESC
    LIMIT 20;
    """

    with get_client(uri, host, port, database, user, password, sslmode, timeout) as client:
        response = client.execute_query(query)
        output_response(response)


@analyze.command("slow")
@common_options
@click.option("--limit", type=int, default=10, help="Number of queries.", show_default=True)
def analyze_slow(
    uri: str | None,
    host: str,
    port: int,
    database: str,
    user: str,
    password: str,
    sslmode: str,
    timeout: int,
    limit: int,
) -> None:
    """Get slowest queries from pg_stat_statements (requires extension)."""
    query = """
    SELECT
        query,
        calls,
        total_exec_time as total_time,
        mean_exec_time as mean_time,
        rows
    FROM pg_stat_statements
    ORDER BY total_exec_time DESC
    LIMIT %s;
    """

    with get_client(uri, host, port, database, user, password, sslmode, timeout) as client:
        response = client.execute_query(query, (limit,))
        output_response(response)


# ============================================================
# Status Commands Group
# ============================================================


@cli.group()
def status() -> None:
    """Monitor database status.

    Check connections, locks, and replication.
    """
    pass


@status.command("connections")
@common_options
def status_connections(
    uri: str | None,
    host: str,
    port: int,
    database: str,
    user: str,
    password: str,
    sslmode: str,
    timeout: int,
) -> None:
    """Get current connection statistics."""
    query = """
    SELECT
        COUNT(*) as total_connections,
        COUNT(*) FILTER (WHERE state = 'active') as active,
        COUNT(*) FILTER (WHERE state = 'idle') as idle,
        datname,
        usename
    FROM pg_stat_activity
    GROUP BY datname, usename
    ORDER BY total_connections DESC;
    """

    with get_client(uri, host, port, database, user, password, sslmode, timeout) as client:
        response = client.execute_query(query)
        output_response(response)


@status.command("locks")
@common_options
def status_locks(
    uri: str | None,
    host: str,
    port: int,
    database: str,
    user: str,
    password: str,
    sslmode: str,
    timeout: int,
) -> None:
    """Get information about current locks and blocked queries."""
    query = """
    SELECT
        blocked_locks.pid AS blocked_pid,
        blocked_activity.usename AS blocked_user,
        blocking_locks.pid AS blocking_pid,
        blocking_activity.usename AS blocking_user,
        blocked_activity.query AS blocked_statement
    FROM pg_catalog.pg_locks blocked_locks
    JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
    JOIN pg_catalog.pg_locks blocking_locks
        ON blocking_locks.locktype = blocked_locks.locktype
        AND blocking_locks.pid != blocked_locks.pid
    JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
    WHERE NOT blocked_locks.granted
    LIMIT 20;
    """

    with get_client(uri, host, port, database, user, password, sslmode, timeout) as client:
        response = client.execute_query(query)
        output_response(response)


@status.command("replication")
@common_options
def status_replication(
    uri: str | None,
    host: str,
    port: int,
    database: str,
    user: str,
    password: str,
    sslmode: str,
    timeout: int,
) -> None:
    """Get streaming replication status and lag."""
    query = """
    SELECT
        client_addr,
        usename,
        state,
        sync_state,
        replay_lag
    FROM pg_stat_replication;
    """

    with get_client(uri, host, port, database, user, password, sslmode, timeout) as client:
        response = client.execute_query(query)
        output_response(response)


# ============================================================
# Utility Commands
# ============================================================


@cli.command()
@common_options
def check(
    uri: str | None,
    host: str,
    port: int,
    database: str,
    user: str,
    password: str,
    sslmode: str,
    timeout: int,
) -> None:
    """Test database connection."""
    try:
        with get_client(uri, host, port, database, user, password, sslmode, timeout) as client:
            response = client.execute_query("SELECT version();")
            if response.success:
                click.echo(click.style("Connection successful!", fg="green"))
                click.echo(json.dumps(response.data, indent=2))
            else:
                click.echo(click.style(f"Connection failed: {response.error}", fg="red"))
                sys.exit(1)
    except Exception as e:
        click.echo(click.style(f"Connection error: {e}", fg="red"))
        sys.exit(1)


@cli.command()
def info() -> None:
    """Show tool/CLI command mapping."""
    mapping = {
        "Database Discovery": {
            "list_databases": "postgresql-mcp-server db list",
            "list_schemas": "postgresql-mcp-server schema list",
            "list_tables": "postgresql-mcp-server tables list --schema=public",
            "get_table_info": "postgresql-mcp-server tables describe TABLE --schema=public",
        },
        "Query Tools": {
            "execute_query": "postgresql-mcp-server query execute 'SELECT ...'",
            "explain_query": "postgresql-mcp-server query explain 'SELECT ...'",
        },
        "Analysis Tools": {
            "find_missing_indexes": "postgresql-mcp-server analyze indexes",
            "find_bloated_tables": "postgresql-mcp-server analyze bloat",
            "get_slow_queries": "postgresql-mcp-server analyze slow",
        },
        "Monitoring Tools": {
            "get_connection_stats": "postgresql-mcp-server status connections",
            "get_lock_info": "postgresql-mcp-server status locks",
            "get_replication_status": "postgresql-mcp-server status replication",
        },
    }

    click.echo("MCP Tool to CLI Command Mapping:\n")
    for category, tools in mapping.items():
        click.echo(click.style(f"{category}:", fg="blue", bold=True))
        for tool, command in tools.items():
            click.echo(f"  {tool:30} → {command}")
        click.echo()


def main() -> None:
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
