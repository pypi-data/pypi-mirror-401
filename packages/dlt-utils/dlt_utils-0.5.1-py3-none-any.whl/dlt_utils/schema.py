"""
Schema utilities for dlt pipelines.

Ensures database tables exist with complete column definitions, even when
resources return no data. Uses the import schema file ({source}/{source}.schema.yaml)
to get complete column definitions including primary keys and data types.
"""

import logging
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, TYPE_CHECKING

import yaml

if TYPE_CHECKING:
    from dlt import Pipeline

logger = logging.getLogger(__name__)


def _load_import_schema(schema_name: str) -> Optional[Dict[str, Any]]:
    """Load the {schema_name}/{schema_name}.schema.yaml file if it exists."""
    search_paths = [
        Path(schema_name) / f"{schema_name}.schema.yaml",
        Path(f"{schema_name}.schema.yaml"),
    ]
    
    for path in search_paths:
        if path.exists():
            logger.debug(f"Loading import schema from {path}")
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
    
    return None


def _ensure_table_in_schema(
    pipeline: "Pipeline",
    import_schema: Dict[str, Any],
    table_name: str,
) -> None:
    """Merge a table definition from import schema into the pipeline schema."""
    import_tables = import_schema.get("tables", {})
    
    if table_name not in import_tables:
        return
    
    import_table = dict(import_tables[table_name])
    import_table["name"] = table_name
    
    # update_table requires 'name' field on each column
    if "columns" in import_table:
        updated_columns = {}
        for col_name, col_def in import_table["columns"].items():
            col_copy = dict(col_def)
            col_copy["name"] = col_name
            updated_columns[col_name] = col_copy
        import_table["columns"] = updated_columns
    
    pipeline.default_schema.update_table(import_table)


def ensure_all_tables_exist(
    pipeline: "Pipeline",
    only_tables: Optional[Iterable[str]] = None,
) -> Dict[str, Any]:
    """
    Ensure tables exist in the database with complete column definitions.

    Loads the import schema file to get complete column definitions (including
    primary keys and data types) and executes CREATE/ALTER TABLE statements.

    Args:
        pipeline: An initialized dlt pipeline with a loaded schema.
        only_tables: Optional list of specific tables to create.

    Returns:
        Dict with info about created/updated tables.
    """
    schema_name = pipeline.default_schema.name
    import_schema = _load_import_schema(schema_name)
    
    # Determine which tables to check
    tables_to_check: List[str] = []
    if only_tables:
        tables_to_check = list(only_tables)
    elif import_schema:
        import_table_names = set(import_schema.get("tables", {}).keys())
        pipeline_table_names = set(pipeline.default_schema.tables.keys())
        tables_to_check = list(import_table_names | pipeline_table_names)
    else:
        tables_to_check = list(pipeline.default_schema.tables.keys())
    
    # Merge import schema definitions into pipeline schema
    if import_schema:
        for table_name in tables_to_check:
            _ensure_table_in_schema(pipeline, import_schema, table_name)

    with pipeline.destination_client() as client:
        storage_tables = list(client.get_storage_tables(tables_to_check))
        sql_scripts, schema_update = client._build_schema_update_sql(storage_tables)

        if sql_scripts:
            logger.info(f"Creating/updating {len(sql_scripts)} tables")
            client.sql_client.execute_many(sql_scripts)

        return schema_update or {}


def get_tables_for_resources(
    pipeline: "Pipeline",
    resource_names: List[str],
) -> List[str]:
    """
    Find all tables (root + children) for given resources.

    Checks both pipeline schema and import schema to find tables,
    including those for resources with no data.

    Args:
        pipeline: An initialized dlt pipeline with a loaded schema.
        resource_names: List of resource names to find tables for.

    Returns:
        List of table names including child tables.
    """
    schema_name = pipeline.default_schema.name
    import_schema = _load_import_schema(schema_name)
    import_tables = import_schema.get("tables", {}) if import_schema else {}
    
    # Combine pipeline schema tables with import schema tables
    all_tables = dict(pipeline.default_schema.tables)
    for table_name, table_def in import_tables.items():
        if table_name not in all_tables:
            all_tables[table_name] = table_def

    relevant_tables = set()

    for resource_name in resource_names:
        if resource_name in all_tables:
            relevant_tables.add(resource_name)
        
        for table_name, table_def in all_tables.items():
            # Match by resource field
            if table_def.get("resource") == resource_name:
                relevant_tables.add(table_name)
            
            # Match child tables by prefix
            if table_name.startswith(f"{resource_name}__"):
                relevant_tables.add(table_name)

            # Match via parent chain
            parent = table_def.get("parent")
            checked = set()
            while parent and parent not in checked:
                checked.add(parent)
                if parent == resource_name:
                    relevant_tables.add(table_name)
                    break
                parent = all_tables.get(parent, {}).get("parent")

    return list(relevant_tables)


def ensure_tables_for_resources(
    pipeline: "Pipeline",
    resource_names: List[str],
) -> Dict[str, Any]:
    """
    Ensure tables exist for specific resources (including child tables).

    Args:
        pipeline: An initialized dlt pipeline with a loaded schema.
        resource_names: List of resource names to ensure tables for.

    Returns:
        Dict with info about created/updated tables.
    """
    tables = get_tables_for_resources(pipeline, resource_names)
    return ensure_all_tables_exist(pipeline, only_tables=tables)
