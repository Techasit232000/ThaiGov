from regional_node.generate_regional_report import generate_regional_summary
from federal_core.aggregator import aggregate_regional_insights
from federal_core.national_risk import classify_national_risk
from federal_core.dashboard import run_dashboard

regional_data = [
    generate_regional_summary("Northern Region", 2.0, 0.6, 0.5),
    generate_regional_summary("Central Region", 3.0, 0.8, 0.4),
    generate_regional_summary("Southern Region", 1.5, 0.5, 0.7)
]

national_score = aggregate_regional_insights(regional_data)
classification = classify_national_risk(national_score)

run_dashboard(national_score, classification, regional_data)
