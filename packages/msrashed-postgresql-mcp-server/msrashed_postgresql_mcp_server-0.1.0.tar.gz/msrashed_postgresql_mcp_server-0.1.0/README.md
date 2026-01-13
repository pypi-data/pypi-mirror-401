# PostgreSQL MCP Server

A read-only Model Context Protocol (MCP) server for [PostgreSQL](https://www.postgresql.org/), enabling AI agents like software engineers to safely inspect databases, analyze performance, and query data without risking modifications.

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-1.24.0+-green.svg)](https://github.com/anthropics/mcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **Read-Only Safety**: All operations are read-only. No INSERT, UPDATE, DELETE, DROP, or ALTER operations
- **Comprehensive Discovery**: List databases, schemas, tables, views, columns, indexes, and constraints
- **Query Execution**: Execute SELECT queries and EXPLAIN plans safely
- **Performance Analysis**: Find missing indexes, unused indexes, bloated tables, and slow queries
- **Monitoring Tools**: View connections, locks, replication lag, and cache hit ratios
- **Type-Safe**: Full type hints for Python 3.12+
- **Dual Interface**: Use as MCP server for AI agents or CLI tool for direct database access

## Installation

### Using uv (Recommended)

```bash
# Install from PyPI
uv pip install msrashed-postgresql-mcp-server

# Or install with pipx for CLI usage
pipx install msrashed-postgresql-mcp-server
```

### Using pip

```bash
pip install msrashed-postgresql-mcp-server
```

## Quick Start

### 1. Set Environment Variables

```bash
# Option 1: Full connection URI
export POSTGRES_URI="postgresql://user:password@localhost:5432/mydb"

# Option 2: Individual parameters
export POSTGRES_HOST="localhost"
export POSTGRES_PORT="5432"
export POSTGRES_DATABASE="mydb"
export POSTGRES_USER="postgres"
export POSTGRES_PASSWORD="secret"
export POSTGRES_SSLMODE="prefer"  # or disable, require, verify-full
```

### 2. Test Connection

```bash
postgresql-mcp-server check --uri postgresql://localhost/mydb
```

### 3. Run the MCP Server

```bash
# Using stdio transport (default, for AI agents)
postgresql-mcp-server run

# Using HTTP transport
postgresql-mcp-server run --transport http --port-bind 8000
```

### 4. Configure with AI Agents

Add to your AI agent configuration (e.g., desktops app):

```json
{
  "mcpServers": {
    "postgresql": {
      "command": "postgresql-mcp-server",
      "args": ["run"],
      "env": {
        "POSTGRES_URI": "postgresql://user:password@localhost:5432/mydb"
      }
    }
  }
}
```

Or with uvx:

```json
{
  "mcpServers": {
    "postgresql": {
      "command": "uvx",
      "args": ["msrashed-postgresql-mcp-server", "run"],
      "env": {
        "POSTGRES_URI": "postgresql://localhost:5432/mydb"
      }
    }
  }
}
```

## CLI Command Reference

The CLI provides commands that mirror all MCP tools, enabling direct testing and automation.

### Connection & Info Commands

```bash
# Test database connection
postgresql-mcp-server check --uri postgresql://localhost/mydb

# Show tool/CLI mapping
postgresql-mcp-server info

# Show version
postgresql-mcp-server --version
```

### Database Discovery Commands

```bash
# List all databases
postgresql-mcp-server db list --uri postgresql://localhost/postgres

# Get database statistics
postgresql-mcp-server db stats --uri postgresql://localhost/mydb

# List schemas
postgresql-mcp-server schema list --uri postgresql://localhost/mydb
```

### Table Operations

```bash
# List tables in schema
postgresql-mcp-server tables list --schema public --uri postgresql://localhost/mydb

# Describe table structure
postgresql-mcp-server tables describe users --schema public --uri postgresql://localhost/mydb

# Get table size
postgresql-mcp-server tables size orders --schema public --uri postgresql://localhost/mydb
```

### Query Commands

```bash
# Execute SELECT query
postgresql-mcp-server query execute "SELECT * FROM users WHERE status = 'active' LIMIT 10" --uri postgresql://localhost/mydb

# Get query execution plan
postgresql-mcp-server query explain "SELECT * FROM orders WHERE user_id = 123" --uri postgresql://localhost/mydb

# Get actual execution stats with EXPLAIN ANALYZE
postgresql-mcp-server query explain "SELECT * FROM large_table WHERE created_at > '2024-01-01'" --analyze --uri postgresql://localhost/mydb
```

### Analysis Commands

```bash
# Find tables that might need indexes (high sequential scans)
postgresql-mcp-server analyze indexes --uri postgresql://localhost/mydb

# Find bloated tables needing VACUUM
postgresql-mcp-server analyze bloat --uri postgresql://localhost/mydb

# Find slowest queries (requires pg_stat_statements extension)
postgresql-mcp-server analyze slow --limit 20 --uri postgresql://localhost/mydb
```

### Status/Monitoring Commands

```bash
# View current connections
postgresql-mcp-server status connections --uri postgresql://localhost/mydb

# Check for locks and blocked queries
postgresql-mcp-server status locks --uri postgresql://localhost/mydb

# Get replication status
postgresql-mcp-server status replication --uri postgresql://localhost/mydb
```

### MCP Server Commands

```bash
# Run with stdio transport (default, for desktop apps)
postgresql-mcp-server run --uri postgresql://localhost/mydb

# Run with HTTP transport
postgresql-mcp-server run --transport http --port-bind 8000 --uri postgresql://localhost/mydb

# Run with SSE transport
postgresql-mcp-server run --transport sse --host-bind 0.0.0.0 --port-bind 8080 --uri postgresql://localhost/mydb
```

### Global Options

All commands support these connection options:

```bash
--uri URI                  Full connection string (env: POSTGRES_URI, DATABASE_URL)
--host HOST               Database host (env: POSTGRES_HOST, default: localhost)
--port PORT               Database port (env: POSTGRES_PORT, default: 5432)
--database DATABASE       Database name (env: POSTGRES_DATABASE, default: postgres)
--user USER               Database user (env: POSTGRES_USER, default: postgres)
--password PASSWORD       Database password (env: POSTGRES_PASSWORD)
--sslmode MODE            SSL mode: disable, require, verify-full (env: POSTGRES_SSLMODE, default: prefer)
--timeout SECONDS         Query timeout in seconds (default: 30)
```

## Available MCP Tools

### Database Discovery Tools (6)

#### `list_databases`
List all databases with size, owner, and connection count.

```python
list_databases()
```

#### `list_schemas`
List all schemas in the database.

```python
list_schemas(database="mydb")  # optional
```

#### `list_tables`
List all tables in a schema with size and row estimates.

```python
list_tables(schema="public")
```

#### `list_views`
List all views in a schema with definitions.

```python
list_views(schema="public")
```

#### `get_table_info`
Get detailed column information for a table.

```python
get_table_info(table="users", schema="public")
```

#### `describe_table`
Get comprehensive table structure including columns and constraints.

```python
describe_table(table="orders", schema="public")
```

### Schema Inspection Tools (5)

#### `get_indexes`
List all indexes on a table with type, size, and columns.

```python
get_indexes(table="users", schema="public")
```

#### `get_constraints`
Get foreign keys, unique, check, and primary key constraints.

```python
get_constraints(table="orders", schema="public")
```

#### `get_table_size`
Get detailed size breakdown (table, indexes, total).

```python
get_table_size(table="large_table", schema="public")
```

#### `get_row_count`
Get fast estimate or exact count of table rows.

```python
# Fast estimate (uses statistics)
get_row_count(table="users", schema="public")

# Exact count (slower on large tables)
get_row_count(table="users", schema="public", exact=True)
```

#### `get_table_access_stats`
Get read/write patterns for a table from pg_stat_user_tables.

```python
get_table_access_stats(table="users", schema="public")
```

### Query Tools (3)

#### `execute_query`
Execute SELECT queries (write operations blocked).

```python
# Simple query
execute_query(query="SELECT * FROM users WHERE status = 'active'", limit=100)

# JOIN query
execute_query(query="SELECT u.name, COUNT(o.id) FROM users u LEFT JOIN orders o ON u.id = o.user_id GROUP BY u.name")
```

#### `explain_query`
Get query execution plan with EXPLAIN or EXPLAIN ANALYZE.

```python
# Get plan without execution
explain_query(query="SELECT * FROM users WHERE email = 'test@example.com'")

# Get actual execution statistics
explain_query(query="SELECT * FROM large_table WHERE indexed_col = 123", analyze=True)
```

#### `get_sample_data`
Get sample rows from a table for inspection.

```python
get_sample_data(table="users", schema="public", limit=10)
```

### Analysis Tools (5)

#### `find_missing_indexes`
Suggest indexes based on tables with high sequential scan ratios.

```python
find_missing_indexes()
```

Returns tables with high `seq_scan` vs `idx_scan` ratios, indicating missing indexes.

#### `find_unused_indexes`
Find indexes that are never used (candidates for removal).

```python
find_unused_indexes()
```

Returns indexes with `idx_scan = 0` that might be wasting space.

#### `find_bloated_tables`
Find tables with dead tuples needing VACUUM.

```python
find_bloated_tables()
```

Returns tables with high `n_dead_tup` count and bloat ratio.

#### `get_table_bloat`
Estimate bloat percentage for a specific table.

```python
get_table_bloat(table="users", schema="public")
```

#### `find_long_running_queries`
Find currently running queries exceeding duration threshold.

```python
# Find queries running > 60 seconds
find_long_running_queries(min_duration_seconds=60)

# Find queries running > 5 minutes
find_long_running_queries(min_duration_seconds=300)
```

### Monitoring Tools (5)

#### `get_database_stats`
Get pg_stat_database statistics (connections, transactions, blocks).

```python
# Current database
get_database_stats()

# Specific database
get_database_stats(database="mydb")
```

#### `get_connection_stats`
Get active connections grouped by state, database, and user.

```python
get_connection_stats()
```

Returns total connections, active, idle, idle-in-transaction counts.

#### `get_lock_info`
Get current locks and blocked queries (for deadlock diagnosis).

```python
get_lock_info()
```

Shows which queries are blocked and what's blocking them.

#### `get_replication_status`
Get streaming replication lag and status.

```python
get_replication_status()
```

Shows standby servers, replication state, and lag (primary only).

#### `get_cache_hit_ratio`
Get buffer cache hit ratio (target: >99%).

```python
get_cache_hit_ratio()
```

Returns percentage of data reads served from cache vs disk.

### Performance Tools (3)

#### `get_slow_queries`
Get slowest queries from pg_stat_statements (requires extension).

```python
# Top 10 slow queries
get_slow_queries(limit=10)

# Top 20 slow queries
get_slow_queries(limit=20)
```

**Note**: Requires `CREATE EXTENSION pg_stat_statements;`

#### `get_index_usage`
Get index scan vs sequential scan ratios for all tables.

```python
get_index_usage()
```

Returns index usage percentage per table to identify optimization opportunities.

#### `get_table_access_stats`
Get detailed read/write patterns per table.

```python
get_table_access_stats(table="users", schema="public")
```

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `POSTGRES_URI` or `DATABASE_URL` | Full connection string | - | No* |
| `POSTGRES_HOST` | Database host | `localhost` | No* |
| `POSTGRES_PORT` | Database port | `5432` | No* |
| `POSTGRES_DATABASE` | Database name | `postgres` | No* |
| `POSTGRES_USER` | Database user | `postgres` | No* |
| `POSTGRES_PASSWORD` | Database password | - | No* |
| `POSTGRES_SSLMODE` | SSL mode | `prefer` | No |
| `POSTGRES_TIMEOUT` | Query timeout (seconds) | `30` | No |

*Either `POSTGRES_URI` or individual connection parameters are required.

### Connection String Examples

```bash
# Local database
postgresql://localhost/mydb

# With credentials
postgresql://user:password@localhost:5432/mydb

# Remote with SSL
postgresql://user:password@db.example.com:5432/production?sslmode=require

# Unix socket
postgresql:///mydb?host=/var/run/postgresql
```

## Use Cases for AI Agents

### Schema Discovery
Ask: "What tables exist in the database?"
```
AI uses: list_tables(schema="public")
```

### Data Exploration
Ask: "Show me sample data from the users table"
```
AI uses:
1. get_table_info(table="users") - understand structure
2. get_sample_data(table="users", limit=10) - see sample data
```

### Performance Investigation
Ask: "Why is this query slow?"
```
AI uses:
1. explain_query(query="...", analyze=True) - get execution plan
2. get_indexes(table="users") - check existing indexes
3. find_missing_indexes() - see if indexes are needed
```

### Database Health Check
Ask: "Is the database healthy?"
```
AI uses:
1. get_connection_stats() - check connection load
2. get_cache_hit_ratio() - verify cache performance
3. find_bloated_tables() - check for maintenance needs
4. get_lock_info() - look for blocking queries
```

### Capacity Planning
Ask: "Which tables are largest?"
```
AI uses:
1. list_tables(schema="public") - see table sizes
2. get_table_size(table="large_table") - detailed size breakdown
3. find_bloated_tables() - identify reclaimable space
```

### Query Optimization
Ask: "How can I optimize this query?"
```
AI uses:
1. explain_query(query="...", analyze=True) - analyze execution
2. get_index_usage() - check if indexes are used
3. find_missing_indexes() - suggest new indexes
```

## Security & Safety

### Read-Only Guarantee

This MCP server is **strictly read-only**:

- ✅ **ALLOWED**: SELECT, EXPLAIN, SHOW, WITH queries
- ❌ **BLOCKED**: INSERT, UPDATE, DELETE, DROP, CREATE, ALTER, TRUNCATE, GRANT, REVOKE

### How It Works

1. **Transaction-Level Protection**: All connections use `SET TRANSACTION READ ONLY`
2. **Query Validation**: SQL is parsed and validated before execution
3. **Blocked Commands**: Write operations are explicitly blocked and throw errors

### Example: Blocked Operations

```python
# This will fail with error
execute_query("INSERT INTO users VALUES (...)")
# Error: Query contains blocked command: INSERT

# This will fail
execute_query("UPDATE users SET status = 'active'")
# Error: Query contains blocked command: UPDATE

# This works
execute_query("SELECT * FROM users")
# Success
```

## PostgreSQL Extensions

Some tools require PostgreSQL extensions:

### pg_stat_statements (for slow query analysis)

```sql
-- Enable extension (requires superuser)
CREATE EXTENSION pg_stat_statements;

-- Add to postgresql.conf
shared_preload_libraries = 'pg_stat_statements'

-- Restart PostgreSQL
-- Then use: get_slow_queries()
```

### Other Statistics Views

These are built-in and always available:
- `pg_stat_user_tables` - table access statistics
- `pg_stat_user_indexes` - index usage statistics
- `pg_statio_user_tables` - I/O statistics
- `pg_stat_database` - database-level statistics
- `pg_stat_activity` - current activity and connections
- `pg_stat_replication` - replication status

## Architecture

### Project Structure

```
postgresql-mcp-server/
├── src/
│   └── postgresql_mcp_server/
│       ├── __init__.py          # Package initialization
│       ├── __main__.py          # CLI entry point
│       ├── server.py            # FastMCP server setup
│       ├── cli.py               # Click-based CLI
│       ├── tools/
│       │   ├── __init__.py
│       │   └── registry.py      # All 27 MCP tool implementations
│       └── utils/
│           ├── __init__.py
│           ├── client.py        # PostgreSQL client wrapper (READ-ONLY)
│           └── helpers.py       # Formatting and utility functions
├── pyproject.toml               # Project configuration
├── README.md                    # This file
└── LICENSE                      # MIT License
```

### Technology Stack

- **MCP Framework**: FastMCP 2.0
- **Database Driver**: psycopg 3.1+ (binary)
- **Python**: 3.12+ with full type hints
- **CLI**: Click 8.1+
- **Read-Only**: Transaction-level and query validation

## CLI to MCP Tool Mapping

| CLI Command | MCP Tool | Description |
|------------|----------|-------------|
| `db list` | `list_databases` | List all databases |
| `db stats` | `get_database_stats` | Database statistics |
| `schema list` | `list_schemas` | List schemas |
| `tables list` | `list_tables` | List tables in schema |
| `tables describe` | `describe_table` | Table structure |
| `tables size` | `get_table_size` | Table size breakdown |
| `query execute` | `execute_query` | Run SELECT query |
| `query explain` | `explain_query` | Get execution plan |
| `analyze indexes` | `find_missing_indexes` | Suggest indexes |
| `analyze bloat` | `find_bloated_tables` | Find bloat |
| `analyze slow` | `get_slow_queries` | Slow queries |
| `status connections` | `get_connection_stats` | Connection stats |
| `status locks` | `get_lock_info` | Lock information |
| `status replication` | `get_replication_status` | Replication status |

## Development

### Setup Development Environment

```bash
# Clone repository
cd /path/to/postgresql-mcp-server

# Install with dev dependencies using uv
uv pip install -e ".[dev]"

# Or with pip
pip install -e ".[dev]"
```

### Code Quality

```bash
# Format and lint with ruff
uvx ruff check src/ --fix
uvx ruff format src/

# Type checking (if using mypy)
mypy src/
```

### Testing with Local PostgreSQL

```bash
# Run PostgreSQL locally with Docker
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres:16

# Test the MCP server
export POSTGRES_URI="postgresql://postgres:postgres@localhost:5432/postgres"
postgresql-mcp-server check
```

## Troubleshooting

### Connection Issues

```bash
# Test PostgreSQL connectivity directly
psql postgresql://user:password@localhost:5432/mydb

# Check with the MCP server
postgresql-mcp-server check --uri postgresql://user:password@localhost:5432/mydb
```

### SSL Certificate Issues

```bash
# Disable SSL verification (not recommended for production)
export POSTGRES_SSLMODE="disable"
postgresql-mcp-server check

# Or use command-line option
postgresql-mcp-server check --sslmode disable
```

### Permission Issues

The database user needs at least these permissions:
- `CONNECT` on database
- `USAGE` on schemas
- `SELECT` on tables/views

```sql
-- Grant read-only access
GRANT CONNECT ON DATABASE mydb TO readonly_user;
GRANT USAGE ON SCHEMA public TO readonly_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO readonly_user;

-- Auto-grant on future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT ON TABLES TO readonly_user;
```

### pg_stat_statements Not Available

```sql
-- Check if extension exists
SELECT * FROM pg_available_extensions WHERE name = 'pg_stat_statements';

-- Install extension (requires superuser)
CREATE EXTENSION pg_stat_statements;

-- Verify
SELECT * FROM pg_stat_statements LIMIT 1;
```

## Examples

### Example Queries for AI Agents

#### Find All Foreign Keys
```python
execute_query(query="""
    SELECT
        tc.table_schema, tc.table_name, kcu.column_name,
        ccu.table_name AS foreign_table_name,
        ccu.column_name AS foreign_column_name
    FROM information_schema.table_constraints AS tc
    JOIN information_schema.key_column_usage AS kcu
        ON tc.constraint_name = kcu.constraint_name
    JOIN information_schema.constraint_column_usage AS ccu
        ON ccu.constraint_name = tc.constraint_name
    WHERE tc.constraint_type = 'FOREIGN KEY'
""")
```

#### Find Large Tables Not Recently Vacuumed
```python
execute_query(query="""
    SELECT
        schemaname, tablename,
        pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
        last_vacuum, last_autovacuum,
        n_dead_tup
    FROM pg_stat_user_tables
    WHERE last_vacuum < NOW() - INTERVAL '7 days'
        OR last_vacuum IS NULL
    ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
""")
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure code passes `ruff` checks
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

- **Issues**: [GitHub Issues](https://github.com/msalah-eg/postgresql-mcp-server/issues)
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **MCP Documentation**: https://modelcontextprotocol.io/

## Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp)
- Follows [Model Context Protocol](https://modelcontextprotocol.io/) specification
- Inspired by the PostgreSQL community's excellent documentation
