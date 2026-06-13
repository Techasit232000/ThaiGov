
from orbit_tracking.iss_tracker import get_iss_position
from ai_detection.anomaly_engine import detect_anomaly
from alerts.alert_manager import send_alert

def run():
    pos = get_iss_position()
    print("ISS Position:", pos)

    data = [[1,2],[2,3],[200,500]]
    result = detect_anomaly(data)

    print("AI analysis:", result)

    if "anomaly" in result.lower():
        send_alert(result)

if __name__ == "__main__":
    run()
