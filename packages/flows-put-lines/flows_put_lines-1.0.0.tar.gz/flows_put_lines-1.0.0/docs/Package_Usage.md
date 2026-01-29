# Example: Using flows-put-lines package in another project

This example shows how to use the `flows-put-lines` package in your own Python project.

## Installation

First, install the package:

```bash
pip install flows-put-lines
```

Or if you're developing locally:

```bash
pip install -e /path/to/Flows-put-lines
```

## Basic Usage

### 1. Using the Core API Functions

```python
import os
from src.config import load_config
from src.gtfs_extractor import download_gtfs_cached, load_gtfs_from_zip, select_routes_by_short_name
from src.flows_kpi import create_kpi_instance, get_all_kpis, delete_kpi

# Set up environment
os.environ['PTV_API_KEY'] = 'your_api_key_here'

# Load configuration
config = load_config('config.yaml')

# Download and process GTFS
zip_path, meta = download_gtfs_cached(
    'https://example.com/gtfs.zip',
    'data'
)

gtfs_data = load_gtfs_from_zip(zip_path)
selected_routes = select_routes_by_short_name(
    gtfs_data['routes'],
    route_short_names=['1', '2', '3'],
    max_routes=3
)

print(f"Selected {len(selected_routes)} routes")
```

### 2. Using the Claude Skill (Recommended)

```python
from claude_skill.flows_put_lines_skill import FlowsPutLinesSkill

# Initialize
skill = FlowsPutLinesSkill('config.yaml')

# Create KPIs
results = skill.provision_kpis_from_gtfs(
    gtfs_url='https://example.com/gtfs.zip',
    route_short_names=['1', '2', '3'],
    apply=True
)

print(f"Created {results['kpis_created']} KPIs")
```

### 3. Integration with Web Applications

```python
from flask import Flask, jsonify
from claude_skill.flows_put_lines_skill import FlowsPutLinesSkill

app = Flask(__name__)
skill = FlowsPutLinesSkill('config.yaml')

@app.route('/api/kpis', methods=['GET'])
def list_kpis():
    kpis = skill.list_kpis()
    return jsonify(kpis)

@app.route('/api/provision', methods=['POST'])
def provision():
    # Get parameters from request
    gtfs_url = request.json.get('gtfs_url')
    routes = request.json.get('route_short_names')
    
    results = skill.provision_kpis_from_gtfs(
        gtfs_url=gtfs_url,
        route_short_names=routes,
        apply=True
    )
    
    return jsonify(results)

if __name__ == '__main__':
    app.run()
```

### 4. Automated Scripts

```python
#!/usr/bin/env python3
"""
Daily KPI provisioning script
"""
from claude_skill.flows_put_lines_skill import FlowsPutLinesSkill
import logging

logging.basicConfig(level=logging.INFO)

def daily_kpi_update():
    skill = FlowsPutLinesSkill('config.yaml')
    
    # Clean old KPIs
    deleted = skill.delete_all_kpis()
    logging.info(f"Deleted {deleted} old KPIs")
    
    # Create fresh KPIs
    results = skill.provision_kpis_from_gtfs(
        gtfs_url='https://example.com/gtfs.zip',
        route_short_names=None,  # All routes
        max_routes=50,
        apply=True
    )
    
    logging.info(f"Created {results['kpis_created']} KPIs")
    logging.info(f"Map available at: {results['map_path']}")
    
    return results

if __name__ == '__main__':
    daily_kpi_update()
```

## Configuration

Create a `config.yaml` in your project:

```yaml
gtfs:
  url: "https://example.com/gtfs.zip"
  route_short_names: []
  max_routes: null

ptv_api:
  api_key: ${PTV_API_KEY}
  base_url: "https://api.ptvgroup.tech/kpieng/v1"
  route_matcher_base_url: "https://api.ptvgroup.tech/flows/routematcher/v1"

kpi:
  apply: false
  timetostart: 0
  thresholds:
    warning_minutes: 15
    critical_minutes: 30

runtime:
  data_dir: "data"
```

## Best Practices

1. **Error Handling**: Always wrap API calls in try-except blocks
   ```python
   try:
       results = skill.provision_kpis_from_gtfs(...)
   except Exception as e:
       logging.error(f"Failed to provision KPIs: {e}")
   ```

2. **Dry-Run First**: Test with `apply=False` before creating real KPIs
   ```python
   # Test first
   results = skill.provision_kpis_from_gtfs(apply=False)
   
   # Then apply
   if results['routes_processed'] > 0:
       results = skill.provision_kpis_from_gtfs(apply=True)
   ```

3. **Use Environment Variables**: Never hardcode API keys
   ```python
   import os
   os.environ['PTV_API_KEY'] = os.getenv('PTV_API_KEY', 'default_key')
   ```

4. **Check Results**: Always verify KPI creation
   ```python
   results = skill.provision_kpis_from_gtfs(...)
   
   if results['kpis_created'] != results['directions_with_shape']:
       logging.warning("Not all directions were provisioned as KPIs")
   ```

## See Also

- [Full API Reference](../claude_skill/README.md)
- [Main Documentation](../README.md)
