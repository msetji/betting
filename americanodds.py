def american_to_percent(american_odds: float) -> float:
    """
    Converts American odds to implied win probability (%).
    """
    if american_odds > 0:
        prob = 100 / (american_odds + 100)
    else:
        prob = abs(american_odds) / (abs(american_odds) + 100)
    return round(prob * 100, 2)

# Examples:
print(american_to_percent(+155))  # 40.0%
print(american_to_percent(-185))  # 54.55%
