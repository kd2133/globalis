import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.sentiment_analyzer import analyze_sentiment

# Die Posts aus SENTIMENT_MOCK
mock_posts = [
    "We need better migration policies.",
    "I am worried about inflation.",
    "Renewable energy should be our top priority.",
    "Traveling broadens the mind.",
    "Climate change is the biggest threat.",
    "Solar power is the future."
]

# Die erwarteten Mock-Werte (wie im Test)
expected_scores = {
    "We need better migration policies.": -0.8,
    "I am worried about inflation.": -0.8,
    "Renewable energy should be our top priority.": 0.8,
    "Traveling broadens the mind.": 0.0,
    "Climate change is the biggest threat.": -0.8,
    "Solar power is the future.": 0.8
}

print("\n--- Sentiment Calibration Vergleich ---")
for text in mock_posts:
    ml_score = analyze_sentiment(text)
    expected = expected_scores[text]
    print(f"Text: {text}\nML-Score: {ml_score:.3f} | Erwartet: {expected:.3f}\n")

#    --- Sentiment Calibration Vergleich ---
#Text: We need better migration policies.
#ML-Score: 0.211 | Erwartet: -0.800

#Text: I am worried about inflation.
#ML-Score: -0.785 | Erwartet: -0.800

#Text: Renewable energy should be our top priority.
#ML-Score: 0.734 | Erwartet: 0.800

#Text: Traveling broadens the mind.
#ML-Score: 0.563 | Erwartet: 0.000

#Text: Climate change is the biggest threat.
#ML-Score: -0.807 | Erwartet: -0.800

#Text: Solar power is the future.
#ML-Score: 0.985 | Erwartet: 0.800