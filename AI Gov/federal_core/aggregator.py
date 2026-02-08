def aggregate_regional_insights(regional_reports):
    total = sum(r["risk_score"] for r in regional_reports)
    national_score = total / len(regional_reports)
    return round(national_score, 3)
