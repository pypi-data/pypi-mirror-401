import argparse
import os

from src.config import load_config
from src.gtfs_extractor import (
    download_gtfs_cached,
    load_gtfs_from_zip,
    select_routes_by_short_name,
    derive_direction_endpoints,
    build_linestring_wkt,
)
from src.flows_kpi import (
    build_expected_travel_time_payload_with_entities,
    create_kpi_instance,
    get_kpi_status,
    get_all_kpis,
    delete_kpi,
)
from src.route_matcher import match_route, extract_entities
from src.map_generator import generate_map_html, save_shapes_metadata


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def cli():
    """CLI entrypoint for flows-put-lines command."""
    main()


def main():
    parser = argparse.ArgumentParser(description="Provision travel-time KPIs in PTV Flows from GTFS")
    parser.add_argument("--config", default="config.yaml", help="Path to config.yaml")
    parser.add_argument("--apply", action="store_true", help="Override config and call PTV Flows API")
    parser.add_argument("--delete-all-kpis", action="store_true", help="Delete all existing KPIs and exit")
    args = parser.parse_args()

    cfg = load_config(args.config)
    data_dir = cfg.runtime.data_dir
    ensure_dir(data_dir)

    # Handle --delete-all-kpis early exit
    if args.delete_all_kpis:
        api_key = cfg.ptv_api.api_key
        if not api_key:
            print("Missing API key; set environment variable as per config.")
            return
        print("Fetching all running KPIs...")
        try:
            kpis = get_all_kpis(cfg.ptv_api.base_url, api_key)
            if not kpis:
                print("No KPIs found.")
                return
            print(f"Found {len(kpis)} KPI(s). Deleting...")
            for kpi in kpis:
                kpi_id = kpi.get("id") or kpi.get("kpiId")
                kpi_name = kpi.get("name", "<unnamed>")
                if kpi_id:
                    print(f"  Deleting KPI: {kpi_name} (id={kpi_id})")
                    try:
                        delete_kpi(cfg.ptv_api.base_url, api_key, kpi_id)
                        print(f"    Deleted.")
                    except Exception as e:
                        print(f"    Error deleting KPI {kpi_id}: {e}")
            print("Delete-all-kpis complete.")
        except Exception as e:
            print(f"Error fetching or deleting KPIs: {e}")
        return

    if not cfg.gtfs.url:
        print("GTFS URL is empty in config; please set gtfs.url")
        return

    zip_path = os.path.join(data_dir, "gtfs.zip")
    meta_path = os.path.join(data_dir, "gtfs_meta.json")
    print(f"Downloading GTFS from {cfg.gtfs.url} (with cache)...")
    zip_path, dl_status = download_gtfs_cached(cfg.gtfs.url, zip_path, meta_path)
    print(f"GTFS {dl_status}; using {zip_path}")

    tables = load_gtfs_from_zip(zip_path)
    routes = select_routes_by_short_name(tables["routes"], cfg.gtfs.route_short_names)
    total_routes = len(routes)
    if total_routes > cfg.gtfs.max_routes:
        routes = routes.head(cfg.gtfs.max_routes)
    print(f"Selected {len(routes)} routes (out of {total_routes}); limiting to {cfg.gtfs.max_routes}.")

    if routes.empty:
        print("No routes matched route_short_names; consider leaving empty to select all.")
        return

    apply = args.apply or cfg.kpi.apply
    print(f"Apply mode: {'ON' if apply else 'DRY-RUN'}")

    stats = {
        "routes_processed": 0,
        "directions_with_shape": 0,
        "kpi_payloads_built": 0,
        "kpis_created": 0,
    }
    
    # Collect shapes for map visualization
    shapes_data = []

    for _, route in routes.iterrows():
        route_id = str(route["route_id"])
        route_short_name = str(route.get("route_short_name", route_id))
        print(f"Processing route {route_short_name} (route_id={route_id})")

        endpoints_list = derive_direction_endpoints(route_id, tables["trips"], tables["stop_times"])  # per direction
        if not endpoints_list:
            print("  No endpoints derived; skipping.")
            continue
        stats["routes_processed"] += 1

        for endpoints in endpoints_list:
            shape_id = endpoints.canonical_shape_id
            if not shape_id:
                print(f"  No canonical shape_id for direction {endpoints.direction_id}; skipping.")
                continue
            wkt_forward = build_linestring_wkt(tables["shapes"], shape_id, reverse=False)
            if not wkt_forward:
                print(f"  Failed to build WKT for shape {shape_id}; skipping.")
                continue
            stats["directions_with_shape"] += 1

            base_name = f"{cfg.kpi.name_prefix} {route_short_name} (dir {endpoints.direction_id})"
            name_forward = f"{base_name} A→B"

            if not apply:
                print(f"  DRY-RUN payload: {name_forward}")
                print(f"    location.shape: {wkt_forward[:120]}...")
            else:
                api_key = cfg.ptv_api.api_key
                if not api_key:
                    print("  Missing API key; set environment variable as per config.")
                    return
                try:
                    rm_base = cfg.ptv_api.route_matcher_base_url or "https://api.myptv.com/flows/routematcher/v1"
                    rm_resp = match_route(rm_base, api_key, wkt_forward)
                    entities = extract_entities(rm_resp.get("links", []))
                    if not entities:
                        raise RuntimeError("Route Matcher returned no usable links.")

                    payload = build_expected_travel_time_payload_with_entities(
                        name=name_forward,
                        entities=entities,
                        timetostart_seconds=cfg.kpi.timetostart_seconds,
                        warning_minutes=cfg.kpi.thresholds.warning_minutes,
                        critical_minutes=cfg.kpi.thresholds.critical_minutes,
                        shape_wkt=wkt_forward,  # Always use original GTFS shape for consistency
                    )

                    resp = create_kpi_instance(cfg.ptv_api.base_url, api_key, payload)
                    print(f"  Created KPI: {resp}")

                    kpi_id = resp.get("id") or resp.get("kpiId")
                    kpi_status = "N/A"
                    if kpi_id:
                        try:
                            st = get_kpi_status(cfg.ptv_api.base_url, api_key, kpi_id)
                            kpi_status = st.get("statusCode", "N/A")
                            print(f"  KPI status: {st}")
                        except Exception as se:
                            print(f"  Could not fetch KPI status: {se}")
                    
                    # Collect shape data for map visualization - use GTFS original shape
                    shapes_data.append({
                        "route_short_name": route_short_name,
                        "direction_id": endpoints.direction_id,
                        "kpi_name": name_forward,
                        "kpi_id": kpi_id or "N/A",
                        "kpi_status": kpi_status,
                        "wkt": wkt_forward  # Always use original GTFS shape, not Route Matcher shape
                    })
                except Exception as e:
                    print(f"  Error creating KPI: {e}")
                    print(
                        "  Hint: If the error mentions 'Entity list is empty', your instance lacks corridor"
                        " map-matching privileges. To proceed, enable Flows Map/Network access to derive entities,"
                        " reuse an existing locationId, or supply OpenLR codes for the corridor segments."
                    )
            stats["kpi_payloads_built"] += 1
            stats["kpis_created"] += 1

    print("\nSummary:")
    print(f"  Routes processed: {stats['routes_processed']}")
    print(f"  Directions with shape: {stats['directions_with_shape']}")
    print(f"  KPI payloads built: {stats['kpi_payloads_built']}")
    
    # Generate map visualization if shapes were collected
    if shapes_data:
        shapes_dir = os.path.join(data_dir, "shapes")
        ensure_dir(shapes_dir)
        
        metadata_path = os.path.join(shapes_dir, "shapes_metadata.json")
        save_shapes_metadata(shapes_data, metadata_path)
        
        map_path = os.path.join(shapes_dir, "kpi_map.html")
        generate_map_html(shapes_data, map_path)
        print(f"\nOpen the map: {os.path.abspath(map_path)}")


if __name__ == "__main__":
    main()
