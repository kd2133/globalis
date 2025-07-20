# Projektstruktur (kommentierte Architektur):
# .
#Globalis/
#├── main.py                  # Einstiegspunkt: Berechnet und zeigt den Global Sentiment Index (GSI)
#├── app.py                   # Streamlit-App für Visualisierung (UI)
#├── data_loader.py           # Lädt Daten aus DB, JSON oder CSV
#├── gsi_db_setup.py          # Setup-Script für SQLite-Datenbank (Tabellen, Testdaten)
#├── .env                     # API-Schlüssel und geheime Konfiguration (nicht ins Git!)
#├── requirements.txt         # Liste aller Python-Pakete, die das Projekt braucht
#├── README.md                # Überblick & Anleitung für Nutzer/Entwickler (GitHub-Visitenkarte)
#├── docs/                    # Detaillierte technische Dokumentation (Architektur, Konzepte)
#│   └── (z.B. architektur.md, datenfluss.md, to-do.md)
#├── models/
#│   ├── gsi_score.py         # Formel zur Berechnung des Impact Scores
#│   └── gsi_weighted.py      # Berechnung des gewichteten globalen GSI
#├── utils/
#│   └── helpers.py           # Hilfsfunktionen (z.B. für Berechnungen)
#├── data/
#│   ├── gsi_data.db          # SQLite-Datenbank mit Rohdaten
#│   └── historical_data.json # Beispiel-JSON mit historischen Daten
#└── venv/                    # Virtuelle Python-Umgebung (lokal, nicht in Git)


# main.py

import sys  # Für Kommandozeilen-Argumente
from data_loader import load_data  # Deine universelle Datenlade-Funktion
from models.gsi_score import calculate_gsi_impact  # Impact Score Formel
from models.gsi_weighted import calculate_weighted_gsi  # Gewichteten GSI berechnen

def main():
    # Standard-Datenquelle, die geladen wird, wenn nichts anderes angegeben ist
    source = 'db'  # Möglich: 'db', 'json', 'csv'

    # Prüfe, ob beim Starten ein Argument übergeben wurde (z.B. 'json' oder 'csv')
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()  # Argument in Kleinbuchstaben
        if arg in ('db', 'json', 'csv'):
            source = arg
        else:
            print(f"⚠️ Ungültige Quelle '{arg}' angegeben, verwende Standard 'db'.")

    print(f"📂 Datenquelle: {source}")

    # Lade die Daten aus der gewählten Quelle
    data = load_data(source=source)

    # Falls keine Daten geladen wurden, Programm abbrechen
    if not data:
        print("⚠️ Keine Daten geladen, Programm wird beendet.")
        return

    # Berechne Impact Score für alle Daten, bei denen er fehlt (None)
    for d in data:
        if d['impact_score'] is None:
            result = calculate_gsi_impact(d)
            d['impact_score'] = result.get("Final Impact Score")

    # Berechne den global gewichteten GSI aus allen Impact Scores
    gsi_weighted = calculate_weighted_gsi(data)

    # Ergebnisse ausgeben
    print("\n🌍 Global Sentiment Index (weighted):", gsi_weighted)
    print("===========================================")
    for d in data:
        print(f"{d['topic']} ({d['country']}): Impact Score={d['impact_score']}, Social Presence={d['social_presence']}")

if __name__ == "__main__":
    main()


