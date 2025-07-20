import sqlite3 ## Datenbank zurücksetzen

def clear_table():
    conn = sqlite3.connect('data/gsi_data.db')
    c = conn.cursor()
    c.execute("DELETE FROM sentiment_data")
    conn.commit()
    conn.close()
    print("✅ Tabelle 'sentiment_data' wurde geleert.")

if __name__ == "__main__":
    clear_table()
