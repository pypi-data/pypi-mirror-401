from typing import Dict, Optional, List

import requests


def build_expected_travel_time_payload(
    name: str,
    path_wkt: str,
    timetostart_seconds: int,
    warning_minutes: int,
    critical_minutes: int,
) -> Dict:
    return {
        "name": name,
        "location": {
            "locationType": "PATH",
            "name": f"{name} corridor",
            "shape": path_wkt,
        },
        "kpiInstanceParameters": {
            "parameters": {
                "timetostart": timetostart_seconds,
            }
        },
        "thresholdsDefinition": {
            "kpiThresholdsReference": "UNUSUAL",
            "thresholdsValues": {
                "warningThreshold": warning_minutes,
                "criticalThreshold": critical_minutes,
            },
        },
        # Unit typically MINUTES for EXPECTED_TRAVEL_TIME; server may set implicitly
        "unitOfMeasure": "MINUTES",
    }


def build_expected_travel_time_payload_with_entities(
    name: str,
    entities: List[Dict],
    timetostart_seconds: int,
    warning_minutes: int,
    critical_minutes: int,
    shape_wkt: Optional[str] = None,
) -> Dict:
    loc: Dict = {
        "locationType": "PATH",
        "name": f"{name} corridor",
        "entities": entities,
    }
    if shape_wkt:
        loc["shape"] = shape_wkt

    return {
        "name": name,
        "location": loc,
        "kpiInstanceParameters": {
            "parameters": {
                "timetostart": timetostart_seconds,
            }
        },
        "thresholdsDefinition": {
            "kpiThresholdsReference": "UNUSUAL",
            "thresholdsValues": {
                "warningThreshold": warning_minutes,
                "criticalThreshold": critical_minutes,
            },
        },
        "unitOfMeasure": "MINUTES",
    }


def create_kpi_instance(
    base_url: str,
    api_key: str,
    payload: Dict,
) -> Optional[Dict]:
    url = f"{base_url}/instance?template=EXPECTED_TRAVEL_TIME"
    headers = {
        "Content-Type": "application/json",
        "apiKey": api_key,
    }
    resp = requests.post(url, json=payload, headers=headers, timeout=60)
    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        # Attach server error details if present, with actionable guidance
        detail = None
        try:
            detail = resp.json()
        except Exception:
            detail = resp.text

        # Improve message when corridor entities are missing
        msg = f"{e}"
        if isinstance(detail, dict):
            desc = detail.get("description", "")
            causes = detail.get("causes", [])
            cause_descs = [c.get("description", "") for c in causes if isinstance(c, dict)]
            texts = " ".join([desc] + cause_descs)
            if "Entity list is empty" in texts:
                msg += (
                    " | Cause: corridor entities are missing."
                    " The KPI API requires a non-empty 'location.entities' list (OpenLR-encoded streets)"
                    " to create PATH locations. Shape-only payloads cannot be persisted."
                    " Options: map-match the WKT to Flows network to derive entities (requires Flows Map/Network access),"
                    " reuse an existing 'locationId', or provide OpenLR codes per segment."
                )
            elif "corridor" in texts and "1000" in texts:
                msg += (
                    " | Cause: corridor exceeds engine limits (likely >1000 streets)."
                    " Consider segmenting the path into smaller KPIs."
                )
        raise RuntimeError(f"{msg} | details: {detail}")
    return resp.json()


def get_kpi_status(base_url: str, api_key: str, kpi_id: str) -> Dict:
    """Fetch KPI status by KPI ID using the status endpoint from the collection.

    GET {base_url}/status/by-kpi-id?kpiId=<id>
    """
    url = f"{base_url}/status/by-kpi-id"
    headers = {"apiKey": api_key}
    params = {"kpiId": kpi_id}
    resp = requests.get(url, headers=headers, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def get_all_kpis(base_url: str, api_key: str) -> List[Dict]:
    """Fetch all running KPIs.

    GET {base_url}/instance/all
    """
    url = f"{base_url}/instance/all"
    headers = {"apiKey": api_key}
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    # Response is a list of KPI objects
    if isinstance(data, list):
        return data
    # Or might be wrapped in a dict with a 'kpis' key
    return data.get("kpis", [])


def delete_kpi(base_url: str, api_key: str, kpi_id: str) -> None:
    """Delete a KPI by ID.

    DELETE {base_url}/instance?id={kpiId}
    """
    url = f"{base_url}/instance"
    headers = {"apiKey": api_key}
    params = {"id": kpi_id}
    resp = requests.delete(url, headers=headers, params=params, timeout=30)
    resp.raise_for_status()

