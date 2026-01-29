# Implementation Status (Jan 14, 2026)

## Completed
- Config and CLI to download GTFS with caching (ETag/Last-Modified).
- GTFS parsing and corridor WKT generation per GTFS direction (0/1).
- Route Matcher integration: derive `location.entities` from GTFS WKT via POST /matchroute.
- KPI creation with EXPECTED_TRAVEL_TIME template using derived entities (one KPI per GTFS direction).
- Status verification via GET /status/by-kpi-id after creation.
- Dry-run payloads and stats reporting.
- README notes and error guidance.

## Resolved
- ~~KPI creation via `POST /instance?template=EXPECTED_TRAVEL_TIME` fails with `GENERAL_VALIDATION_ERROR: Entity list is empty`.~~
  - **Resolution**: Enabled Flows Map/Network API access; Route Matcher now derives corridor entities successfully.
- ~~KPI API requires `location.entities` for PATH locations.~~
  - **Resolution**: Integrated Route Matcher to map-match WKT → entities (strt/fsnd pairs) before KPI creation.

## Working Flow (Jan 14, 2026)
1. Download and cache GTFS feed.
2. Parse routes, trips, stop_times, stops, shapes.
3. Derive endpoints and canonical shape per GTFS direction (0/1).
4. Build WKT LINESTRING per direction.
5. Call Route Matcher to derive corridor entities from WKT.
6. Create KPI instance with PATH location + entities + UNUSUAL thresholds.
7. Fetch and log KPI status.

## Next Steps (Future Work)
- Optional: Add `.gitignore` to exclude `data/` artifacts (gtfs.zip, gtfs_meta.json).
- Optional: Increase `gtfs.max_routes` to roll out more lines.
- Optional: Persist created KPI IDs to JSON for lifecycle management (pause/delete/status checks).
- Optional: Add retries/backoff for API calls.

## References
- KPI API OpenAPI: https://api.ptvgroup.tech/meta/services/kpieng/v1/openapi.json
- Route Matcher API OpenAPI: https://api.ptvgroup.tech/meta/services/flows/routematcher/v1/openapi.json
- Network API OpenAPI: https://api.ptvgroup.tech/meta/services/flows/map/v1/openapi.json
- Docs: Quick Start / Use Cases / OpenLR concept.
