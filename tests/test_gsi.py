from utils.gsi_weighted import calculate_weighted_gsi
import pytest

def test_weighted_gsi_basic():
    # Zwei Themen, beide gleich präsent, einer mit Score 100, einer mit 0
    data = [
        {"impact_score": 100, "social_presence": 50},
        {"impact_score": 0, "social_presence": 50}
    ]
    # Erwartet: (100*0.5 + 0*0.5) / (0.5+0.5) = 50.0
    assert calculate_weighted_gsi(data) == 50.0

def test_weighted_gsi_mixed():
    # Unterschiedliche Präsenz, unterschiedliche Scores
    data = [
        {"impact_score": 80, "social_presence": 60},
        {"impact_score": 50, "social_presence": 40}
    ]
    # Erwartet: (80*0.6 + 50*0.4) / (0.6+0.4) = (48+20)/1 = 68.0
    assert calculate_weighted_gsi(data) == 68.0

def test_weighted_gsi_zero_weight():
    # Alle social_presence = 0, sollte 0 zurückgeben
    data = [
        {"impact_score": 50, "social_presence": 0},
        {"impact_score": 80, "social_presence": 0}
    ]
    assert calculate_weighted_gsi(data) == 0.0

def test_weighted_gsi_invalid_impact_score():
    # Ungültiger impact_score (negativ)
    data = [
        {"impact_score": -1, "social_presence": 50},
        {"impact_score": 80, "social_presence": 50}
    ]
    with pytest.raises(ValueError):
        calculate_weighted_gsi(data)

def test_weighted_gsi_invalid_social_presence():
    # Ungültige social_presence (über 100)
    data = [
        {"impact_score": 80, "social_presence": 101},
        {"impact_score": 50, "social_presence": 50}
    ]
    with pytest.raises(ValueError):
        calculate_weighted_gsi(data)