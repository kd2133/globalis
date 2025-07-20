import sqlite3
import json
import csv
import os

def load_from_db(db_path='data/gsi_data.db'):
    """
    Lädt Daten aus der SQLite-Datenbank 'sentiment_data'.

    Args:
        db_path (str): Pfad zur SQLite-Datenbank (Standard: 'data/gsi_data.db').

    Returns:
        list: Liste von Dictionaries mit den Spalten topic, country, social_presence, likes, shares, comments, views,
              sentiment_raw, news_presence, impact_score.
              Gibt eine leere Liste zurück bei Fehlern oder wenn die Tabelle leer ist.
    """
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute(
            "SELECT topic, country, social_presence, likes, shares, comments, views, "
            "sentiment_raw, news_presence, impact_score FROM sentiment_data"
        )
        rows = c.fetchall()
        conn.close()

        if not rows:
            print(f"⚠️ Tabelle 'sentiment_data' in {db_path} ist leer.")
            return []

        columns = ["topic", "country", "social_presence", "likes", "shares", "comments", "views",
                   "sentiment_raw", "news_presence", "impact_score"]
        # Jede Zeile wird zu einem Dictionary mit Spaltennamen als Keys
        return [dict(zip(columns, row)) for row in rows]

    except sqlite3.Error as e:
        print(f"❌ Fehler beim Laden aus DB {db_path}: {e}")
        return []
    except FileNotFoundError:
        print(f"❌ Datenbank {db_path} nicht gefunden.")
        return []

def load_from_json(json_path='data/historical_data.json'):
    """
    Lädt Daten aus einer JSON-Datei.

    Args:
        json_path (str): Pfad zur JSON-Datei.

    Returns:
        list: Liste von Dictionaries mit den Daten.
              Gibt eine leere Liste zurück bei Fehlern oder wenn die Datei nicht gefunden wird.
    """
    try:
        if not os.path.exists(json_path):
            print(f"⚠️ JSON-Datei {json_path} nicht gefunden.")
            return []

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Prüfe, ob alle benötigten Keys in jedem Eintrag vorhanden sind
        required_keys = {"topic", "country", "social_presence", "likes", "shares", "comments",
                         "views", "sentiment_raw", "news_presence"}

        for d in data:
            if not all(key in d for key in required_keys):
                print(f"⚠️ Ungültiges JSON-Format in {json_path}. Fehlende Schlüssel in einem Eintrag.")
                return []

            # Konvertiere numerische Werte in float, setze sinnvolle Defaults falls leer
            d["social_presence"] = float(d["social_presence"] or 0)
            d["likes"] = float(d["likes"] or 0)
            d["shares"] = float(d["shares"] or 0)
            d["comments"] = float(d["comments"] or 0)
            d["views"] = float(d["views"] or 0)
            d["sentiment_raw"] = float(d["sentiment_raw"] or 50)
            d["news_presence"] = float(d["news_presence"] or 0)
            d["impact_score"] = float(d["impact_score"]) if d.get("impact_score") else None

        return data

    except json.JSONDecodeError as e:
        print(f"❌ Fehler beim Parsen von JSON {json_path}: {e}")
        return []
    except FileNotFoundError:
        print(f"❌ JSON-Datei {json_path} nicht gefunden.")
        return []

def load_from_csv(csv_path='data/gsi_data.csv'):
    """
    Lädt Daten aus einer CSV-Datei.

    Args:
        csv_path (str): Pfad zur CSV-Datei.

    Returns:
        list: Liste von Dictionaries mit den Daten.
              Gibt eine leere Liste zurück bei Fehlern oder wenn die Datei nicht gefunden wird.
    """
    try:
        if not os.path.exists(csv_path):
            print(f"⚠️ CSV-Datei {csv_path} nicht gefunden.")
            return []

        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = []

            required_keys = {"topic", "country", "social_presence", "likes", "shares", "comments",
                            "views", "sentiment_raw", "news_presence"}

            for row in reader:
                if not all(key in row for key in required_keys):
                    print(f"⚠️ Ungültiges CSV-Format in {csv_path}. Fehlende Schlüssel in einer Zeile.")
                    return []

                # Numerische Werte konvertieren und Defaults setzen
                row["social_presence"] = float(row["social_presence"] or 0)
                row["likes"] = float(row["likes"] or 0)
                row["shares"] = float(row["shares"] or 0)
                row["comments"] = float(row["comments"] or 0)
                row["views"] = float(row["views"] or 0)
                row["sentiment_raw"] = float(row["sentiment_raw"] or 50)
                row["news_presence"] = float(row["news_presence"] or 0)
                row["impact_score"] = float(row["impact_score"]) if row.get("impact_score") else None

                data.append(row)

        return data

    except Exception as e:
        print(f"❌ Fehler beim Laden von CSV {csv_path}: {e}")
        return []

def load_data(source='db', db_path='data/gsi_data.db', json_path='data/historical_data.json', csv_path='data/gsi_data.csv'):
    """
    Universelle Funktion zum Laden von Daten aus verschiedenen Quellen.

    Args:
        source (str): Datenquelle, möglich sind 'db', 'json' oder 'csv'.
        db_path (str): Pfad zur SQLite-Datenbank.
        json_path (str): Pfad zur JSON-Datei.
        csv_path (str): Pfad zur CSV-Datei.

    Returns:
        list: Liste von Dictionaries mit den geladenen Daten.
              Leere Liste, falls Quelle ungültig oder Fehler auftreten.
    """
    if source == 'db':
        data = load_from_db()
    elif source == 'json':
        data = load_from_json()
    elif source == 'csv':
        data = load_from_csv()
    else:
        print("Ungültige Quelle")
        return []

    print(f"✅ {len(data)} Einträge aus Quelle '{source}' geladen.")
    return data


    
    