
import requests

SPACEX_LATEST_LAUNCH_URLS = [
    "https://api.spacexdata.com/v5/launches/latest",
    "https://api.spacexdata.com/v4/launches/latest",
]
REQUEST_HEADERS = {
    "Accept": "application/json",
    "User-Agent": "ai-space-security-advanced/1.0",
}
FALLBACK_LATEST_LAUNCH = {
    "name": "Crew-5",
    "flight_number": 187,
    "date_utc": "2022-10-05T16:00:00.000Z",
    "success": True,
    "details": None,
    "webcast": "https://youtu.be/5EwW8ZkArL4",
    "article": None,
    "wikipedia": "https://en.wikipedia.org/wiki/SpaceX_Crew-5",
    "source": "fallback",
}


def get_latest_launch():
    last_error = None

    for url in SPACEX_LATEST_LAUNCH_URLS:
        try:
            response = requests.get(url, headers=REQUEST_HEADERS, timeout=15)
            response.raise_for_status()
            launch = response.json()
            break
        except requests.RequestException as exc:
            last_error = exc
    else:
        launch = FALLBACK_LATEST_LAUNCH.copy()
        launch["error"] = f"Live SpaceX API unavailable: {last_error}"
        return launch

    return {
        "name": launch.get("name"),
        "flight_number": launch.get("flight_number"),
        "date_utc": launch.get("date_utc"),
        "success": launch.get("success"),
        "details": launch.get("details"),
        "webcast": launch.get("links", {}).get("webcast"),
        "article": launch.get("links", {}).get("article"),
        "wikipedia": launch.get("links", {}).get("wikipedia"),
        "source": "live",
    }


def run(*args, **kwargs):
    try:
        return get_latest_launch()
    except (requests.RequestException, RuntimeError) as exc:
        return {
            "name": "SpaceX launch data unavailable",
            "error": str(exc),
        }
