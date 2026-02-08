from regional_node.local_risk_model import calculate_regional_risk

def generate_regional_summary(region_name, economic, food, cyber):
    risk = calculate_regional_risk(economic, food, cyber)

    return {
        "region": region_name,
        "risk_score": risk
    }
