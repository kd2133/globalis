from utils.helpers import calculate_social_presence_score, calculate_impact_score, calculate_visibility_factor, normalize_presence

def test_calculate_social_presence_score_precise():
    historical = [0.1, 0.2, 0.3, 0.4]
    score = calculate_social_presence_score(0.2, historical)
    assert isinstance(score, float)
    assert 0 <= score <= 100

def test_calculate_impact_score_extremes_and_middle():
    assert calculate_impact_score(1, 1) == 100
    # Sichtbarkeit 0 ergibt 50 laut Formel!
    assert calculate_impact_score(0, 1) == 50
    # Mittelwert: Sichtbarkeit 0.5, Sentiment 0.5
    assert calculate_impact_score(0.5, 0.5) == round(50 + (0.5 * 0.5 * 50), 2)

def test_calculate_visibility_factor_extremes_and_middle():
    assert calculate_visibility_factor(100) == 1.0
    assert calculate_visibility_factor(0) == 0.0
    assert calculate_visibility_factor(50) == 0.5

def test_normalize_presence_precise():
    result = normalize_presence(0.5, 0.2, 0.8, 1.0)
    assert isinstance(result, float)
    assert 0 <= result <= 100