# PTV Flows KPI API Summary

- Base URL: https://api.ptvgroup.tech/kpieng/v1
- Auth: Header `apiKey: YOUR_API_KEY`

## Create KPI Instance
- Endpoint: POST /instance?template=EXPECTED_TRAVEL_TIME
- Payload (KpiInstanceDto):
  - `name`: descriptive string
  - `location` (KpiLocationDto):
    - `locationType`: PATH
    - `name`: location name
    - `shape`: WKT `LINESTRING(lon lat, ...)`
    - `entities`: writeOnly array of corridor segments (AffectedEntityDto). Required for persistence; WKT-only fails.
  - `kpiInstanceParameters.parameters`:
    - `timetostart`: seconds offset (0 for immediate)
  - `thresholdsDefinition`:
    - `kpiThresholdsReference`: UNUSUAL | FREE_FLOW
    - `thresholdsValues.warningThreshold` and `criticalThreshold`: minutes
  - Server sets readOnly fields: `template`, `direction`, `visualizationModes`, `unitOfMeasure`

### Common Errors
- 400 GENERAL_VALIDATION_ERROR: "Entity list is empty" → Supply `location.entities` (OpenLR segments) or reuse `locationId`.
- 400: Corridor exceeds limit (~1000 streets) → Segment the path.

## KPI Location API
- GET /location/by-id?locationId=uuid → returns location with entities
- PUT /location/by-id?locationId=uuid → update location (including entities)
- GET /location/all → locations for active KPIs

## KPI Instance API
- GET /instance/all → list active KPIs
- GET /instance/by-kpi-id?kpiId=uuid → one KPI instance
- DELETE /instance?id=uuid → delete KPI
- GET /count → count KPIs

## KPI Results & Status
- POST /result/by-kpi-ids → results for multiple KPIs in [from,to]
- GET /result/by-kpi-id?kpiId=uuid → results for one KPI
- GET /status/all, GET /status/by-kpi-id → latest status (OK/WARNING/CRITICAL)

## Notes
- PATH creation requires corridor `entities`; shape-only payloads are not persisted.
- `entities` entries include: `strt` (street id), `fsnd` (from node id), `order`, `startProgressive`, `endProgressive`, and server-computed `openLrCode`.
- Example responses show PATH `shape` as WKT and `locationId` UUID.
