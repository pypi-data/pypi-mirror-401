"""Helper utilities for PostgreSQL MCP server."""

import json
from typing import Any


def format_bytes(bytes_value: int | None) -> str:
    """
    Format bytes to human-readable size.

    Args:
        bytes_value: Size in bytes

    Returns:
        Human-readable size (e.g., "1.5 GB", "256 MB")
    """
    if bytes_value is None:
        return "N/A"

    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_value < 1024:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024
    return f"{bytes_value:.2f} PB"


def format_table_result(data: list[dict[str, Any]], max_rows: int = 100) -> str:
    """
    Format query results as a readable table.

    Args:
        data: List of row dictionaries
        max_rows: Maximum number of rows to display

    Returns:
        Formatted table string
    """
    if not data:
        return "No results"

    # Limit rows
    limited_data = data[:max_rows]
    has_more = len(data) > max_rows

    # Get column names
    columns = list(limited_data[0].keys()) if limited_data else []

    # Calculate column widths
    widths = {col: len(col) for col in columns}
    for row in limited_data:
        for col in columns:
            val = str(row.get(col, ""))
            widths[col] = max(widths[col], len(val))

    # Build header
    header = " | ".join(col.ljust(widths[col]) for col in columns)
    separator = "-+-".join("-" * widths[col] for col in columns)

    # Build rows
    rows = []
    for row in limited_data:
        row_str = " | ".join(
            str(row.get(col, "")).ljust(widths[col])
            for col in columns
        )
        rows.append(row_str)

    result = f"{header}\n{separator}\n" + "\n".join(rows)

    if has_more:
        result += f"\n\n... and {len(data) - max_rows} more rows"

    return result


def format_json_result(data: Any) -> str:
    """
    Format data as JSON.

    Args:
        data: Data to format

    Returns:
        JSON string
    """
    return json.dumps(data, indent=2, default=str)


def sanitize_identifier(identifier: str) -> str:
    """
    Sanitize SQL identifier (table/column name).

    Args:
        identifier: SQL identifier

    Returns:
        Sanitized identifier

    Raises:
        ValueError: If identifier contains invalid characters
    """
    # Allow alphanumeric, underscore, and dollar sign
    import re
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_$]*$', identifier):
        raise ValueError(
            f"Invalid identifier: {identifier}. "
            f"Must start with letter/underscore and contain only alphanumeric/underscore/dollar."
        )
    return identifier


def build_safe_query(template: str, **kwargs: Any) -> str:
    """
    Build SQL query from template with safe substitution.

    Args:
        template: SQL template with {placeholders}
        **kwargs: Values to substitute

    Returns:
        SQL query with substituted values
    """
    # Sanitize all identifiers
    sanitized = {}
    for key, value in kwargs.items():
        if isinstance(value, str):
            sanitized[key] = sanitize_identifier(value)
        else:
            sanitized[key] = value

    return template.format(**sanitized)


def parse_postgres_array(array_str: str | None) -> list[str]:
    """
    Parse PostgreSQL array string to Python list.

    Args:
        array_str: PostgreSQL array string like "{val1,val2}"

    Returns:
        List of values
    """
    if not array_str:
        return []

    # Remove braces and split
    cleaned = array_str.strip("{}")
    if not cleaned:
        return []

    return [item.strip() for item in cleaned.split(",")]


def estimate_bloat_ratio(
    total_bytes: int,
    dead_tuple_bytes: int,
) -> float:
    """
    Estimate table bloat ratio.

    Args:
        total_bytes: Total table size in bytes
        dead_tuple_bytes: Dead tuple size in bytes

    Returns:
        Bloat ratio (0.0 to 1.0)
    """
    if total_bytes == 0:
        return 0.0

    return dead_tuple_bytes / total_bytes


def categorize_column_type(pg_type: str) -> str:
    """
    Categorize PostgreSQL data type.

    Args:
        pg_type: PostgreSQL type name

    Returns:
        Category: numeric, text, datetime, boolean, json, binary, geometric, other
    """
    pg_type = pg_type.lower()

    numeric_types = (
        "integer", "bigint", "smallint", "numeric", "decimal",
        "real", "double precision", "serial", "bigserial"
    )
    text_types = ("character varying", "varchar", "character", "char", "text")
    datetime_types = (
        "timestamp", "timestamp with time zone",
        "timestamp without time zone", "date", "time", "interval"
    )

    if pg_type in numeric_types:
        return "numeric"
    elif pg_type in text_types:
        return "text"
    elif pg_type in datetime_types:
        return "datetime"
    elif pg_type == "boolean":
        return "boolean"
    elif pg_type in ("json", "jsonb"):
        return "json"
    elif pg_type in ("bytea", "bit", "bit varying"):
        return "binary"
    elif pg_type in ("point", "line", "lseg", "box", "path", "polygon", "circle"):
        return "geometric"
    elif pg_type in ("uuid", "xml", "cidr", "inet", "macaddr"):
        return "special"
    elif pg_type.startswith("array"):
        return "array"
    else:
        return "other"
