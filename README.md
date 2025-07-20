## Global Sentiment Index (GSI)

## Überblick

Der Global Sentiment Index (GSI) ist eine bahnbrechende Plattform, die globale Stimmungen zu Themen wie Wirtschaft, Umwelt oder soziale Gerechtigkeit in Echtzeit erfasst, mit dynamischer Datenanalyse, interaktiver Visualisierung und KI-gestützter Erkennung von Zufriedenheit, Sorgen, Angst und Panik, um Regierungen, Organisationen und Entscheidungsträger weltweit mit fairen, transparenten Einblicken zu befähigen, eine bessere Zukunft zu gestalten.


## Vision

Fair, transparent, universell – weltweite Stimmungen wie Zufriedenheit, Sorgen, Angst und Panik in Echtzeit messen und verstehen.


## Hauptmerkmale

Echtzeit-Analyse: Erfassung und Bewertung globaler Stimmungen zu vielfältigen Themen.
Interaktive Visualisierung: Intuitive Web-Oberfläche mit Diagrammen, Filtern und Kontrastanalysen (z. B. Unterschiede zwischen sozialer und medialer Wahrnehmung).
KI-gestützte Erkenntnisse: Automatische Erkennung von Stimmungen (z. B. Zufriedenheit, Angst) und neuen Themen durch maschinelles Lernen.
Flexible Datenquellen: Unterstützt verschiedene Formate für universelle Anwendbarkeit.
Skalierbarkeit: Bereit für Echtzeit-Datenintegration (z. B. soziale Medien).


## Nutzen

Für Entscheidungsträger: Erkennt globale Trends und gesellschaftliche Prioritäten für datenbasierte Entscheidungen.
Für Organisationen: Fördert Transparenz und Fairness durch objektive Stimmungsanalysen.
Für die Welt: Unterstützt nachhaltige Lösungen durch tiefes Verständnis globaler Stimmungen.


## Installation

Erstelle ein virtuelles Environment:python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate


## Installiere Abhängigkeiten:

pip install streamlit pandas plotly transformers scikit-learn tweepy numpy


## Optional für erweiterte Features:

(z. B. Web-Scraping, Excel-Export):pip install matplotlib seaborn openpyxl beautifulsoup4 requests python-dotenv



## Verwendung

Konsole: Führe python main.py [db/json/csv] aus, um Stimmungen und GSI in der Konsole zu analysieren.
Web-Oberfläche: Starte streamlit run app.py für interaktive Visualisierung mit Filtern, Diagrammen und Kontrastanalysen.



## Projektstruktur

main.py: Hauptprogramm für die GSI-Berechnung
app.py: Streamlit-App für interaktive Visualisierung
data_loader.py: Lädt Daten aus DB, JSON oder CSV
gsi_db_setup.py: Erstellt und füllt die SQLite-Datenbank
.env: Versteckte Datei für API-Schlüssel und geheime Einstellungen
requirements.txt: Liste aller benötigten Python-Pakete
README.md: Diese Datei
docs/: Technische Dokumentation und weitere Informationen
models/: Berechnung der Impact Scores
utils/: Hilfsfunktionen
data/: Rohdaten (DB, JSON)
venv/: Virtuelle Python-Umgebung (nicht versioniert)


## Weitere Hinweise

.env: Hier kannst du sensible Informationen wie API-Keys speichern. Diese Datei wird nicht ins öffentliche Repository hochgeladen.
requirements.txt: Falls du Pakete manuell installierst, kannst du mit pip freeze > requirements.txt deine Paketliste aktualisieren.
venv/: Diese Ordner enthält die isolierte Python-Umgebung und sollte nicht im Git gespeichert werden.


## Mitmachen

Falls du Fehler findest oder Features vorschlagen willst, öffne gerne ein Issue oder Pull Request.

