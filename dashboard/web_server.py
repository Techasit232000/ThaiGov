
from flask import Flask, jsonify

from dashboard.metrics_api import get_dashboard_metrics

app = Flask(__name__)


@app.get("/api/metrics")
def metrics():
    return jsonify(get_dashboard_metrics())


@app.get("/")
def index():
    metrics_data = get_dashboard_metrics()
    launch = metrics_data["spacex_latest_launch"]
    iss = metrics_data["iss_position"]

    return {
        "system": "AI Space Security Advanced Dashboard",
        "iss_position": iss,
        "latest_spacex_launch": launch,
    }


def run(*args, **kwargs):
    return get_dashboard_metrics()


if __name__ == "__main__":
    app.run(debug=True)
