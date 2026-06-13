
from orbit_tracking.iss_tracker import get_iss_position
from satellite_ingest.satellite_api import run as get_spacex_latest_launch


def get_dashboard_metrics():
    return {
        "iss_position": get_iss_position(),
        "spacex_latest_launch": get_spacex_latest_launch(),
    }


def run(*args, **kwargs):
    return get_dashboard_metrics()
