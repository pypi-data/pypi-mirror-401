from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import os
import io
import zipfile
import json

import pandas as pd
import requests


@dataclass
class DirectionEndpoints:
    direction_id: int
    first_stop_id: str
    last_stop_id: str
    canonical_shape_id: Optional[str]


def download_gtfs(url: str, dest_path: str) -> str:
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    resp = requests.get(url, stream=True, timeout=60)
    resp.raise_for_status()
    with open(dest_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    return dest_path


def download_gtfs_cached(url: str, dest_path: str, meta_path: str) -> Tuple[str, str]:
    """Download GTFS with basic HTTP caching using ETag/Last-Modified.
    Returns (path, status) where status is 'downloaded' or 'not-modified'.
    """
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    headers = {}
    status = "downloaded"
    if os.path.exists(meta_path):
        try:
            with open(meta_path, "r", encoding="utf-8") as mf:
                meta = json.load(mf)
            if meta.get("etag"):
                headers["If-None-Match"] = meta["etag"]
            if meta.get("last_modified"):
                headers["If-Modified-Since"] = meta["last_modified"]
        except Exception:
            pass

    resp = requests.get(url, headers=headers, stream=True, timeout=60)
    if resp.status_code == 304 and os.path.exists(dest_path):
        return dest_path, "not-modified"
    resp.raise_for_status()
    with open(dest_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    etag = resp.headers.get("ETag")
    last_modified = resp.headers.get("Last-Modified")
    try:
        with open(meta_path, "w", encoding="utf-8") as mf:
            json.dump({"url": url, "etag": etag, "last_modified": last_modified}, mf)
    except Exception:
        pass
    return dest_path, status


def load_gtfs_from_zip(zip_path: str) -> Dict[str, pd.DataFrame]:
    with zipfile.ZipFile(zip_path, "r") as z:
        def read_csv(name: str) -> pd.DataFrame:
            try:
                with z.open(name) as f:
                    # Read all as string to simplify joins and avoid mixed dtypes; convert numerics later
                    return pd.read_csv(f, dtype=str, low_memory=False)
            except KeyError:
                return pd.DataFrame()

        return {
            "routes": read_csv("routes.txt"),
            "trips": read_csv("trips.txt"),
            "stop_times": read_csv("stop_times.txt"),
            "stops": read_csv("stops.txt"),
            "shapes": read_csv("shapes.txt"),
        }


def select_routes_by_short_name(routes: pd.DataFrame, short_names: List[str]) -> pd.DataFrame:
    if not short_names:
        return routes
    # normalize to strings
    target = set(str(s).strip() for s in short_names)
    return routes[routes["route_short_name"].astype(str).str.strip().isin(target)]


def _mode(items: List[str]) -> Optional[str]:
    if not items:
        return None
    return Counter(items).most_common(1)[0][0]


def derive_direction_endpoints(
    route_id: str,
    trips: pd.DataFrame,
    stop_times: pd.DataFrame,
) -> List[DirectionEndpoints]:
    """Return endpoints and canonical shape per direction (0/1) for a route.
    Uses majority endpoints across trips in each direction, optimized to avoid per-trip filtering.
    """
    out: List[DirectionEndpoints] = []

    # Filter trips for the route
    route_trips = trips[trips["route_id"].astype(str) == str(route_id)]
    if route_trips.empty:
        return out

    # Ensure direction_id is integer-like; treat missing as 0
    di = route_trips["direction_id"].fillna("0")
    route_trips = route_trips.assign(direction_id=di.astype(int))

    for direction_id in (0, 1):
        dir_trips = route_trips[route_trips["direction_id"] == direction_id]
        if dir_trips.empty:
            continue

        # Canonical shape: most frequent shape_id in this direction
        shp_series = dir_trips["shape_id"].dropna().astype(str)
        shape_mode = shp_series.mode().iloc[0] if not shp_series.empty else None

        # Stop endpoints: compute first/last per trip by grouping
        trip_ids = dir_trips["trip_id"].astype(str)
        st_dir = stop_times[stop_times["trip_id"].astype(str).isin(trip_ids)]
        if st_dir.empty:
            continue

        st_dir = st_dir.assign(stop_sequence=st_dir["stop_sequence"].astype(int))
        st_sorted = st_dir.sort_values(["trip_id", "stop_sequence"])  # sort once
        first_per_trip = st_sorted.groupby("trip_id").first()["stop_id"].astype(str).tolist()
        last_per_trip = st_sorted.groupby("trip_id").last()["stop_id"].astype(str).tolist()

        first_mode = _mode(first_per_trip)
        last_mode = _mode(last_per_trip)

        if first_mode and last_mode:
            out.append(
                DirectionEndpoints(
                    direction_id=direction_id,
                    first_stop_id=first_mode,
                    last_stop_id=last_mode,
                    canonical_shape_id=shape_mode,
                )
            )

    return out


def build_linestring_wkt(shapes: pd.DataFrame, shape_id: str, reverse: bool = False) -> Optional[str]:
    seg = shapes[shapes["shape_id"].astype(str) == str(shape_id)]
    if seg.empty:
        return None
    # ensure numeric sort by sequence
    seg_sorted = seg.assign(shape_pt_sequence=seg["shape_pt_sequence"].astype(int)).sort_values("shape_pt_sequence")
    coords = [(float(row["shape_pt_lon"]), float(row["shape_pt_lat"])) for _, row in seg_sorted.iterrows()]
    if reverse:
        coords = list(reversed(coords))
    # WKT requires x y pairs (lon lat)
    wkt_coords = ", ".join(f"{lon} {lat}" for lon, lat in coords)
    return f"LINESTRING({wkt_coords})"


def stop_coords(stops: pd.DataFrame, stop_id: str) -> Optional[Tuple[float, float]]:
    s = stops[stops["stop_id"].astype(str) == str(stop_id)]
    if s.empty:
        return None
    row = s.iloc[0]
    return float(row["stop_lon"]), float(row["stop_lat"])  # lon, lat
