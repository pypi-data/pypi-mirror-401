from __future__ import annotations

from typing import Dict, Iterable, List, Optional

from .connectors import MSSQLConnector, PostgresConnector


Catalog = Dict[str, dict]


def _key(schema: str, name: str, obj_type: str) -> str:
    return f"{schema}.{name}:{obj_type}"


def _in_scope(schema: str, includes: Optional[List[str]], excludes: Optional[List[str]]) -> bool:
    if includes and schema not in includes:
        return False
    if excludes and schema in excludes:
        return False
    return True


def extract_catalog_mssql(
    conn: MSSQLConnector, includes: Optional[List[str]] = None, excludes: Optional[List[str]] = None
) -> Catalog:
    """Extract views, procedures, functions, and triggers from SQL Server.

    Read-only, system schemas filtered out. Returns a normalized catalog.
    """
    catalog: Catalog = {}

    # Views
    sql_views = r"""
    SELECT s.name AS schema_name, v.name AS object_name, 'view' AS obj_type,
           m.definition AS definition
    FROM sys.views v
    JOIN sys.schemas s ON s.schema_id = v.schema_id
    LEFT JOIN sys.sql_modules m ON m.object_id = v.object_id
    WHERE s.name NOT IN ('sys', 'INFORMATION_SCHEMA')
    """
    for schema, name, obj_type, definition in conn.fetchall(sql_views):
        if not _in_scope(schema, includes, excludes):
            continue
        catalog[_key(schema, name, obj_type)] = {
            "schema": schema,
            "name": name,
            "type": obj_type,
            "definition": definition or "",
        }

    # Procedures
    sql_procs = r"""
    SELECT s.name AS schema_name, p.name AS object_name, 'procedure' AS obj_type,
           m.definition AS definition
    FROM sys.procedures p
    JOIN sys.schemas s ON s.schema_id = p.schema_id
    LEFT JOIN sys.sql_modules m ON m.object_id = p.object_id
    WHERE s.name NOT IN ('sys', 'INFORMATION_SCHEMA')
    """
    for schema, name, obj_type, definition in conn.fetchall(sql_procs):
        if not _in_scope(schema, includes, excludes):
            continue
        catalog[_key(schema, name, obj_type)] = {
            "schema": schema,
            "name": name,
            "type": obj_type,
            "definition": definition or "",
        }

    # Functions
    sql_funcs = r"""
    SELECT s.name AS schema_name, o.name AS object_name, 'function' AS obj_type,
           m.definition AS definition
    FROM sys.objects o
    JOIN sys.schemas s ON s.schema_id = o.schema_id
    LEFT JOIN sys.sql_modules m ON m.object_id = o.object_id
    WHERE o.type IN ('FN','IF','TF')
      AND s.name NOT IN ('sys', 'INFORMATION_SCHEMA')
    """
    for schema, name, obj_type, definition in conn.fetchall(sql_funcs):
        if not _in_scope(schema, includes, excludes):
            continue
        catalog[_key(schema, name, obj_type)] = {
            "schema": schema,
            "name": name,
            "type": obj_type,
            "definition": definition or "",
        }

    # Triggers
    sql_trigs = r"""
    SELECT s.name AS schema_name, t.name AS object_name, 'trigger' AS obj_type,
           m.definition AS definition
    FROM sys.triggers t
    JOIN sys.objects o ON o.object_id = t.parent_id
    JOIN sys.schemas s ON s.schema_id = o.schema_id
    LEFT JOIN sys.sql_modules m ON m.object_id = t.object_id
    WHERE s.name NOT IN ('sys', 'INFORMATION_SCHEMA')
    """
    for schema, name, obj_type, definition in conn.fetchall(sql_trigs):
        if not _in_scope(schema, includes, excludes):
            continue
        catalog[_key(schema, name, obj_type)] = {
            "schema": schema,
            "name": name,
            "type": obj_type,
            "definition": definition or "",
        }

    return catalog


def extract_catalog_postgres(
    conn: PostgresConnector, includes: Optional[List[str]] = None, excludes: Optional[List[str]] = None
) -> Catalog:
    """Extract views, procedures (pg>=11), functions, triggers from PostgreSQL."""
    catalog: Catalog = {}

    # Views
    sql_views = r"""
    SELECT n.nspname AS schema_name, c.relname AS object_name, 'view' AS obj_type,
           pg_get_viewdef(c.oid, true) AS definition
    FROM pg_class c
    JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE c.relkind = 'v'
      AND n.nspname NOT IN ('pg_catalog', 'information_schema')
    """
    for schema, name, obj_type, definition in conn.fetchall(sql_views):
        if not _in_scope(schema, includes, excludes):
            continue
        catalog[_key(schema, name, obj_type)] = {
            "schema": schema,
            "name": name,
            "type": obj_type,
            "definition": definition or "",
        }

    # Functions
    sql_funcs = r"""
    SELECT n.nspname AS schema_name, p.proname AS object_name, 'function' AS obj_type,
           pg_get_functiondef(p.oid) AS definition
    FROM pg_proc p
    JOIN pg_namespace n ON n.oid = p.pronamespace
    WHERE p.prokind = 'f'
      AND n.nspname NOT IN ('pg_catalog', 'information_schema')
    """
    for schema, name, obj_type, definition in conn.fetchall(sql_funcs):
        if not _in_scope(schema, includes, excludes):
            continue
        catalog[_key(schema, name, obj_type)] = {
            "schema": schema,
            "name": name,
            "type": obj_type,
            "definition": definition or "",
        }

    # Procedures (PostgreSQL 11+)
    sql_procs = r"""
    SELECT n.nspname AS schema_name, p.proname AS object_name, 'procedure' AS obj_type,
           pg_get_functiondef(p.oid) AS definition
    FROM pg_proc p
    JOIN pg_namespace n ON n.oid = p.pronamespace
    WHERE p.prokind = 'p'
      AND n.nspname NOT IN ('pg_catalog', 'information_schema')
    """
    try:
        for schema, name, obj_type, definition in conn.fetchall(sql_procs):
            if not _in_scope(schema, includes, excludes):
                continue
            catalog[_key(schema, name, obj_type)] = {
                "schema": schema,
                "name": name,
                "type": obj_type,
                "definition": definition or "",
            }
    except Exception:
        # Older versions may not support 'p' kind; ignore gracefully.
        pass

    # Triggers
    sql_trigs = r"""
    SELECT n.nspname AS schema_name, tg.tgname AS object_name, 'trigger' AS obj_type,
           pg_get_triggerdef(tg.oid, true) AS definition
    FROM pg_trigger tg
    JOIN pg_class c ON c.oid = tg.tgrelid
    JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE NOT tg.tgisinternal
      AND n.nspname NOT IN ('pg_catalog', 'information_schema')
    """
    for schema, name, obj_type, definition in conn.fetchall(sql_trigs):
        if not _in_scope(schema, includes, excludes):
            continue
        catalog[_key(schema, name, obj_type)] = {
            "schema": schema,
            "name": name,
            "type": obj_type,
            "definition": definition or "",
        }

    return catalog

