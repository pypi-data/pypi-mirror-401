# Claude Skill for Flows Put Lines

This directory contains a Claude skill that allows AI assistants to use the `flows-put-lines` package programmatically.

## Installation

1. **Install the flows-put-lines package** (from the parent directory):
   ```bash
   cd ..
   pip install -e .
   ```

2. **Set up your environment**:
   ```bash
   export PTV_API_KEY="your_api_key_here"
   ```

3. **Configure** your `config.yaml` in the parent directory with your GTFS feed and settings.

## Usage

### Import the skill in your Python code:

```python
from claude_skill.flows_put_lines_skill import FlowsPutLinesSkill

# Initialize the skill
skill = FlowsPutLinesSkill("config.yaml")

# List existing KPIs
kpis = skill.list_kpis()
print(f"Found {len(kpis)} KPIs")

# Provision KPIs from a GTFS feed
results = skill.provision_kpis_from_gtfs(
    gtfs_url="https://example.com/gtfs.zip",
    route_short_names=["1", "2", "3"],
    max_routes=3,
    apply=True  # Set to False for dry-run
)

print(f"Created {results['kpis_created']} KPIs")
print(f"Map available at: {results['map_path']}")

# Delete all KPIs
deleted_count = skill.delete_all_kpis()
print(f"Deleted {deleted_count} KPIs")
```

### For Claude/AI Assistants

The skill provides these main methods:

1. **`list_kpis()`** - List all existing KPIs
2. **`delete_all_kpis()`** - Delete all KPIs and return count
3. **`provision_kpis_from_gtfs(gtfs_url, route_short_names, max_routes, apply)`** - Download GTFS and create KPIs
4. **`get_kpi_details(kpi_id)`** - Get detailed status for a specific KPI

## Example: Complete Workflow

```python
from claude_skill.flows_put_lines_skill import FlowsPutLinesSkill

# Initialize
skill = FlowsPutLinesSkill("config.yaml")

# Clean up existing KPIs
deleted = skill.delete_all_kpis()
print(f"Cleaned up {deleted} old KPIs")

# Create new KPIs from Rome GTFS
results = skill.provision_kpis_from_gtfs(
    gtfs_url="https://dati.comune.roma.it/catalog/dataset/a7dadb4a-66ae-4eff-8ded-a102064702ba/resource/266d82e1-ba53-4510-8a81-370880c4678f/download/rome_static_gtfs.zip",
    route_short_names=["211", "C2", "62"],
    max_routes=3,
    apply=True
)

print(f"✓ Processed {results['routes_processed']} routes")
print(f"✓ Created {results['kpis_created']} KPIs")
print(f"✓ Map: {results['map_path']}")

# Check KPI details
for kpi in results['kpi_details']:
    print(f"  - {kpi['name']}: {kpi['status']}")
```

## Running the Example

```bash
# From the claude_skill directory
python flows_put_lines_skill.py
```

This will run the example workflow defined in the script.

## API Reference

### FlowsPutLinesSkill

**Constructor:**
- `FlowsPutLinesSkill(config_path: str = "config.yaml")` - Initialize with config file

**Methods:**

- `list_kpis() -> List[Dict[str, Any]]`
  - Returns list of all existing KPIs

- `delete_all_kpis() -> int`
  - Deletes all KPIs
  - Returns number of KPIs deleted

- `provision_kpis_from_gtfs(gtfs_url, route_short_names=None, max_routes=None, apply=False) -> Dict`
  - Downloads GTFS and creates KPIs
  - Parameters:
    - `gtfs_url`: URL to GTFS zip file
    - `route_short_names`: List of route IDs to process (optional)
    - `max_routes`: Max number of routes to process (optional)
    - `apply`: If True, creates KPIs; if False, dry-run only
  - Returns dictionary with:
    - `routes_processed`: int
    - `directions_with_shape`: int
    - `kpis_created`: int
    - `kpi_details`: List of KPI info
    - `map_path`: Path to generated HTML map

- `get_kpi_details(kpi_id: str) -> Dict[str, Any]`
  - Gets detailed status for a specific KPI
  - Returns KPI status dictionary

## Notes

- The skill automatically uses original GTFS shapes (not trimmed by Route Matcher)
- Interactive HTML maps are generated automatically after KPI creation
- All operations respect the configuration in `config.yaml`
- API key must be set via environment variable `PTV_API_KEY`
