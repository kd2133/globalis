# models/gsi_weighted.py

def calculate_weighted_gsi(data):
    """
    Berechnet den gewichteten GSI über alle Topics (Social Presence als Gewichtung).
    """
    total_weight = sum(d['social_presence'] for d in data)
    if total_weight == 0:
        return 0.0
    weighted_sum = sum(d['impact_score'] * d['social_presence'] for d in data)
    return round(weighted_sum / total_weight, 2)
