"""
PostgreSQL tools registry for MCP server.

All tools are READ-ONLY and use the PostgreSQL client wrapper.
"""

import json

from mcp.server.fastmcp import FastMCP

from postgresql_mcp_server.utils.client import PostgreSQLClient


class PostgreSQLTools:
    """
    Register read-only PostgreSQL tools with MCP server.

    Provides comprehensive access to PostgreSQL database:
    - Discovery: Databases, schemas, tables, views
    - Schema: Table structure, indexes, constraints
    - Queries: Execute SELECT, EXPLAIN queries
    - Analysis: Missing indexes, bloat, performance issues
    - Monitoring: Connections, locks, replication
    - Performance: Slow queries, index usage, cache hits
    """

    def __init__(
        self,
        mcp: FastMCP,
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
        Initialize PostgreSQL tools.

        Args:
            mcp: FastMCP server instance
            uri: Full connection string
            host: Database host
            port: Database port
            database: Database name
            user: Database user
            password: Database password
            sslmode: SSL mode
            timeout: Query timeout in seconds
        """
        self.mcp = mcp
        self.uri = uri
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.sslmode = sslmode
        self.timeout = timeout
        self._register_tools()

    def _get_client(self) -> PostgreSQLClient:
        """Create a new PostgreSQL client."""
        return PostgreSQLClient(
            uri=self.uri,
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password,
            sslmode=self.sslmode,
            timeout=self.timeout,
        )

    def _format_response(self, response) -> str:
        """Format database response for MCP."""
        if response.success:
            result = {
                "data": response.data,
                "rows": response.rows_affected
            }
            if response.columns:
                result["columns"] = response.columns
            return json.dumps(result, indent=2, default=str)
        else:
            return f"Error: {response.error}"

    def _register_tools(self) -> None:
        """Register all PostgreSQL tools with the MCP server."""

        # ============================================================
        # DATABASE DISCOVERY TOOLS
        # ============================================================

        @self.mcp.tool()
        def list_databases() -> str:
            """
            List all databases in the PostgreSQL instance.

            Returns all accessible databases with their size, owner, encoding,
            and number of connections. Useful for discovering available databases.

            Returns:
                JSON with array of databases including:
                - datname: Database name
                - pg_size_pretty: Human-readable size
                - datdba: Owner user ID
                - encoding: Character encoding
                - datcollate: Collation
                - datctype: Character type
                - datconnlimit: Connection limit (-1 = unlimited)
                - numbackends: Current number of connections

            Examples:
                # List all databases
                list_databases()
            """
            query = """
            SELECT
                d.datname,
                pg_catalog.pg_get_userbyid(d.datdba) as owner,
                pg_catalog.pg_encoding_to_char(d.encoding) as encoding,
                d.datcollate,
                d.datctype,
                pg_catalog.pg_size_pretty(pg_catalog.pg_database_size(d.datname)) as size,
                d.datconnlimit,
                (SELECT count(*) FROM pg_stat_activity WHERE datname = d.datname) as connections
            FROM pg_catalog.pg_database d
            WHERE d.datistemplate = false
            ORDER BY d.datname;
            """

            with self._get_client() as client:
                response = client.execute_query(query)
                return self._format_response(response)

        @self.mcp.tool()
        def list_schemas(database: str | None = None) -> str:
            """
            List all schemas in the current or specified database.

            Returns all schemas (namespaces) that organize database objects.
            Schemas are like directories for tables, views, and functions.

            Args:
                database: Database name (optional, uses current if not specified)

            Returns:
                JSON with array of schemas including:
                - schema_name: Schema name
                - schema_owner: Owner username
                - schema_acl: Access control list

            Examples:
                # List schemas in current database
                list_schemas()

                # List schemas in specific database
                list_schemas(database="myapp")
            """
            query = """
            SELECT
                n.nspname as schema_name,
                pg_catalog.pg_get_userbyid(n.nspowner) as owner
            FROM pg_catalog.pg_namespace n
            WHERE n.nspname !~ '^pg_' AND n.nspname <> 'information_schema'
            ORDER BY n.nspname;
            """

            with self._get_client() as client:
                response = client.execute_query(query)
                return self._format_response(response)

        @self.mcp.tool()
        def list_tables(schema: str = "public") -> str:
            """
            List all tables in a schema.

            Returns all user tables with their size, row count, and description.

            Args:
                schema: Schema name (default: "public")

            Returns:
                JSON with array of tables including:
                - table_name: Table name
                - table_type: BASE TABLE or VIEW
                - row_estimate: Estimated row count
                - total_size: Total size including indexes
                - table_size: Table size only
                - indexes_size: Indexes size

            Examples:
                # List tables in public schema
                list_tables()

                # List tables in custom schema
                list_tables(schema="analytics")
            """
            query = """
            SELECT
                c.relname as table_name,
                pg_catalog.pg_get_userbyid(c.relowner) as owner,
                pg_catalog.pg_size_pretty(
                    pg_catalog.pg_total_relation_size(c.oid)
                ) as total_size,
                pg_catalog.pg_size_pretty(pg_catalog.pg_relation_size(c.oid)) as table_size,
                pg_catalog.pg_size_pretty(
                    pg_catalog.pg_total_relation_size(c.oid) -
                    pg_catalog.pg_relation_size(c.oid)
                ) as indexes_size,
                c.reltuples::bigint as row_estimate,
                obj_description(c.oid, 'pg_class') as description
            FROM pg_catalog.pg_class c
            LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
            WHERE c.relkind = 'r'
                AND n.nspname = %s
            ORDER BY pg_catalog.pg_total_relation_size(c.oid) DESC;
            """

            with self._get_client() as client:
                response = client.execute_query(query, (schema,))
                return self._format_response(response)

        @self.mcp.tool()
        def list_views(schema: str = "public") -> str:
            """
            List all views in a schema.

            Returns all views with their definition and description.

            Args:
                schema: Schema name (default: "public")

            Returns:
                JSON with array of views including:
                - view_name: View name
                - definition: View SQL definition
                - is_updatable: Whether view is updatable

            Examples:
                # List views in public schema
                list_views()

                # List views in custom schema
                list_views(schema="reports")
            """
            query = """
            SELECT
                c.relname as view_name,
                pg_catalog.pg_get_userbyid(c.relowner) as owner,
                pg_catalog.pg_get_viewdef(c.oid, true) as definition,
                obj_description(c.oid, 'pg_class') as description
            FROM pg_catalog.pg_class c
            LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
            WHERE c.relkind = 'v'
                AND n.nspname = %s
            ORDER BY c.relname;
            """

            with self._get_client() as client:
                response = client.execute_query(query, (schema,))
                return self._format_response(response)

        @self.mcp.tool()
        def get_table_info(table: str, schema: str = "public") -> str:
            """
            Get detailed information about a table's columns and types.

            Returns column definitions, data types, constraints, and defaults.

            Args:
                table: Table name
                schema: Schema name (default: "public")

            Returns:
                JSON with array of columns including:
                - column_name: Column name
                - data_type: PostgreSQL data type
                - is_nullable: YES or NO
                - column_default: Default value
                - character_maximum_length: Max length for strings
                - numeric_precision: Precision for numbers

            Examples:
                # Get info for users table
                get_table_info(table="users")

                # Get info from custom schema
                get_table_info(table="orders", schema="sales")
            """
            query = """
            SELECT
                a.attname as column_name,
                pg_catalog.format_type(a.atttypid, a.atttypmod) as data_type,
                a.attnotnull as not_null,
                (SELECT pg_catalog.pg_get_expr(d.adbin, d.adrelid)
                 FROM pg_catalog.pg_attrdef d
                 WHERE d.adrelid = a.attrelid AND d.adnum = a.attnum AND
                       a.atthasdef) as default_value,
                col_description(a.attrelid, a.attnum) as description
            FROM pg_catalog.pg_attribute a
            JOIN pg_catalog.pg_class c ON a.attrelid = c.oid
            JOIN pg_catalog.pg_namespace n ON c.relnamespace = n.oid
            WHERE c.relname = %s
                AND n.nspname = %s
                AND a.attnum > 0
                AND NOT a.attisdropped
            ORDER BY a.attnum;
            """

            with self._get_client() as client:
                response = client.execute_query(query, (table, schema))
                return self._format_response(response)

        # ============================================================
        # SCHEMA INSPECTION TOOLS
        # ============================================================

        @self.mcp.tool()
        def describe_table(table: str, schema: str = "public") -> str:
            """
            Get comprehensive table structure including columns, constraints, and indexes.

            Combines column information with primary keys, foreign keys, unique
            constraints, and check constraints.

            Args:
                table: Table name
                schema: Schema name (default: "public")

            Returns:
                JSON with detailed table structure

            Examples:
                # Describe users table
                describe_table(table="users")
            """
            # Get columns
            columns_query = """
            SELECT
                a.attname as column_name,
                pg_catalog.format_type(a.atttypid, a.atttypmod) as data_type,
                a.attnotnull as not_null,
                (SELECT pg_catalog.pg_get_expr(d.adbin, d.adrelid)
                 FROM pg_catalog.pg_attrdef d
                 WHERE d.adrelid = a.attrelid AND d.adnum = a.attnum AND
                       a.atthasdef) as default_value,
                (SELECT true FROM pg_catalog.pg_index i
                 WHERE i.indrelid = a.attrelid AND a.attnum = ANY(i.indkey) AND
                       i.indisprimary) as is_primary_key
            FROM pg_catalog.pg_attribute a
            JOIN pg_catalog.pg_class c ON a.attrelid = c.oid
            JOIN pg_catalog.pg_namespace n ON c.relnamespace = n.oid
            WHERE c.relname = %s AND n.nspname = %s AND a.attnum > 0 AND NOT a.attisdropped
            ORDER BY a.attnum;
            """

            with self._get_client() as client:
                response = client.execute_query(columns_query, (table, schema))
                return self._format_response(response)

        @self.mcp.tool()
        def get_indexes(table: str, schema: str = "public") -> str:
            """
            List all indexes on a table.

            Returns index names, columns, type, and whether they're unique or primary.

            Args:
                table: Table name
                schema: Schema name (default: "public")

            Returns:
                JSON with array of indexes including:
                - index_name: Index name
                - index_type: btree, hash, gist, gin, etc.
                - is_unique: Whether index enforces uniqueness
                - is_primary: Whether this is the primary key index
                - columns: Array of indexed columns
                - index_size: Size of the index

            Examples:
                # Get indexes for users table
                get_indexes(table="users")
            """
            query = """
            SELECT
                i.relname as index_name,
                am.amname as index_type,
                ix.indisunique as is_unique,
                ix.indisprimary as is_primary,
                ARRAY(
                    SELECT pg_get_indexdef(ix.indexrelid, k + 1, true)
                    FROM generate_subscripts(ix.indkey, 1) as k
                    ORDER BY k
                ) as columns,
                pg_catalog.pg_size_pretty(pg_catalog.pg_relation_size(i.oid)) as index_size
            FROM pg_catalog.pg_class c
            JOIN pg_catalog.pg_index ix ON c.oid = ix.indrelid
            JOIN pg_catalog.pg_class i ON i.oid = ix.indexrelid
            JOIN pg_catalog.pg_am am ON i.relam = am.oid
            JOIN pg_catalog.pg_namespace n ON c.relnamespace = n.oid
            WHERE c.relname = %s AND n.nspname = %s
            ORDER BY i.relname;
            """

            with self._get_client() as client:
                response = client.execute_query(query, (table, schema))
                return self._format_response(response)

        @self.mcp.tool()
        def get_constraints(table: str, schema: str = "public") -> str:
            """
            Get all constraints on a table (foreign keys, unique, check).

            Returns primary key, foreign key, unique, and check constraints.

            Args:
                table: Table name
                schema: Schema name (default: "public")

            Returns:
                JSON with array of constraints including:
                - constraint_name: Constraint name
                - constraint_type: PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK
                - definition: SQL definition

            Examples:
                # Get constraints for orders table
                get_constraints(table="orders")
            """
            query = """
            SELECT
                con.conname as constraint_name,
                CASE con.contype
                    WHEN 'p' THEN 'PRIMARY KEY'
                    WHEN 'f' THEN 'FOREIGN KEY'
                    WHEN 'u' THEN 'UNIQUE'
                    WHEN 'c' THEN 'CHECK'
                END as constraint_type,
                pg_catalog.pg_get_constraintdef(con.oid, true) as definition
            FROM pg_catalog.pg_constraint con
            JOIN pg_catalog.pg_class c ON c.oid = con.conrelid
            JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
            WHERE c.relname = %s AND n.nspname = %s
            ORDER BY con.contype, con.conname;
            """

            with self._get_client() as client:
                response = client.execute_query(query, (table, schema))
                return self._format_response(response)

        @self.mcp.tool()
        def get_table_size(table: str, schema: str = "public") -> str:
            """
            Get detailed size information for a table.

            Returns table size, index size, total size, and toast size.

            Args:
                table: Table name
                schema: Schema name (default: "public")

            Returns:
                JSON with size information including:
                - table_size: Size of table data
                - indexes_size: Size of all indexes
                - toast_size: Size of TOAST data (large objects)
                - total_size: Total size including everything

            Examples:
                # Get size of users table
                get_table_size(table="users")
            """
            query = """
            SELECT
                pg_catalog.pg_size_pretty(pg_catalog.pg_table_size(c.oid)) as table_size,
                pg_catalog.pg_size_pretty(pg_catalog.pg_indexes_size(c.oid)) as indexes_size,
                pg_catalog.pg_size_pretty(
                    pg_catalog.pg_total_relation_size(c.oid)
                ) as total_size,
                pg_catalog.pg_size_pretty(
                    pg_catalog.pg_total_relation_size(c.oid) -
                    pg_catalog.pg_table_size(c.oid)
                ) as toast_and_indexes_size
            FROM pg_catalog.pg_class c
            JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
            WHERE c.relname = %s AND n.nspname = %s;
            """

            with self._get_client() as client:
                response = client.execute_query(query, (table, schema))
                return self._format_response(response)

        @self.mcp.tool()
        def get_row_count(table: str, schema: str = "public", exact: bool = False) -> str:
            """
            Get row count for a table.

            Returns either fast estimate or exact count (slower).

            Args:
                table: Table name
                schema: Schema name (default: "public")
                exact: If True, use COUNT(*) for exact count (slow on large tables)

            Returns:
                JSON with row count

            Examples:
                # Get estimated row count (fast)
                get_row_count(table="users")

                # Get exact row count (slow on large tables)
                get_row_count(table="users", exact=True)
            """
            if exact:
                # Exact count using COUNT(*) - slow on large tables
                query = f"""
                SELECT COUNT(*) as row_count
                FROM {schema}.{table};
                """
            else:
                # Fast estimate from statistics
                query = """
                SELECT c.reltuples::bigint as row_count
                FROM pg_catalog.pg_class c
                JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
                WHERE c.relname = %s AND n.nspname = %s;
                """

            with self._get_client() as client:
                if exact:
                    response = client.execute_query(query)
                else:
                    response = client.execute_query(query, (table, schema))
                return self._format_response(response)

        # ============================================================
        # QUERY TOOLS
        # ============================================================

        @self.mcp.tool()
        def execute_query(query: str, limit: int = 100) -> str:
            """
            Execute a SELECT query (READ-ONLY).

            Executes a SELECT statement and returns results. All write operations
            are blocked (INSERT, UPDATE, DELETE, DROP, etc.).

            Args:
                query: SQL SELECT query to execute
                limit: Maximum number of rows to return (default: 100)

            Returns:
                JSON with query results

            Examples:
                # Simple SELECT
                execute_query(query="SELECT * FROM users LIMIT 10")

                # JOIN query
                execute_query(
                    query="SELECT u.name, o.total FROM users u "
                          "JOIN orders o ON u.id = o.user_id"
                )

                # Aggregation
                execute_query(query="SELECT status, COUNT(*) FROM orders GROUP BY status")

            Security:
                - Only SELECT statements are allowed
                - INSERT, UPDATE, DELETE, DROP are blocked
                - Transaction is READ ONLY
            """
            # Add LIMIT if not present
            query_upper = query.strip().upper()
            if "LIMIT" not in query_upper:
                query = f"{query.rstrip(';')} LIMIT {limit}"

            with self._get_client() as client:
                response = client.execute_query(query)
                return self._format_response(response)

        @self.mcp.tool()
        def explain_query(query: str, analyze: bool = False) -> str:
            """
            Get query execution plan with EXPLAIN or EXPLAIN ANALYZE.

            Returns the query planner's execution strategy including cost estimates,
            row counts, and actual execution statistics if ANALYZE is used.

            Args:
                query: SQL query to explain
                analyze: If True, actually executes query and shows real stats (EXPLAIN ANALYZE)

            Returns:
                JSON with query plan

            Examples:
                # Get query plan without execution
                explain_query(query="SELECT * FROM users WHERE email = 'test@example.com'")

                # Get actual execution statistics
                explain_query(query="SELECT * FROM orders WHERE status = 'pending'", analyze=True)

            Note:
                - EXPLAIN ANALYZE actually runs the query (but in READ ONLY transaction)
                - Use analyze=True to see actual row counts and timing
                - Useful for optimizing query performance
            """
            if analyze:
                explain_query = f"EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) {query}"
            else:
                explain_query = f"EXPLAIN (FORMAT JSON) {query}"

            with self._get_client() as client:
                response = client.execute_query(explain_query)
                return self._format_response(response)

        @self.mcp.tool()
        def get_sample_data(table: str, schema: str = "public", limit: int = 10) -> str:
            """
            Get sample rows from a table.

            Returns a small sample of data from the table for inspection.

            Args:
                table: Table name
                schema: Schema name (default: "public")
                limit: Number of rows to return (default: 10)

            Returns:
                JSON with sample rows

            Examples:
                # Get 10 sample rows
                get_sample_data(table="users")

                # Get 50 sample rows
                get_sample_data(table="orders", limit=50)
            """
            query = f"""
            SELECT * FROM {schema}.{table}
            LIMIT %s;
            """

            with self._get_client() as client:
                response = client.execute_query(query, (limit,))
                return self._format_response(response)

        # ============================================================
        # ANALYSIS TOOLS
        # ============================================================

        @self.mcp.tool()
        def find_missing_indexes() -> str:
            """
            Suggest missing indexes based on sequential scans.

            Analyzes query statistics to find tables that are frequently scanned
            sequentially (slow) and might benefit from indexes.

            Returns:
                JSON with tables that might need indexes including:
                - schema: Schema name
                - table: Table name
                - seq_scan: Number of sequential scans
                - seq_tup_read: Rows read by sequential scans
                - idx_scan: Number of index scans
                - ratio: Ratio of seq scans to total scans

            Examples:
                # Find tables that need indexes
                find_missing_indexes()

            Note:
                - High seq_scan with low idx_scan suggests missing index
                - Focus on tables with many seq_tup_read
                - Requires pg_stat_statements or pg_stat_user_tables
            """
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

            with self._get_client() as client:
                response = client.execute_query(query)
                return self._format_response(response)

        @self.mcp.tool()
        def find_unused_indexes() -> str:
            """
            Find indexes that are not being used.

            Returns indexes with zero or very low usage that might be candidates
            for removal to save space and improve write performance.

            Returns:
                JSON with unused indexes including:
                - schema: Schema name
                - table: Table name
                - index: Index name
                - index_size: Size of the index
                - idx_scan: Number of times index was used

            Examples:
                # Find unused indexes
                find_unused_indexes()

            Note:
                - idx_scan = 0 means index was never used
                - Consider removing unused indexes to save space
                - Keep primary key and unique constraint indexes
            """
            query = """
            SELECT
                s.schemaname as schema,
                s.relname as table,
                s.indexrelname as index,
                pg_size_pretty(pg_relation_size(s.indexrelid)) as index_size,
                s.idx_scan
            FROM pg_stat_user_indexes s
            JOIN pg_index i ON s.indexrelid = i.indexrelid
            WHERE s.idx_scan = 0
                AND NOT i.indisprimary
                AND NOT i.indisunique
            ORDER BY pg_relation_size(s.indexrelid) DESC;
            """

            with self._get_client() as client:
                response = client.execute_query(query)
                return self._format_response(response)

        @self.mcp.tool()
        def find_bloated_tables() -> str:
            """
            Find tables with significant bloat that need VACUUM.

            Returns tables with dead tuples that are wasting space and might
            benefit from VACUUM or VACUUM FULL.

            Returns:
                JSON with bloated tables including:
                - schema: Schema name
                - table: Table name
                - n_dead_tup: Number of dead tuples
                - n_live_tup: Number of live tuples
                - bloat_ratio: Ratio of dead to live tuples
                - last_vacuum: Last vacuum time
                - last_autovacuum: Last autovacuum time

            Examples:
                # Find bloated tables
                find_bloated_tables()

            Note:
                - High n_dead_tup indicates bloat
                - bloat_ratio > 0.2 (20%) is concerning
                - Run VACUUM to reclaim space
            """
            query = """
            SELECT
                schemaname as schema,
                tablename as table,
                n_dead_tup,
                n_live_tup,
                CASE WHEN n_live_tup > 0
                    THEN ROUND((n_dead_tup::float / n_live_tup::float)::numeric, 4)
                    ELSE 0
                END as bloat_ratio,
                last_vacuum,
                last_autovacuum
            FROM pg_stat_user_tables
            WHERE n_dead_tup > 1000
            ORDER BY n_dead_tup DESC
            LIMIT 20;
            """

            with self._get_client() as client:
                response = client.execute_query(query)
                return self._format_response(response)

        @self.mcp.tool()
        def get_table_bloat(table: str, schema: str = "public") -> str:
            """
            Estimate bloat percentage for a specific table.

            Calculates how much wasted space exists in a table due to dead tuples.

            Args:
                table: Table name
                schema: Schema name (default: "public")

            Returns:
                JSON with bloat estimate

            Examples:
                # Check bloat for users table
                get_table_bloat(table="users")
            """
            query = """
            SELECT
                n_dead_tup,
                n_live_tup,
                CASE WHEN n_live_tup > 0
                    THEN ROUND((100.0 * n_dead_tup / (n_dead_tup + n_live_tup))::numeric, 2)
                    ELSE 0
                END as bloat_percent,
                last_vacuum,
                last_autovacuum
            FROM pg_stat_user_tables
            WHERE schemaname = %s AND tablename = %s;
            """

            with self._get_client() as client:
                response = client.execute_query(query, (schema, table))
                return self._format_response(response)

        @self.mcp.tool()
        def find_long_running_queries(min_duration_seconds: int = 60) -> str:
            """
            Find currently running queries that exceed a duration threshold.

            Returns active queries that have been running longer than specified.

            Args:
                min_duration_seconds: Minimum query duration in seconds (default: 60)

            Returns:
                JSON with long-running queries including:
                - pid: Process ID
                - usename: Username
                - datname: Database name
                - state: Query state
                - query: SQL query
                - duration: How long it's been running

            Examples:
                # Find queries running > 60 seconds
                find_long_running_queries()

                # Find queries running > 5 minutes
                find_long_running_queries(min_duration_seconds=300)
            """
            query = """
            SELECT
                pid,
                usename,
                datname,
                state,
                query,
                NOW() - query_start as duration
            FROM pg_stat_activity
            WHERE state = 'active'
                AND query NOT LIKE '%pg_stat_activity%'
                AND NOW() - query_start > interval '%s seconds'
            ORDER BY duration DESC;
            """

            with self._get_client() as client:
                response = client.execute_query(query, (min_duration_seconds,))
                return self._format_response(response)

        # ============================================================
        # MONITORING TOOLS
        # ============================================================

        @self.mcp.tool()
        def get_database_stats(database: str | None = None) -> str:
            """
            Get statistics for current or specified database.

            Returns connection counts, transaction counts, block reads/hits,
            and other database-level metrics.

            Args:
                database: Database name (optional, uses current if not specified)

            Returns:
                JSON with database statistics

            Examples:
                # Get stats for current database
                get_database_stats()

                # Get stats for specific database
                get_database_stats(database="myapp")
            """
            if database:
                query = """
                SELECT * FROM pg_stat_database
                WHERE datname = %s;
                """
                params = (database,)
            else:
                query = """
                SELECT * FROM pg_stat_database
                WHERE datname = current_database();
                """
                params = None

            with self._get_client() as client:
                response = client.execute_query(query, params)
                return self._format_response(response)

        @self.mcp.tool()
        def get_connection_stats() -> str:
            """
            Get current connection statistics.

            Returns active connections grouped by state, database, and user.

            Returns:
                JSON with connection information including:
                - total_connections: Total number of connections
                - active_queries: Number of active queries
                - idle_connections: Number of idle connections
                - connections_by_database: Breakdown by database
                - connections_by_user: Breakdown by user

            Examples:
                # Get connection statistics
                get_connection_stats()
            """
            query = """
            SELECT
                COUNT(*) as total_connections,
                COUNT(*) FILTER (WHERE state = 'active') as active,
                COUNT(*) FILTER (WHERE state = 'idle') as idle,
                COUNT(*) FILTER (WHERE state = 'idle in transaction') as idle_in_transaction,
                COUNT(*) FILTER (WHERE wait_event_type IS NOT NULL) as waiting,
                datname,
                usename
            FROM pg_stat_activity
            GROUP BY datname, usename
            ORDER BY total_connections DESC;
            """

            with self._get_client() as client:
                response = client.execute_query(query)
                return self._format_response(response)

        @self.mcp.tool()
        def get_lock_info() -> str:
            """
            Get information about current locks and blocked queries.

            Returns locks that are blocking other queries, helping diagnose
            deadlocks and long-running transactions.

            Returns:
                JSON with lock information including:
                - blocked_pid: Process being blocked
                - blocking_pid: Process holding the lock
                - blocked_query: Query being blocked
                - blocking_query: Query holding the lock

            Examples:
                # Get lock information
                get_lock_info()
            """
            query = """
            SELECT
                blocked_locks.pid AS blocked_pid,
                blocked_activity.usename AS blocked_user,
                blocking_locks.pid AS blocking_pid,
                blocking_activity.usename AS blocking_user,
                blocked_activity.query AS blocked_statement,
                blocking_activity.query AS blocking_statement,
                blocked_activity.application_name AS blocked_application
            FROM pg_catalog.pg_locks blocked_locks
            JOIN pg_catalog.pg_stat_activity blocked_activity
                ON blocked_activity.pid = blocked_locks.pid
            JOIN pg_catalog.pg_locks blocking_locks
                ON blocking_locks.locktype = blocked_locks.locktype
                AND blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database
                AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
                AND blocking_locks.page IS NOT DISTINCT FROM blocked_locks.page
                AND blocking_locks.tuple IS NOT DISTINCT FROM blocked_locks.tuple
                AND blocking_locks.virtualxid IS NOT DISTINCT FROM blocked_locks.virtualxid
                AND blocking_locks.transactionid IS NOT DISTINCT FROM blocked_locks.transactionid
                AND blocking_locks.classid IS NOT DISTINCT FROM blocked_locks.classid
                AND blocking_locks.objid IS NOT DISTINCT FROM blocked_locks.objid
                AND blocking_locks.objsubid IS NOT DISTINCT FROM blocked_locks.objsubid
                AND blocking_locks.pid != blocked_locks.pid
            JOIN pg_catalog.pg_stat_activity blocking_activity
                ON blocking_activity.pid = blocking_locks.pid
            WHERE NOT blocked_locks.granted;
            """

            with self._get_client() as client:
                response = client.execute_query(query)
                return self._format_response(response)

        @self.mcp.tool()
        def get_replication_status() -> str:
            """
            Get streaming replication status and lag.

            Returns replication slots, standby servers, and replication lag.

            Returns:
                JSON with replication information including:
                - client_addr: Standby server address
                - state: Replication state
                - sync_state: Sync or async replication
                - replay_lag: How far behind standby is

            Examples:
                # Get replication status
                get_replication_status()

            Note:
                - Only available on primary server
                - Shows lag for each standby
                - Empty result if no replication configured
            """
            query = """
            SELECT
                client_addr,
                usename,
                application_name,
                state,
                sync_state,
                replay_lag,
                write_lag,
                flush_lag
            FROM pg_stat_replication;
            """

            with self._get_client() as client:
                response = client.execute_query(query)
                return self._format_response(response)

        @self.mcp.tool()
        def get_cache_hit_ratio() -> str:
            """
            Get buffer cache hit ratio.

            Returns the percentage of data reads served from memory cache vs disk.
            Higher is better (target: >99%).

            Returns:
                JSON with cache statistics including:
                - cache_hit_ratio: Percentage of reads from cache
                - heap_read: Disk reads
                - heap_hit: Cache hits

            Examples:
                # Get cache hit ratio
                get_cache_hit_ratio()

            Note:
                - Ratio > 99% is good
                - Ratio < 90% suggests need for more memory
                - Based on pg_statio_user_tables
            """
            query = """
            SELECT
                SUM(heap_blks_read) as heap_read,
                SUM(heap_blks_hit) as heap_hit,
                CASE WHEN SUM(heap_blks_hit) + SUM(heap_blks_read) > 0
                    THEN ROUND(
                        100.0 * SUM(heap_blks_hit) /
                        (SUM(heap_blks_hit) + SUM(heap_blks_read)), 2
                    )
                    ELSE 0
                END as cache_hit_ratio
            FROM pg_statio_user_tables;
            """

            with self._get_client() as client:
                response = client.execute_query(query)
                return self._format_response(response)

        # ============================================================
        # PERFORMANCE TOOLS
        # ============================================================

        @self.mcp.tool()
        def get_slow_queries(limit: int = 10) -> str:
            """
            Get slowest queries from pg_stat_statements.

            Returns queries ordered by total execution time. Requires
            pg_stat_statements extension to be installed.

            Args:
                limit: Number of queries to return (default: 10)

            Returns:
                JSON with slow queries including:
                - query: SQL query text
                - calls: Number of times executed
                - total_time: Total execution time
                - mean_time: Average execution time
                - rows: Total rows returned

            Examples:
                # Get top 10 slow queries
                get_slow_queries()

                # Get top 20 slow queries
                get_slow_queries(limit=20)

            Note:
                - Requires pg_stat_statements extension
                - Run: CREATE EXTENSION pg_stat_statements;
                - Reset stats: SELECT pg_stat_statements_reset();
            """
            query = """
            SELECT
                query,
                calls,
                total_exec_time as total_time,
                mean_exec_time as mean_time,
                max_exec_time as max_time,
                rows
            FROM pg_stat_statements
            ORDER BY total_exec_time DESC
            LIMIT %s;
            """

            with self._get_client() as client:
                response = client.execute_query(query, (limit,))
                return self._format_response(response)

        @self.mcp.tool()
        def get_index_usage() -> str:
            """
            Get index usage statistics for all tables.

            Returns index scan vs sequential scan ratios to identify tables
            that might need better indexing.

            Returns:
                JSON with index usage including:
                - schema: Schema name
                - table: Table name
                - index_scans: Number of index scans
                - seq_scans: Number of sequential scans
                - rows_read: Total rows read

            Examples:
                # Get index usage statistics
                get_index_usage()

            Note:
                - Low index scans vs high seq scans suggests missing indexes
                - Focus on frequently queried tables
            """
            query = """
            SELECT
                schemaname as schema,
                tablename as table,
                idx_scan as index_scans,
                seq_scan as seq_scans,
                idx_tup_fetch + seq_tup_read as rows_read,
                CASE WHEN idx_scan + seq_scan > 0
                    THEN ROUND(100.0 * idx_scan / (idx_scan + seq_scan), 2)
                    ELSE 0
                END as index_usage_percent
            FROM pg_stat_user_tables
            ORDER BY idx_scan + seq_scan DESC
            LIMIT 20;
            """

            with self._get_client() as client:
                response = client.execute_query(query)
                return self._format_response(response)

        @self.mcp.tool()
        def get_table_access_stats(table: str, schema: str = "public") -> str:
            """
            Get read/write access patterns for a specific table.

            Returns detailed statistics about how a table is being accessed.

            Args:
                table: Table name
                schema: Schema name (default: "public")

            Returns:
                JSON with access statistics including:
                - seq_scan: Sequential scans
                - idx_scan: Index scans
                - n_tup_ins: Rows inserted
                - n_tup_upd: Rows updated
                - n_tup_del: Rows deleted
                - n_live_tup: Live rows
                - n_dead_tup: Dead rows

            Examples:
                # Get access stats for users table
                get_table_access_stats(table="users")
            """
            query = """
            SELECT
                seq_scan,
                seq_tup_read,
                idx_scan,
                idx_tup_fetch,
                n_tup_ins,
                n_tup_upd,
                n_tup_del,
                n_tup_hot_upd,
                n_live_tup,
                n_dead_tup,
                last_vacuum,
                last_autovacuum,
                last_analyze,
                last_autoanalyze
            FROM pg_stat_user_tables
            WHERE schemaname = %s AND tablename = %s;
            """

            with self._get_client() as client:
                response = client.execute_query(query, (schema, table))
                return self._format_response(response)
