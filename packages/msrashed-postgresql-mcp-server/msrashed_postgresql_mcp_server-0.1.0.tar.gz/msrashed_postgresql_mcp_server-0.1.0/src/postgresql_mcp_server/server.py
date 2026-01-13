"""
PostgreSQL MCP Server.

A read-only MCP server for PostgreSQL database platform.
All operations are safe and cannot modify database data.
"""

from mcp.server.fastmcp import FastMCP

from postgresql_mcp_server.tools.registry import PostgreSQLTools

SERVER_INSTRUCTIONS = """
PostgreSQL MCP Server - Read-Only Database Inspection & Analysis

This server provides read-only access to PostgreSQL databases.
All operations are safe and cannot modify your database data.

## Available Tools:

### Database Discovery (6 tools)
- **list_databases**: List all databases with size and connection info
- **list_schemas**: List all schemas (namespaces) in database
- **list_tables**: List tables in schema with size and row estimates
- **list_views**: List views in schema with definitions
- **get_table_info**: Get detailed column information for a table
- **describe_table**: Comprehensive table structure with constraints

### Schema Inspection (5 tools)
- **get_indexes**: List all indexes on a table with type and size
- **get_constraints**: Get foreign keys, unique, and check constraints
- **get_table_size**: Detailed size breakdown (table, indexes, toast)
- **get_row_count**: Fast estimate or exact count of table rows
- **get_table_access_stats**: Read/write patterns for a table

### Query Tools (3 tools)
- **execute_query**: Execute SELECT queries (write operations blocked)
- **explain_query**: Get query execution plan (EXPLAIN/EXPLAIN ANALYZE)
- **get_sample_data**: Get sample rows from a table for inspection

### Analysis Tools (5 tools)
- **find_missing_indexes**: Suggest indexes based on sequential scans
- **find_unused_indexes**: Find indexes never used (candidates for removal)
- **find_bloated_tables**: Find tables with dead tuples needing VACUUM
- **get_table_bloat**: Estimate bloat percentage for specific table
- **find_long_running_queries**: Find queries exceeding duration threshold

### Monitoring Tools (5 tools)
- **get_database_stats**: Database statistics (connections, transactions, blocks)
- **get_connection_stats**: Active connections grouped by state/database/user
- **get_lock_info**: Current locks and blocked queries (deadlock diagnosis)
- **get_replication_status**: Streaming replication lag and status
- **get_cache_hit_ratio**: Buffer cache effectiveness (target >99%)

### Performance Tools (3 tools)
- **get_slow_queries**: Slowest queries from pg_stat_statements
- **get_index_usage**: Index scan vs sequential scan ratios
- **get_table_access_stats**: Detailed read/write patterns per table

## Common Use Cases:

### Schema Discovery:
```
# Explore database structure
list_databases()
list_schemas()
list_tables(schema="public")
get_table_info(table="users", schema="public")
```

### Query Analysis:
```
# Execute and analyze queries
execute_query(query="SELECT * FROM users WHERE status = 'active' LIMIT 10")
explain_query(query="SELECT * FROM orders WHERE user_id = 123", analyze=True)
```

### Performance Tuning:
```
# Find performance issues
find_missing_indexes()
find_unused_indexes()
get_slow_queries(limit=10)
get_index_usage()
```

### Monitoring:
```
# Monitor database health
get_connection_stats()
get_lock_info()
get_cache_hit_ratio()
find_long_running_queries(min_duration_seconds=60)
```

### Maintenance:
```
# Identify maintenance needs
find_bloated_tables()
get_table_bloat(table="large_table")
get_table_size(table="orders")
```

## Connection Configuration:

Set via environment variables:
- POSTGRES_URI or DATABASE_URL: Full connection string
  Example: postgresql://user:pass@localhost:5432/mydb
- OR individual parameters:
  - POSTGRES_HOST: Database host (default: localhost)
  - POSTGRES_PORT: Database port (default: 5432)
  - POSTGRES_DATABASE: Database name (default: postgres)
  - POSTGRES_USER: Database user (default: postgres)
  - POSTGRES_PASSWORD: Database password
  - POSTGRES_SSLMODE: SSL mode (disable, require, verify-full)

## Security & Safety:

- **READ-ONLY MODE**: All operations run in read-only transactions
- **BLOCKED OPERATIONS**: INSERT, UPDATE, DELETE, DROP, CREATE, ALTER are blocked
- **ALLOWED OPERATIONS**: Only SELECT, EXPLAIN, SHOW, WITH queries permitted
- **SAFE FOR PRODUCTION**: Cannot modify data or schema

## Extensions:

Some tools require PostgreSQL extensions:
- **pg_stat_statements**: For get_slow_queries() tool
  Enable: CREATE EXTENSION pg_stat_statements;
- **pg_stat_user_tables**: Built-in, shows table access patterns
- **pg_statio_user_tables**: Built-in, shows I/O statistics

## Tips:

1. **Performance**: Use estimated row counts for large tables (exact=False)
2. **Index Analysis**: Run find_missing_indexes() and find_unused_indexes() together
3. **Bloat**: Check find_bloated_tables() regularly, VACUUM when needed
4. **Monitoring**: Monitor get_cache_hit_ratio() - aim for >99%
5. **Query Plans**: Use explain_query(analyze=True) to see actual execution stats
"""


def create_server(
    uri: str | None = None,
    host: str | None = None,
    port: int | None = None,
    database: str | None = None,
    user: str | None = None,
    password: str | None = None,
    sslmode: str | None = None,
    timeout: int = 30,
) -> FastMCP:
    """
    Create and configure the PostgreSQL MCP server.

    Args:
        uri: Full connection string (postgresql://user:pass@host:port/db)
        host: Database host
        port: Database port
        database: Database name
        user: Database user
        password: Database password
        sslmode: SSL mode (disable, require, verify-full)
        timeout: Query timeout in seconds

    Returns:
        Configured FastMCP server instance
    """
    mcp = FastMCP(
        name="postgresql-mcp-server",
        instructions=SERVER_INSTRUCTIONS,
    )

    # Register all PostgreSQL tools
    PostgreSQLTools(
        mcp=mcp,
        uri=uri,
        host=host,
        port=port,
        database=database,
        user=user,
        password=password,
        sslmode=sslmode,
        timeout=timeout,
    )

    return mcp


def main() -> None:
    """Entry point for the PostgreSQL MCP server."""
    from postgresql_mcp_server.cli import main as cli_main

    cli_main()


if __name__ == "__main__":
    main()
