# OpenLR in PTV Flows

OpenLR™ encodes locations across different maps. In KPI API context, each corridor street entity includes an `openLrCode`.

## Entity Fields (AffectedEntityDto)
- `strt`: street identifier (int)
- `fsnd`: from-node identifier (int)
- `order`: segment progressive order
- `startProgressive`: offset from segment start (0–1)
- `endProgressive`: offset to segment end (0–1)
- `openLrCode`: server-computed OpenLR for the segment (readOnly)

## Example (from docs)
```
{
  "name": "giotestfinal",
  "entities": [
    {"strt": 84899, "fsnd": 96586, "openLrCode": "CwjonR3U/yKDBADPAMYiM+k=", "order": 0, "startProgressive": 0.66502345, "endProgressive": 1},
    {"strt": 84898, "fsnd": 88888, "openLrCode": "CwjonR3U/yKDBADPAMYicxbf", "order": 1, "startProgressive": 0, "endProgressive": 1}
  ],
  "shape": "LINESTRING (12.5279 41.951363, 12.52804 41.95151, 12.52903 41.95244)",
  "locationId": "833c5ead-3777-4a00-9d8b-87e1b41d1e7f",
  "locationType": "PATH"
}
```

## Notes
- Providing `entities` allows KPI creation; `openLrCode` is computed by Flows when entity references are valid.
- Without entities, PATH locations cannot be persisted via KPI API.
