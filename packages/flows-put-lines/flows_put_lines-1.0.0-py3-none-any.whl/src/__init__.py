"""
Flows Put Lines - GTFS to PTV Flows KPI provisioning.

This package downloads GTFS static feeds and creates Expected Travel Time KPIs
on PTV Flows for entire transit lines (one KPI per direction).
"""

from .gtfs_extractor import (
    download_gtfs,
    extract_lines_with_shapes,
    derive_endpoints,
)
from .flows_kpi import (
    create_kpi,
    get_kpi_status,
    get_all_kpis,
    delete_kpi,
)
from .config import load_config

__version__ = "1.0.0"
__all__ = [
    "download_gtfs",
    "extract_lines_with_shapes",
    "derive_endpoints",
    "create_kpi",
    "get_kpi_status",
    "get_all_kpis",
    "delete_kpi",
    "load_config",
]
