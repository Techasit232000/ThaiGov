
from sklearn.ensemble import IsolationForest

model = IsolationForest(contamination=0.01)

def detect_anomaly(data):
    try:
        r = model.fit_predict(data)
        if -1 in r:
            return "Satellite anomaly detected"
        return "Telemetry normal"
    except:
        return "AI error"
