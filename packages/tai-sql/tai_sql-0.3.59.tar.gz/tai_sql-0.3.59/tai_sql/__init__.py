"""
Declarative models for SQLAlchemy.
This module provides the base classes and utilities to define
models using SQLAlchemy's declarative system.
"""
from __future__ import annotations
from sqlalchemy.types import (
    BigInteger as bigint,
    Text as text,
    Numeric as numeric,
    LargeBinary as largebinary,
)

from datetime import datetime, date, time
from typing import List, Optional

from .project import ProjectManager as pm
from .core import datasource, generate, env, connection_string, params, query
from .orm import Table, AllTables, View, Enum, column, relation, TriggerAPI, on_create, on_update, on_delete, trigger_api
from .drivers import postgresql, mysql, sqlserver

# Exportar los elementos principales
__all__ = [
    'datasource', 
    'generate',
    'env',
    'connection_string',
    'params',
    'Table',
    'AllTables',
    'column',
    'relation',
    'List',
    'Optional',
    'datetime',
    'date',
    'time',
    'bigint',
    'text',
    'numeric',
    'largebinary',
    'TriggerAPI',
    'on_create',
    'on_update',
    'on_delete',
    'trigger_api',
    'query',
    'View',
    'Enum',
]