Version 3 To-Do-Liste

1. Multi-Topic-Erkennung pro Post (~2–3 Tage)


Ziel: Ermögliche, dass ein Post mehrere Themen (z. B. „Inflation + Steuern“) zugeordnet bekommt, basierend auf einem Multi-Label-Classifier.

Umsetzung:


Erweitere Version 2s Topic Classifier (distilbert-base-uncased) für Multi-Label-Klassifikation.


Trainingsdaten: ~1000–2000 Posts pro Thema-Kombination (manuell oder via LLM, z. B. Grok: https://x.ai/api).


Integriere in reddit_data.py:

from transformers import pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
text = "Die EZB erhöht Zinsen, Inflation steigt"
topics = ["Inflation", "Geldpolitik", "Healthcare"]
result = classifier(text, topics, multi_label=True)
# Ausgabe: {'labels': ['Inflation', 'Geldpolitik'], 'scores': [0.95, 0.90, 0.02]}

Nutzen: Realistischere Themenzuordnung, verbessert Stance/Sentiment-Präzision.


Priorität: Hoch, baut auf Version 2s Topic Classifier auf.

2. User-Tracking / Community-Heatmaps (~2–3 Tage)


Ziel: Visualisiere, welche Communities (z. B. Subreddits, X-Accounts) über Themen sprechen und wie ihre Stimmung ist (z. B. „r/economics negativ zu Inflation“).


Umsetzung:


Aggregiere Daten nach Community (Reddit: Subreddit, X: Hashtags) in reddit_data.py/news_data.py.


Erstelle Heatmaps mit plotly:

import plotly.express as px
df = pd.DataFrame({
    "subreddit": ["economics", "healthcare"],
    "topic": ["Inflation", "Healthcare"],
    "stance": [-0.5, 0.7]
})
fig = px.density_heatmap(df, x="subreddit", y="topic", z="stance")
fig.show()

Beachte Datenschutz (anonymisierte Nutzer-IDs).

Nutzen: Einblicke in Community-Dynamiken, ansprechende UI für app.py.


Priorität: Mittel, ergänzt interaktive UI.

3. Langzeit-Trends / Change Detection (~2–3 Tage)



Ziel: Analysiere Trends in Sentiment/Stance über Wochen/Monate (z. B. „Inflation-Stimmung verschlechtert sich seit Woche 29“).

Umsetzung:


Nutze pandas/statsmodels für Zeitreihenanalyse in gsi_score.py:

import pandas as pd
df = pd.read_csv("data/historical_gsi_data.csv")
trend = df.groupby(["week", "topic"])["stance"].mean().diff()
# Ausgabe: Trend-Änderungen pro Woche


Visualisiere in app.py mit plotly:

import plotly.express as px
fig = px.line(df, x="week", y="stance", color="topic")
fig.show()

Nutzen: Strategische Einblicke, z. B. für Governance-Reports.


Priorität: Hoch, nutzt bestehende Daten (historical_gsi_data.csv).

4. Ereignis-Extraktion (Event Detection) (~3–4 Tage)


Ziel: Identifiziere Schlüsselereignisse (z. B. „EZB erhöht Zinsen“) aus Posts/News für besseren Kontext.

Umsetzung:


Nutze spaCy oder BERT-basiertes Modell in news_data.py:

import spacy
nlp = spacy.load("en_core_web_sm")
text = "EZB erhöht Zinsen um 0.5%"
doc = nlp(text)
events = [(ent.text, ent.label_) for ent in doc.ents if ent.label_ in ["EVENT", "ORG"]]
# Ausgabe: [("EZB", "ORG"), ("Zinsen um 0.5%", "EVENT")]

Integriere Events in gsi_data.csv (neue Spalte: event).


Nutzen: Präzisere Stance/Sentiment durch Ereigniskontext.


Priorität: Hoch, besonders für NewsAPI-Daten.

5. Interaktive UI-Erweiterung (~2–3 Tage)


Ziel: Erweitere app.py mit interaktiven Filtern (Thema, Land, Zeitraum) und Dashboards.


Umsetzung:


Nutze streamlit oder dash:

import streamlit as st
topic = st.selectbox("Thema", ["Inflation", "Healthcare", "Freedom"])
df = pd.read_csv("data/gsi_data.csv")
st.dataframe(df[df["topic"] == topic][["text", "stance", "social_presence"]])


Füge Trend-Diagramme hinzu (siehe Langzeit-Trends).

Nutzen: Bessere Nutzererfahrung, zugänglichere Analysen.


Priorität: Mittel, verbessert Präsentation.

6. Automatisierte Datensammlung (~1–2 Tage)


Ziel: Automatisiere Reddit/News/X-Datenbeschaffung mit einem Scheduler.


Umsetzung:


Nutze schedule:

import schedule
import time
def fetch_data():
    # Rufe reddit_data.py/news_data.py
    pass
schedule.every().day.at("00:00").do(fetch_data)
while True:
    schedule.run_pending()
    time.sleep(60)

Integriere mit Version 2s Datenquellen (GNews, X API).

Nutzen: Kontinuierliche Daten, unterstützt Langzeit-Trends.


Priorität: Hoch, reduziert manuellen Aufwand.

7. Modell-Ensemble für Stance/Sentiment (~3–4 Tage)


Ziel: Kombiniere Modelle (z. B. cross-encoder/stsb-roberta-base + bert-base-multilingual) für robustere Werte.


Umsetzung:


Trainiere Ensemble mit transformers:

from transformers import pipeline
stance_model1 = pipeline("text-classification", model="cross-encoder/stsb-roberta-base")
stance_model2 = pipeline("text-classification", model="bert-base-multilingual-cased")
def ensemble_stance(text, topic):
    score1 = stance_model1(f"{text} Positive opinion on {topic}")[0]["score"]
    score2 = stance_model2(f"{text} Positive opinion on {topic}")[0]["score"]
    return (score1 + score2) / 2

Nutzen: Höhere Genauigkeit, weniger Bias.


Priorität: Mittel, baut auf Version 2s Modellverbesserungen.

8. Fehlerprotokollierung und Monitoring (~1–2 Tage)


Ziel: Detailliertes Logging und Monitoring (API-Ausfälle, Modellgenauigkeit).


Umsetzung:


Nutze sentry oder logging:

import logging
import sentry_sdk
sentry_sdk.init("dein_sentry_dsn")
logger = logging.getLogger(__name__)
try:
    # z. B. stance_analyzer.py
    pass
except Exception as e:
    logger.error(f"Fehler: {e}")
    sentry_sdk.capture_exception(e)



Nutzen: Stabilität, einfaches Debugging.



Priorität: Mittel, erhöht Zuverlässigkeit.

9. Graph-Analysen (optional, ~3–4 Tage)





Ziel: Visualisiere Beziehungen (z. B. „r/economics spricht negativ über EZB“) mit Netzwerkanalysen.

Umsetzung:

Nutze networkx:

import networkx as nx
G = nx.DiGraph()
G.add_edge("r/economics", "EZB", stance=-0.5)
nx.draw(G, with_labels=True)



Nutzen: Tiefere Einblicke in Community-Dynamiken.


Priorität: Niedrig, zu komplex für Version 3.

Gesamtaufwand: ~10–15 Tage (ohne Graph-Analysen: ~10–12 Tage).
Zeithorizont: 12–18 Monate (Juli 2026 – Januar 2027).
Priorität: Multi-Topic, Langzeit-Trends, Event Detection, Datensammlung zuerst. Graph-Analysen und GPT-Vision (hohe Kosten) optional.