import json
import os
from typing import List, Dict


def wkt_linestring_to_geojson(wkt: str) -> List[List[float]]:
    """Convert WKT LINESTRING to GeoJSON coordinates [[lon, lat], ...]."""
    # WKT format: LINESTRING(lon1 lat1, lon2 lat2, ...)
    if not wkt.startswith("LINESTRING"):
        return []
    coords_str = wkt.replace("LINESTRING(", "").replace(")", "")
    pairs = coords_str.split(",")
    coords = []
    for pair in pairs:
        parts = pair.strip().split()
        if len(parts) == 2:
            try:
                lon, lat = float(parts[0]), float(parts[1])
                coords.append([lon, lat])
            except ValueError:
                continue
    return coords


def generate_map_html(shapes_data: List[Dict], output_path: str) -> None:
    """Generate an HTML map with Leaflet showing all KPI shapes.
    
    Args:
        shapes_data: List of dicts with keys: route_short_name, direction_id, kpi_name, kpi_id, wkt
        output_path: Path to write the HTML file
    """
    # Convert all WKT to GeoJSON features
    features = []
    for item in shapes_data:
        coords = wkt_linestring_to_geojson(item["wkt"])
        if not coords:
            continue
        
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": coords
            },
            "properties": {
                "route_short_name": item["route_short_name"],
                "direction_id": item["direction_id"],
                "kpi_name": item["kpi_name"],
                "kpi_id": item.get("kpi_id", "N/A"),
                "kpi_status": item.get("kpi_status", "N/A")
            }
        }
        features.append(feature)
    
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    # Generate HTML with Leaflet
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>PTV Flows KPI Map</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
        }}
        #map {{
            position: absolute;
            top: 0;
            bottom: 0;
            width: 100%;
        }}
        .info-box {{
            position: absolute;
            top: 10px;
            right: 10px;
            background: white;
            padding: 15px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.3);
            z-index: 1000;
            max-width: 300px;
        }}
        .info-box h3 {{
            margin: 0 0 10px 0;
            font-size: 16px;
        }}
        .info-box p {{
            margin: 5px 0;
            font-size: 13px;
        }}
        .legend {{
            position: absolute;
            bottom: 30px;
            left: 10px;
            background: white;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.3);
            z-index: 1000;
        }}
        .legend h4 {{
            margin: 0 0 10px 0;
            font-size: 14px;
        }}
        .legend p {{
            margin: 3px 0;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div id="map"></div>
    <div class="info-box" id="info">
        <h3>PTV Flows KPI Visualization</h3>
        <p><strong>Total KPIs:</strong> {len(features)}</p>
        <p style="color: #666; font-size: 11px;">Click on a line to see details</p>
    </div>
    <div class="legend">
        <h4>Legend</h4>
        <p><span style="color: #3388ff;">━━</span> Direction 0</p>
        <p><span style="color: #ff6633;">━━</span> Direction 1</p>
    </div>
    
    <script>
        // Initialize map centered on first feature
        var geojsonData = {json.dumps(geojson, indent=2)};
        
        // Calculate bounds
        var bounds = L.latLngBounds([]);
        geojsonData.features.forEach(function(feature) {{
            feature.geometry.coordinates.forEach(function(coord) {{
                bounds.extend([coord[1], coord[0]]);
            }});
        }});
        
        var map = L.map('map').fitBounds(bounds);
        
        // Add OpenStreetMap tiles
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }}).addTo(map);
        
        // Color by direction
        function getColor(direction_id) {{
            return direction_id === 0 ? '#3388ff' : '#ff6633';
        }}
        
        // Add GeoJSON layer with popups
        L.geoJSON(geojsonData, {{
            style: function(feature) {{
                return {{
                    color: getColor(feature.properties.direction_id),
                    weight: 4,
                    opacity: 0.8
                }};
            }},
            onEachFeature: function(feature, layer) {{
                var props = feature.properties;
                var popupContent = `
                    <div style="min-width: 200px;">
                        <h4 style="margin: 0 0 10px 0;">${{props.kpi_name}}</h4>
                        <p><strong>Route:</strong> ${{props.route_short_name}}</p>
                        <p><strong>Direction:</strong> ${{props.direction_id}}</p>
                        <p><strong>KPI ID:</strong> <code style="font-size: 10px;">${{props.kpi_id}}</code></p>
                        <p><strong>Status:</strong> ${{props.kpi_status}}</p>
                    </div>
                `;
                layer.bindPopup(popupContent);
                
                // Update info box on click
                layer.on('click', function() {{
                    document.getElementById('info').innerHTML = `
                        <h3>${{props.kpi_name}}</h3>
                        <p><strong>Route:</strong> ${{props.route_short_name}}</p>
                        <p><strong>Direction:</strong> ${{props.direction_id}}</p>
                        <p><strong>KPI ID:</strong><br><code style="font-size: 10px;">${{props.kpi_id}}</code></p>
                        <p><strong>Status:</strong> ${{props.kpi_status}}</p>
                    `;
                }});
            }}
        }}).addTo(map);
    </script>
</body>
</html>"""
    
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Map visualization generated: {output_path}")


def save_shapes_metadata(shapes_data: List[Dict], output_path: str) -> None:
    """Save shapes metadata as JSON for later reference."""
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(shapes_data, f, indent=2, ensure_ascii=False)
    print(f"Shapes metadata saved: {output_path}")
