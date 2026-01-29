"""
Claude Skill for Flows Put Lines.

This skill allows Claude to provision PTV Flows KPIs from GTFS feeds
using the flows-put-lines package.
"""

import os
import sys
from typing import Dict, Any, List, Optional

# Ensure the package can be imported
try:
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
except ImportError:
    print("ERROR: flows-put-lines package not found. Install it with:")
    print("  pip install -e /path/to/Flows-put-lines")
    sys.exit(1)


class FlowsPutLinesSkill:
    """
    Claude skill for managing PTV Flows KPIs from GTFS data.
    
    This skill provides methods to:
    - Download and process GTFS feeds
    - Create travel time KPIs on PTV Flows
    - Generate interactive map visualizations
    - Delete existing KPIs
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize the skill with a configuration file.
        
        Args:
            config_path: Path to the YAML configuration file
        """
        self.config = load_config(config_path)
        self.api_key = self.config.ptv_api.api_key
        if not self.api_key:
            # Prompt for API key if missing
            print("PTV_API_KEY not found in environment or config.")
            entered = input("Enter PTV_API_KEY: ").strip()
            if not entered:
                raise ValueError("PTV API key is required")
            os.environ["PTV_API_KEY"] = entered
            # Reload config to pick up env substitution if applicable
            self.config = load_config(config_path)
            self.api_key = self.config.ptv_api.api_key or entered
    
    def list_kpis(self) -> List[Dict[str, Any]]:
        """
        List all existing KPIs.
        
        Returns:
            List of KPI dictionaries with id, name, template, location info
        """
        base_url = self.config.ptv_api.base_url
        kpis = get_all_kpis(base_url, self.api_key)
        return kpis
    
    def delete_all_kpis(self) -> int:
        """
        Delete all existing KPIs.
        
        Returns:
            Number of KPIs deleted
        """
        base_url = self.config.ptv_api.base_url
        kpis = get_all_kpis(base_url, self.api_key)
        count = 0
        for kpi in kpis:
            kpi_id = kpi.get("kpiId")
            if kpi_id:
                success = delete_kpi(base_url, self.api_key, kpi_id)
                if success:
                    count += 1
        return count
    
    def provision_kpis_from_gtfs(
        self,
        gtfs_url: str,
        route_short_names: Optional[List[str]] = None,
        max_routes: Optional[int] = None,
        apply: bool = False
    ) -> Dict[str, Any]:
        """
        Download GTFS feed and provision KPIs.
        
        Args:
            gtfs_url: URL to GTFS zip file
            route_short_names: List of route short names to process (None = all)
            max_routes: Maximum number of routes to process
            apply: If True, actually create KPIs; if False, dry-run only
        
        Returns:
            Dictionary with:
                - routes_processed: int
                - directions_with_shape: int
                - kpis_created: int
                - kpi_details: List[Dict]
                - map_path: str (path to generated HTML map)
        """
        # Ensure GTFS URL
        if not gtfs_url:
            print("GTFS URL not provided.")
            gtfs_url = input("Enter GTFS zip URL: ").strip()
            if not gtfs_url:
                raise ValueError("GTFS URL is required")
        # Update config dynamically
        self.config.gtfs.url = gtfs_url
        if route_short_names is not None:
            self.config.gtfs.route_short_names = route_short_names
        if max_routes is not None:
            self.config.gtfs.max_routes = max_routes
        if apply:
            self.config.kpi.apply = True
        
        data_dir = self.config.runtime.data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        # Download GTFS
        print(f"Downloading GTFS from {gtfs_url}...")
        zip_path, meta = download_gtfs_cached(gtfs_url, data_dir)
        print(f"GTFS downloaded: {zip_path}")
        
        # Load and process GTFS
        gtfs_data = load_gtfs_from_zip(zip_path)
        selected_routes = select_routes_by_short_name(
            gtfs_data["routes"],
            self.config.gtfs.route_short_names,
            self.config.gtfs.max_routes
        )
        print(f"Selected {len(selected_routes)} routes")
        
        results = {
            "routes_processed": 0,
            "directions_with_shape": 0,
            "kpis_created": 0,
            "kpi_details": [],
            "map_path": None
        }
        
        shapes_data = []
        
        for _, route_row in selected_routes.iterrows():
            route_id = route_row["route_id"]
            route_short_name = route_row["route_short_name"]
            print(f"\nProcessing route {route_short_name} (route_id={route_id})")
            
            results["routes_processed"] += 1
            
            # Process both directions
            for direction_id in [0, 1]:
                # Build shape
                wkt = build_linestring_wkt(gtfs_data, route_id, direction_id)
                if not wkt:
                    print(f"  No shape for direction {direction_id}")
                    continue
                
                results["directions_with_shape"] += 1
                
                # Derive endpoints
                first_stop, last_stop = derive_direction_endpoints(gtfs_data, route_id, direction_id)
                
                kpi_name = f"GTFS Line {route_short_name} (dir {direction_id}) {first_stop}→{last_stop}"
                
                if self.config.kpi.apply:
                    # Match route to get entities
                    rm_resp = match_route(
                        self.config.ptv_api.route_matcher_base_url,
                        self.api_key,
                        wkt
                    )
                    entities = extract_entities(rm_resp)
                    
                    # Create KPI
                    payload = build_expected_travel_time_payload_with_entities(
                        name=kpi_name,
                        shape_wkt=wkt,
                        entities=entities,
                        warning_minutes=self.config.kpi.thresholds.warning_minutes,
                        critical_minutes=self.config.kpi.thresholds.critical_minutes,
                        timetostart=self.config.kpi.timetostart
                    )
                    
                    kpi_resp = create_kpi_instance(
                        self.config.ptv_api.base_url,
                        self.api_key,
                        payload
                    )
                    
                    kpi_id = kpi_resp.get("kpiId")
                    status_resp = get_kpi_status(
                        self.config.ptv_api.base_url,
                        self.api_key,
                        kpi_id
                    )
                    
                    results["kpis_created"] += 1
                    results["kpi_details"].append({
                        "name": kpi_name,
                        "kpi_id": kpi_id,
                        "route": route_short_name,
                        "direction": direction_id,
                        "status": status_resp.get("statusCode")
                    })
                    
                    # Collect shape data for map
                    shapes_data.append({
                        "route_short_name": route_short_name,
                        "direction_id": direction_id,
                        "kpi_name": kpi_name,
                        "kpi_id": kpi_id,
                        "kpi_status": status_resp.get("statusCode"),
                        "wkt": wkt
                    })
                else:
                    print(f"  [DRY-RUN] Would create KPI: {kpi_name}")
        
        # Generate map if KPIs were created
        if shapes_data:
            shapes_dir = os.path.join(data_dir, "shapes")
            os.makedirs(shapes_dir, exist_ok=True)
            
            save_shapes_metadata(shapes_data, shapes_dir)
            map_path = generate_map_html(shapes_data, shapes_dir)
            results["map_path"] = map_path
            print(f"\nMap generated: {map_path}")
        
        return results
    
    def get_kpi_details(self, kpi_id: str) -> Dict[str, Any]:
        """
        Get detailed status for a specific KPI.
        
        Args:
            kpi_id: KPI instance ID
        
        Returns:
            KPI status dictionary
        """
        return get_kpi_status(
            self.config.ptv_api.base_url,
            self.api_key,
            kpi_id
        )


# Example usage for Claude
def example_usage():
    """
    Example showing how Claude can use this skill.
    """
    # Initialize skill
    skill = FlowsPutLinesSkill("config.yaml")
    
    # List existing KPIs
    print("=== Existing KPIs ===")
    kpis = skill.list_kpis()
    print(f"Found {len(kpis)} KPIs")
    
    # Delete all KPIs (optional cleanup)
    # deleted_count = skill.delete_all_kpis()
    # print(f"Deleted {deleted_count} KPIs")
    
    # Provision new KPIs from GTFS
    print("\n=== Provisioning KPIs ===")
    results = skill.provision_kpis_from_gtfs(
        gtfs_url="https://dati.comune.roma.it/catalog/dataset/a7dadb4a-66ae-4eff-8ded-a102064702ba/resource/266d82e1-ba53-4510-8a81-370880c4678f/download/rome_static_gtfs.zip",
        route_short_names=["211", "C2", "62"],
        max_routes=3,
        apply=True  # Set to False for dry-run
    )
    
    print(f"\nResults:")
    print(f"  Routes processed: {results['routes_processed']}")
    print(f"  KPIs created: {results['kpis_created']}")
    print(f"  Map: {results['map_path']}")
    
    # Get details for a specific KPI
    if results['kpi_details']:
        first_kpi = results['kpi_details'][0]
        print(f"\n=== KPI Details: {first_kpi['name']} ===")
        details = skill.get_kpi_details(first_kpi['kpi_id'])
        print(f"Status: {details.get('statusCode')}")
        print(f"Value: {details.get('value')}")


if __name__ == "__main__":
    example_usage()
