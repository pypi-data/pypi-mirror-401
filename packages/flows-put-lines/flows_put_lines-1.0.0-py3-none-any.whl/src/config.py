import os
from dataclasses import dataclass
from typing import List, Optional

import yaml


@dataclass
class PtvApiConfig:
    base_url: str
    api_key: Optional[str]
    route_matcher_base_url: Optional[str] = None


@dataclass
class GtfsConfig:
    url: str
    route_short_names: List[str]
    max_routes: int = 5


@dataclass
class KpiThresholds:
    warning_minutes: int
    critical_minutes: int


@dataclass
class KpiConfig:
    name_prefix: str
    thresholds: KpiThresholds
    timetostart_seconds: int
    apply: bool


@dataclass
class RuntimeConfig:
    data_dir: str


@dataclass
class AppConfig:
    ptv_api: PtvApiConfig
    gtfs: GtfsConfig
    kpi: KpiConfig
    runtime: RuntimeConfig


def load_config(path: str) -> AppConfig:
    with open(path, "r", encoding="utf-8") as f:
        doc = yaml.safe_load(f) or {}

    ptv = doc.get("ptv_api", {})
    gtfs = doc.get("gtfs", {})
    kpi = doc.get("kpi", {})
    runtime = doc.get("runtime", {})

    base_url = ptv.get("base_url", "https://api.ptvgroup.tech/kpieng/v1")
    route_matcher_base_url = ptv.get("route_matcher_base_url", "https://api.myptv.com/flows/routematcher/v1")
    api_key_env = ptv.get("api_key_env")
    api_key = os.getenv(api_key_env) if api_key_env else ptv.get("api_key")

    ptv_cfg = PtvApiConfig(base_url=base_url, api_key=api_key, route_matcher_base_url=route_matcher_base_url)

    gtfs_cfg = GtfsConfig(
        url=gtfs.get("url", ""),
        route_short_names=list(gtfs.get("route_short_names", []) or []),
        max_routes=int(gtfs.get("max_routes", 5)),
    )

    thresholds_doc = kpi.get("thresholds", {})
    thresholds = KpiThresholds(
        warning_minutes=int(thresholds_doc.get("warning_minutes", 15)),
        critical_minutes=int(thresholds_doc.get("critical_minutes", 30)),
    )

    kpi_cfg = KpiConfig(
        name_prefix=kpi.get("name_prefix", "GTFS Line"),
        thresholds=thresholds,
        timetostart_seconds=int(kpi.get("timetostart_seconds", 0)),
        apply=bool(kpi.get("apply", False)),
    )

    runtime_cfg = RuntimeConfig(data_dir=runtime.get("data_dir", "data"))

    return AppConfig(ptv_api=ptv_cfg, gtfs=gtfs_cfg, kpi=kpi_cfg, runtime=runtime_cfg)
