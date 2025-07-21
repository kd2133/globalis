import sqlite3

def clear_table():
    try:
        conn = sqlite3.connect('data/gsi_data.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS sentiment_data (topic TEXT, country TEXT, social_presence REAL, likes REAL, shares REAL, comments REAL, views REAL, sentiment_raw REAL, news_presence REAL, impact_score REAL)")
        c.execute("DELETE FROM sentiment_data")
        conn.commit()
        conn.close()
        print("✅ Tabelle 'sentiment_data' wurde geleert.")
    except sqlite3.Error as e:
        print(f"❌ Fehler beim Leeren der Tabelle: {e}")

if __name__ == "__main__":
    clear_table()