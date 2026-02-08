from shared.config import NATIONAL_THRESHOLD_HIGH, NATIONAL_THRESHOLD_MEDIUM

def classify_national_risk(score):
    if score >= NATIONAL_THRESHOLD_HIGH:
        return "High National Instability"
    elif score >= NATIONAL_THRESHOLD_MEDIUM:
        return "Moderate Risk Trend"
    else:
        return "Stable Condition"
