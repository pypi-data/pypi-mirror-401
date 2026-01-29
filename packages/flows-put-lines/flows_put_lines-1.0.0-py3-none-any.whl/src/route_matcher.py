from typing import Dict, List, Optional

import requests


class RouteMatcherError(RuntimeError):
    pass


def match_route(base_url: str, api_key: str, points_wkt: str) -> Dict:
    """Call Route Matcher /matchroute with a WKT LINESTRING of points.

    Returns a dict with keys possibly including: 'links', 'shape', 'message'.
    Raises RouteMatcherError with server details on failure.
    """
    url = f"{base_url.rstrip('/')}/matchroute"
    headers = {"apiKey": api_key, "Content-Type": "application/json"}
    payload = {"points": points_wkt}
    resp = requests.post(url, json=payload, headers=headers, timeout=60)
    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        detail: Optional[Dict] = None
        try:
            detail = resp.json()
        except Exception:
            detail = {"text": resp.text}
        raise RouteMatcherError(f"RouteMatcher error: {e} | details: {detail}")
    data = resp.json()
    # Normalize to a dict with at least 'links'
    if isinstance(data, list):
        return {"links": data}
    if isinstance(data, dict):
        # Some variants might use a different key; try a few common ones
        if "links" in data:
            return data
        if "routeLinks" in data:
            data["links"] = data.get("routeLinks", [])
            return data
    # Fallback: wrap unknown structure
    return {"links": [], "raw": data}


def extract_entities(links: List) -> List[Dict]:
    """Transform RouteMatcher 'links' into KPI 'location.entities'.

    Expected fields per link: 'strt', 'fsnd', and optionally 'startProgressive', 'endProgressive'.
    Adds sequential 'order' if not present. Filters out links without required ids.
    """
    entities: List[Dict] = []
    for idx, link in enumerate(links or []):
        strt = None
        fsnd = None
        start_prog = 0
        end_prog = 1
        order = idx

        if isinstance(link, dict):
            strt = link.get("strt") or link.get("startNode") or link.get("from") or link.get("a")
            fsnd = link.get("fsnd") or link.get("endNode") or link.get("to") or link.get("b")
            order = link.get("order", order)
            start_prog = link.get("startProgressive", start_prog)
            end_prog = link.get("endProgressive", end_prog)
        elif isinstance(link, (list, tuple)) and len(link) >= 2:
            strt, fsnd = link[0], link[1]

        if strt is None or fsnd is None:
            continue

        entities.append(
            {
                "strt": strt,
                "fsnd": fsnd,
                "order": order,
                "startProgressive": start_prog,
                "endProgressive": end_prog,
            }
        )
    return entities
