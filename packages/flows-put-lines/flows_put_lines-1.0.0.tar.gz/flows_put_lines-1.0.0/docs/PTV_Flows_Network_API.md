# PTV Flows Network/Map API Summary

- Network API Base: https://api.ptvgroup.tech/flows/map/v1
- Auth: Header `apiKey`

## Endpoints
- GET /streets → Protobuf network streets data (requires Network API access)
- GET /tiles → JSON list of tiles for your product instance

## Corridor Map-Matching
- Public KPI API requires `location.entities` to persist PATH locations.
- Deriving `entities` (map-matching a WKT path onto Flows streets) is not exposed in public KPI endpoints.
- You must request Flows Map/Network access or use precomputed corridors to obtain `entities`.

## Practical Approaches
- Server-side: With proper instance privileges, Flows can map-match provided shapes to streets and populate `entities`.
- Precompute: Use an existing `locationId` (previously created corridor), then reference it when creating KPIs.
- Manual: Provide OpenLR per segment (`strt`, `fsnd`, `order`, `startProgressive`, `endProgressive`).

## References
- OpenAPI: https://api.ptvgroup.tech/meta/services/flows/map/v1/openapi.json
- Tiles example shows productInstanceId and mapVersion.
