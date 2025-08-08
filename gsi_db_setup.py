import sqlite3
import json
import os
from utils.helpers import (
    calculate_social_presence_score,
    calculate_social_engagement_score,
    calculate_social_visibility,
    calculate_visibility_factor,
    calculate_sentiment_scaled,
    calculate_impact_score,
    get_news_contrast
)

# Initialisiert die Datenbank und legt die Tabelle für die Analyse-Daten an
def init_db():
    os.makedirs('data', exist_ok=True)
    conn = sqlite3.connect('data/gsi_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sentiment_data
                 (topic TEXT, country TEXT, social_presence REAL, likes REAL,
                  shares REAL, comments REAL, views REAL, sentiment_raw REAL,
                  news_presence REAL, impact_score REAL)''')
    conn.commit()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sentiment_data'")
    if c.fetchone():
        print("✅ Tabelle 'sentiment_data' erstellt oder vorhanden.")
    else:
        print("❌ Fehler: Tabelle 'sentiment_data' konnte nicht erstellt werden.")
    conn.close()

# Speichert die Daten als JSON (z.B. für Backups oder historische Analysen)
def save_to_json(data, filename='data/historical_data.json'):
    os.makedirs('data', exist_ok=True)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"✅ JSON-Datei gespeichert: {filename}")

# Speichert einen Datensatz in die Datenbank und berechnet alle Scores
def save_to_db(data):
    conn = sqlite3.connect('data/gsi_data.db')
    c = conn.cursor()
    # Berechne alle relevanten Scores für die Analyse
    presence_score = calculate_social_presence_score(data["social_presence"])
    visibility = calculate_social_visibility(presence_score)  # Engagement wird nicht genutzt
    visibility_factor = calculate_visibility_factor(visibility)
    sentiment_scaled = calculate_sentiment_scaled(data["sentiment_raw"])
    impact_score = calculate_impact_score(visibility_factor, sentiment_scaled)
    try:
        c.execute('''INSERT OR REPLACE INTO sentiment_data
                     (topic, country, social_presence, likes, shares, comments, views,
                      sentiment_raw, news_presence, impact_score)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (data["topic"], data["country"], data["social_presence"], data["likes"],
                   data["shares"], data["comments"], data["views"], data["sentiment_raw"],
                   data["news_presence"], impact_score))
        conn.commit()
        print(f"✅ Daten für {data['topic']} ({data['country']}) in DB gespeichert.")
    except sqlite3.Error as e:
        print(f"❌ Fehler beim Speichern in DB: {e}")
    conn.close()
    # Rückgabe der wichtigsten Scores für Kontrolle und Debugging
    return {
        "topic": data["topic"],
        "country": data["country"],
        "Social Presence Score": presence_score,
        "Social Visibility": visibility,
        "Social Visibility Factor": visibility_factor,
        "Sentiment (scaled)": sentiment_scaled,
        "\u279e Final Impact Score": impact_score,
        "News Contrast": get_news_contrast(presence_score, data["news_presence"])
    }

# Zeigt den aktuellen Inhalt der Datenbank an (für Kontrolle und Debugging)
def check_db():
    try:
        conn = sqlite3.connect('data/gsi_data.db')
        c = conn.cursor()
        c.execute("SELECT * FROM sentiment_data")
        rows = c.fetchall()
        if rows:
            print("\n📋 Datenbankinhalt (sentiment_data):")
            for row in rows:
                print(row)
        else:
            print("\n⚠️ Tabelle 'sentiment_data' ist leer.")
        conn.close()
    except sqlite3.Error as e:
        print(f"❌ Fehler beim Prüfen der DB: {e}")

# Beispiel-Testdaten für die Datenbank (verschiedene Länder und Themen, inkl. Extremwerte)
test_data = [
    {
        "topic": "Inflation",
        "country": "Germany",
        "social_presence": 0.75,
        "likes": 2000,
        "shares": 500,
        "comments": 300,
        "views": 100000,
        "sentiment_raw": 80.0,
        "news_presence": 0.4
    },
    {
        "topic": "Unemployment",
        "country": "France",
        "social_presence": 0.4,
        "likes": 100,
        "shares": 50,
        "comments": 20,
        "views": 1000,
        "sentiment_raw": 30.0,
        "news_presence": 0.9
    },
    {
        "topic": "Climate Change",
        "country": "USA",
        "social_presence": 0.3,
        "likes": 100,
        "shares": 50,
        "comments": 20,
        "views": 10000,
        "sentiment_raw": 50.0,
        "news_presence": 0.8
    },
    {
        "topic": "Healthcare",
        "country": "UK",
        "social_presence": 0.4,
        "likes": 160,
        "shares": 50,
        "comments": 20,
        "views": 5000,
        "sentiment_raw": 30.0,
        "news_presence": 0.7
    },
    {
        "topic": "Education",
        "country": "Canada",
        "social_presence": 0.4,
        "likes": 100,
        "shares": 50,
        "comments": 20,
        "views": 1000,
        "sentiment_raw": 30.0,
        "news_presence": 0.9
    },
    {
        "topic": "Immigration",
        "country": "Australia",
        "social_presence": 0.9,
        "likes": 1000,
        "shares": 500,
        "comments": 200,
        "views": 20000,
        "sentiment_raw": 5.0,
        "news_presence": 0.3
    },
    {
        "topic": "Mental Health",
        "country": "Sweden",
        "social_presence": 0.9,
        "likes": 1000,
        "shares": 100,
        "comments": 50,
        "views": 10000,
        "sentiment_raw": 30.0,
        "news_presence": 0.9
    },
    {
        "topic": "Climate Change",
        "country": "United States",
        "social_presence": 0.65,
        "likes": 1500,
        "shares": 400,
        "comments": 250,
        "views": 90000,
        "sentiment_raw": 70.0,
        "news_presence": 0.7
    },
    {
        "topic": "Healthcare",
        "country": "India",
        "social_presence": 0.55,
        "likes": 800,
        "shares": 300,
        "comments": 150,
        "views": 70000,
        "sentiment_raw": 60.0,
        "news_presence": 0.6
    },
    {
        "topic": "Education",
        "country": "Kenya",
        "social_presence": 0.35,
        "likes": 500,
        "shares": 100,
        "comments": 80,
        "views": 30000,
        "sentiment_raw": 75.0,
        "news_presence": 0.3
    },
    {
        "topic": "Unemployment",
        "country": "Spain",
        "social_presence": 0.45,
        "likes": 600,
        "shares": 200,
        "comments": 120,
        "views": 50000,
        "sentiment_raw": 40.0,
        "news_presence": 0.8
    },
    {
        "topic": "Crime",
        "country": "South Africa",
        "social_presence": 0.5,
        "likes": 700,
        "shares": 250,
        "comments": 200,
        "views": 60000,
        "sentiment_raw": 25.0,
        "news_presence": 0.85
    },
    # Extremwerte für Robustheitstests
    {
        "topic": "Corruption",
        "country": "Russia",
        "social_presence": 0.95,    # Sehr hohe Präsenz
        "likes": 5000,
        "shares": 4000,
        "comments": 3000,
        "views": 200000,
        "sentiment_raw": 10.0,      # Sehr negatives Sentiment
        "news_presence": 0.8
    },
    {
        "topic": "Space Exploration",
        "country": "USA",
        "social_presence": 0.1,     # Sehr niedrige Präsenz
        "likes": 50,
        "shares": 20,
        "comments": 10,
        "views": 5000,
        "sentiment_raw": 90.0,      # Sehr positives Sentiment
        "news_presence": 0.2
    },
    {
        "topic": "Technology Advances",
        "country": "Japan",
        "social_presence": 1.0,     # Maximale Präsenz
        "likes": 15000,
        "shares": 12000,
        "comments": 8000,
        "views": 500000,
        "sentiment_raw": 50.0,      # Neutrales Sentiment
        "news_presence": 1.0        # Maximal präsent in den Medien
    },
    {
        "topic": "Unemployment",
        "country": "Greece",
        "social_presence": 0.05,    # Sehr geringe Präsenz
        "likes": 0,
        "shares": 0,
        "comments": 0,
        "views": 100,
        "sentiment_raw": 5.0,       # Extrem negatives Sentiment
        "news_presence": 0.9        # Sehr starke Medienpräsenz
    }
]

# Hauptausführung: Initialisiert die DB, speichert Testdaten und zeigt Ergebnisse
if __name__ == "__main__":
    init_db()
    save_to_json(test_data)
    for data in test_data:
        result = save_to_db(data)
        print(f"\n📊 Topic: {result['topic']} ({result['country']})")
        for key, value in result.items():
            if key not in ["topic", "country"]:
                print(f"{key}: {value}")
    check_db()