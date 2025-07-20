# models/gsi_score.py
# Berechnet den Impact Score für GSI

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils.helpers import (
    calculate_social_presence_score,
    calculate_social_engagement_score,
    calculate_social_visibility,
    calculate_visibility_factor,
    calculate_sentiment_scaled,
    calculate_impact_score,
    get_news_contrast
)

def calculate_gsi_impact(data):
    try:
        presence_score = calculate_social_presence_score(data["social_presence"])
        engagement_score = calculate_social_engagement_score(
            data["likes"], data["shares"], data["comments"], data["views"]
        )
        visibility = calculate_social_visibility(presence_score, engagement_score)
        visibility_factor = calculate_visibility_factor(visibility)
        sentiment_scaled = calculate_sentiment_scaled(data["sentiment_raw"])
        impact_score = calculate_impact_score(visibility_factor, sentiment_scaled)
        contrast = get_news_contrast(presence_score, data["news_presence"])

        return {
            "Social Presence Score": presence_score,
            "Social Engagement Score": engagement_score,
            "Social Visibility": visibility,
            "Social Visibility Factor": visibility_factor,
            "Sentiment (scaled)": sentiment_scaled,
            "Final Impact Score": impact_score,
            "News Contrast": contrast
        }
    except Exception as e:
        raise ValueError(f"Fehler bei Impact Score: {e}")

if __name__ == "__main__":
    # Testaufruf
    sample_data = {
        "social_presence": 0.8,
        "sentiment_raw": 20.5,
        "news_presence": 0.6,
        "likes": 1000,
        "shares": 200,
        "comments": 150,
        "views": 5000
    }
    print(calculate_gsi_impact(sample_data))