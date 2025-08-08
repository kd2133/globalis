import json
import os
import logging
from statistics import median
from typing import Dict, Union

logger = logging.getLogger(__name__)

def calculate_combined_score(
    presence_ratio: float,
    min_rel: float,
    med_rel: float,
    max_rel: float,
    sentiment: float
) -> float:
    """
    Kombiniert Präsenz und Sentiment zu einem flüssigen Score:
    - min_rel: Score = 50 (neutral)
    - max_rel: Score = 100 (sentiment=1.0) oder 0 (sentiment=-1.0)
    - Zwischen min_rel und max_rel: Sentiment-proportionale Interpolation
    - Über max_rel: Score nur vom Sentiment abhängig
    """
    try:
        if not isinstance(presence_ratio, (int, float)) or presence_ratio < 0:
            return 50.0
        if not isinstance(sentiment, (int, float)) or sentiment < -1 or sentiment > 1:
            return 50.0
        if max_rel <= min_rel:
            return 50.0

        if presence_ratio <= min_rel or abs(sentiment) <= 0.01:  # Neutral oder unter min_rel
            return 50.0
        elif presence_ratio >= max_rel:
            # Score nur vom Sentiment abhängig
            return max(0.0, min(100.0, 50.0 + sentiment * 50.0))
        else:
            # Sentiment-proportionale Interpolation
            abs_sentiment = abs(sentiment)
            if sentiment > 0.01:
                if presence_ratio <= med_rel:
                    # 50 -> 50 + 25*|sentiment|
                    target = 50.0 + 25.0 * abs_sentiment
                    score = 50.0 + ((presence_ratio - min_rel) / (med_rel - min_rel)) * (target - 50.0)
                else:
                    # 50+25*|sentiment| -> 50+50*|sentiment|
                    start = 50.0 + 25.0 * abs_sentiment
                    target = 50.0 + 50.0 * abs_sentiment
                    score = start + ((presence_ratio - med_rel) / (max_rel - med_rel)) * (target - start)
                return min(100.0, score)
            else:  # sentiment < -0.01
                if presence_ratio <= med_rel:
                    # 50 -> 50 - 25*|sentiment|
                    target = 50.0 - 25.0 * abs_sentiment
                    score = 50.0 - ((presence_ratio - min_rel) / (med_rel - min_rel)) * (50.0 - target)
                else:
                    # 50-25*|sentiment| -> 50-50*|sentiment|
                    start = 50.0 - 25.0 * abs_sentiment
                    target = 50.0 - 50.0 * abs_sentiment
                    score = start - ((presence_ratio - med_rel) / (max_rel - med_rel)) * (start - target)
                return max(0.0, score)

    except Exception as e:
        logger.error(f"Fehler bei Combined Score: {e}")
        return 50.0

def load_historical_stats() -> Dict[str, Dict[str, Union[float, list]]]:
    """
    Lädt historische Statistik aus JSON-Datei.
    """
    stats_file = 'data/social_presence_stats.json'
    try:
        if os.path.exists(stats_file):
            with open(stats_file, 'r') as f:
                return json.load(f)
        else:
            logger.info(f"Keine Stats-Datei gefunden, verwende Default-Werte: {stats_file}")
            return {
                topic: {'min_rel': 0.01, 'med_rel': 0.05, 'max_rel': 0.5, 'history': []}
                for topic in ['Inflation', 'Migration', 'Environment', 'Energy', 'Safety', 'Healthcare', 'Freedom']
            }
    except Exception as e:
        logger.error(f"Fehler beim Laden historischer Statistik: {e}")
        return {
            topic: {'min_rel': 0.01, 'med_rel': 0.05, 'max_rel': 0.5, 'history': []}
            for topic in ['Inflation', 'Migration', 'Environment', 'Energy', 'Safety', 'Healthcare', 'Freedom']
        }

def save_historical_stats(stats: Dict[str, Dict[str, Union[float, list]]]) -> None:
    """
    Speichert historische Statistik in JSON-Datei.
    """
    stats_file = 'data/social_presence_stats.json'
    try:
        os.makedirs(os.path.dirname(stats_file), exist_ok=True)
        with open(stats_file, 'w') as f:
            json.dump(stats, f, indent=2)
        logger.info(f"Historische Statistik gespeichert: {stats_file}")
    except Exception as e:
        logger.error(f"Fehler beim Speichern historischer Statistik: {e}")