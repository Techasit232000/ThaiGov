import numpy as np

def calculate_regional_risk(economic, food, cyber):
    economic_risk = 1 - (economic / 5)
    food_risk = 1 - food
    cyber_risk = cyber

    score = np.mean([economic_risk, food_risk, cyber_risk])
    return round(score, 3)
