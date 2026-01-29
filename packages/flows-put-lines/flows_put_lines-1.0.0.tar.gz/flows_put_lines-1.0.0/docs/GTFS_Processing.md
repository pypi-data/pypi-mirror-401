# GTFS Processing for Corridors

## Files Used
- `routes.txt`: `route_id`, `route_short_name`
- `trips.txt`: `route_id`, `trip_id`, `direction_id`, `shape_id`
- `stop_times.txt`: `trip_id`, `stop_id`, `stop_sequence`
- `stops.txt`: `stop_id`, `stop_lat`, `stop_lon`
- `shapes.txt`: `shape_id`, `shape_pt_lat`, `shape_pt_lon`, `shape_pt_sequence`

## Workflow
- Filter routes by `route_short_name` and limit to `max_routes`.
- Per route, group trips by `direction_id` (0/1).
- Derive endpoints: modal first and last stops across trips for each direction.
- Choose canonical `shape_id`: most frequent `shape_id` within direction.
- Build corridor WKT `LINESTRING` from `shapes.txt` ordered by numeric `shape_pt_sequence`.
  

## Output
- One WKT path per GTFS direction (0/1) per route.
- Stats: routes processed, directions with shape, payloads built.

## Notes
- Sequence sorting must treat `shape_pt_sequence` as numeric.
- Big corridors may exceed KPI engine limits; consider segmenting.
