import requests
import pandas as pd
import pickle
import os
import logging
from datetime import datetime
import numpy as np
from dotenv import load_dotenv
from utils.helpers import normalize_presence, calculate_dynamic_threshold

# Logging-Konfiguration: Zeigt Infos und Fehler mit Zeitstempel an
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Holt News-Daten zu einem Thema von der NewsAPI und nutzt einen Tages-Cache
def fetch_news_data(query, count=50):
    cache_file = "data/news_cache.pkl"
    cache = {}
    
    # Lade Cache, falls vorhanden
    if os.path.exists(cache_file):
        with open(cache_file, "rb") as f:
            cache = pickle.load(f)
    
    cache_key = f"{query}_{datetime.now().strftime('%Y-%m-%d')}"
    if cache_key in cache:
        logger.info(f"Cache-Treffer für {query}")
        return cache[cache_key]
    
    try:
        load_dotenv()
        api_key = os.getenv("NEWSAPI_KEY")
        url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}&pageSize={count}&language=en"
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        data = [
            {"title": article["title"], "published_at": article["publishedAt"], "lang": "en"}
            for article in articles
        ]
        cache[cache_key] = data
        with open(cache_file, "wb") as f:
            pickle.dump(cache, f)
        logger.info(f"{len(data)} Nachrichten für {query} abgerufen.")
        return data
    except Exception as e:
        logger.error(f"Fehler beim Abrufen von News-Daten für {query}: {e}")
        return []

# Verarbeitet News-Daten für eine Liste von Themen und berechnet News Presence
def process_news_data(topics, count=50):
    all_articles = []
    topic_counts = {topic: 0 for topic in topics}
    week_number = datetime.now().isocalendar()[1]

    # Hole und sammle News-Artikel für jedes Thema
    for topic in topics:
        logger.info(f"Verarbeite News für Thema: {topic}")
        articles = fetch_news_data(topic, count)
        topic_counts[topic] = len(articles)
        for article in articles:
            all_articles.append({
                "topic": topic,
                "title": article["title"],
                "published_at": article["published_at"],
                "lang": article["lang"],
                "news_presence_raw": 0.0,
                "news_presence": 0.0,
                "week": week_number
            })

    # Lade historische Artikel-Anzahlen (für Skalierung und Vergleich)
    historical_article_counts_file = "data/historical_article_counts.npy"
    try:
        historical_article_counts = np.load(historical_article_counts_file, allow_pickle=True).item() if os.path.exists(historical_article_counts_file) else {"Healthcare": 100, "Inflation": 200, "Freedom": 500}
        logger.info(f"Geladene historische Artikel-Anzahlen: {historical_article_counts}")
    except Exception as e:
        logger.error(f"Fehler beim Laden von {historical_article_counts_file}: {e}")
        historical_article_counts = {"Healthcare": 100, "Inflation": 200, "Freedom": 500}

    # Berechne News Presence (Rohwert) für jeden Artikel
    news_presences_raw = []
    total_articles_current = sum(topic_counts.values())
    historical_max_articles = max(list(historical_article_counts.values()) + [total_articles_current * 2] or [1])
    logger.info(f"Historisches Maximum Artikel-Anzahl: {historical_max_articles}, Aktuelle Gesamtartikel: {total_articles_current}")
    for article in all_articles:
        topic = article["topic"]
        article_count = topic_counts[topic]
        article["news_presence_raw"] = article_count / historical_max_articles if article_count > 0 else 0.01
        article["news_presence_raw"] = min(max(article["news_presence_raw"], 0.01), 1.0)
        news_presences_raw.append(article["news_presence_raw"])
        logger.debug(f"News Presence (raw) für {topic}: {article['news_presence_raw']:.4f} (article_count={article_count}, historical_max={historical_max_articles})")

    # Lade und bereinige historische News Presence Werte
    historical_news_file = "data/historical_news_presences.npy"
    try:
        historical_news_presences = np.load(historical_news_file).tolist() if os.path.exists(historical_news_file) else [0.01, 0.05, 0.1, 0.2]
        historical_news_presences = [x for x in historical_news_presences if 0.001 <= x <= 1.0]
        logger.info(f"Geladene und bereinigte historische Präsenzwerte: {historical_news_presences[:10]}... (Länge: {len(historical_news_presences)})")
    except Exception as e:
        logger.error(f"Fehler beim Laden von {historical_news_file}: {e}")
        historical_news_presences = [0.01, 0.05, 0.1, 0.2]

    # Skaliere News Presence für jeden Artikel
    for article in all_articles:
        if historical_news_presences and len(historical_news_presences) >= 3:
            threshold = calculate_dynamic_threshold(historical_news_presences)
            median_val = float(np.median(historical_news_presences))
            max_val = float(np.max(historical_news_presences))
            article["news_presence"] = normalize_presence(article["news_presence_raw"], threshold, median_val, max_val)
        else:
            # Fallback: einfache lineare Skalierung
            article["news_presence"] = 50 + 50 * ((article["news_presence_raw"] - 0.5) / (1 - 0.5))
        logger.debug(f"News Presence (scaled) für {article['topic']}: {article['news_presence']:.2f}")

    # Aktualisiere historische Artikel-Anzahlen
    updated_article_counts = historical_article_counts.copy()
    for topic in topic_counts:
        updated_article_counts[topic] = updated_article_counts.get(topic, 0) + topic_counts[topic]
    np.save(historical_article_counts_file, np.array(updated_article_counts, dtype=object))

    # Speichere die News-Daten als DataFrame und sichere sie als CSV
    df = pd.DataFrame(all_articles)
    if not df.empty:
        historical_file = "data/historical_news_data.csv"
        if os.path.exists(historical_file):
            historical_df = pd.read_csv(historical_file)
            df = pd.concat([historical_df, df], ignore_index=True)
        df.to_csv(historical_file, index=False)
        df.to_csv("data/news_data.csv", index=False)
        logger.info("News-Daten in data/news_data.csv und data/historical_news_data.csv gespeichert!")
        np.save(historical_news_file, np.array(historical_news_presences + news_presences_raw))
    else:
        logger.warning("Keine News-Daten abgerufen.")
    
    return df