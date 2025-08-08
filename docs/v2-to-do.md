Version 2 To-Do-Liste

1. Topic Classifier (~1–2 Tage)

Ziel: Präzise Erkennung dominanter Themen (z. B. „Inflation“, „Healthcare“) statt Keyword-Filter.

Umsetzung:

Nutze distilbert-base-uncased oder facebook/bart-large-mnli (zero-shot).

Trainingsdaten: ~500–1000 gelabelte Posts pro Thema (manuell oder via LLM, z. B. Grok: https://x.ai/api).

Integriere in reddit_data.py vor stance_analyzer.py.

Nutzen: Reduziert Fehlzuordnungen (z. B. „I love my job“ → ignoriert).

2. LLM für explain_results.py (~1–2 Tage)


Ziel: Ersetze regelbasierte Erklärungen durch natürliche, kontextbezogene (z. B. „Warum ist Sentiment für Inflation gefallen?“).

Umsetzung:

Nutze Grok (via https://x.ai/api) oder GPT-4o/Claude.

Prompt-Engineering für „Was“, „Warum“, „Prognose“, „Folgen“, „Vorschläge“.

Beispiel:

import requests
def generate_llm_explanation(df, topic):
    prompt = f"Erkläre, warum das Sentiment für {topic} in Woche 30 bei {df['sentiment_raw'].mean():.2f} liegt."
    response = requests.post("https://x.ai/api/grok", json={"prompt": prompt}).json()
    return response["text"]



Nutzen: Dynamischere, nutzerfreundliche Erklärungen, skalierbar für interaktive UI.

3. Named Entity Recognition (NER) (~1 Tag)


Ziel: Erkenne relevante Akteure/Begriffe (z. B. „EZB“, „Inflation“, „Regierung“) für präzisere Relevanzfilterung.

Umsetzung:

Nutze spacy: pip install spacy, lade en_core_web_sm oder de_core_news_sm.

Integriere in reddit_data.py vor Stance-Analyse.

Beispiel:

import spacy
nlp = spacy.load("en_core_web_sm")
text = "Die EZB macht alles schlimmer"
doc = nlp(text)
entities = [ent.text for ent in doc.ents if ent.label_ in ["ORG", "GPE"]]



Nutzen: Genauerer Kontext (z. B. „EZB“ → „Geldpolitik“).

4. Feinere GSI-Aufschlüsselung (~1 Tag)


Ziel: Teile GSI in gsi_score.py in Komponenten: Sentiment, Stance, Social Presence, News Presence.


Umsetzung:


Erweitere gsi_score.py:

def calculate_gsi(df):
    return {
        "sentiment": df["sentiment_raw"].mean(),
        "stance": df["stance"].mean(),
        "social_presence": df["social_presence"].mean(),
        "news_presence": df["news_presence"].mean(),
        "gsi_total": df[["sentiment_raw", "stance", "social_presence", "news_presence"]].mean().mean()
    }

Passe app.py an, um Komponenten in Tabelle/Diagramm anzuzeigen.



Nutzen: Transparentere Analyse, bessere Visualisierung in UI.

5. Dynamische Themenlisten (~2–3 Stunden)


Ziel: Speichere Themen und Keywords in topics.json für flexible Erweiterung.



Umsetzung:


Erstelle topics.json:

{
  "Healthcare": ["healthcare", "hospital", "insurance"],
  "Inflation": ["inflation", "prices", "cost of living"],
  "Freedom": ["freedom", "liberty", "rights"]
}


Lade in reddit_data.py:

import json
with open("topics.json") as f:
    topic_keywords = json.load(f)



Nutzen: Neue Themen (z. B. „Klimawandel“) ohne Code-Änderungen.

6. Erweiterte Stance-Detektion (~1–2 Tage)


Ziel: Fange implizite Haltungen (z. B. „Die Regierung macht Fehler“ → negativ zu „Wirtschaftspolitik“) mit Few-Shot-Prompting oder Regeln.


Umsetzung:


Nutze LLM (z. B. Grok) oder erweitere stance_analyzer.py:

if "mistake" in text.lower() and any(e in text.lower() for e in ["government", "ezb"]):
    stance = -0.5
    topic = "Geldpolitik"



Nutzen: Präzisere Stance für komplexe Posts.

7. Neue Datenquellen (~2–3 Tage)


Ziel: Ergänze Reddit mit News-APIs (z. B. GNews, Mediastack) oder X (via API).



Umsetzung:



Integriere in news_data.py:

import requests
def fetch_gnews_data(topics, count=10):
    api_key = "dein_gnews_key"
    data = []
    for topic in topics:
        url = f"https://gnews.io/api/v4/search?q={topic}&token={api_key}&max={count}"
        response = requests.get(url).json()
        data.extend([{"title": a["title"], "published_at": a["publishedAt"], "lang": "en"} for a in response["articles"]])
    return data



API-Kosten prüfen (z. B. GNews: ~$0.01/100 Anfragen).


Nutzen: Vielfältigere Daten, robusteres news_presence.

8. Modellverbesserungen (~1 Woche, optional)



Ziel: Fine-Tune Sentiment- (cardiffnlp/twitter-roberta-base-sentiment) und Stance-Modelle (cross-encoder/stsb-roberta-base) für bessere Genauigkeit.

Umsetzung:


Sammle ~1000–2000 gelabelte Posts (manuell oder LLM).

Fine-Tuning mit transformers auf GPU (~8–12 Stunden).

Nutzen: Höhere Genauigkeit, aber hoher Aufwand.

Gesamtaufwand: ~5–10 Tage (ohne Modellverbesserungen: ~5–7 Tage).
Priorität: Topic Classifier, LLM, NER, GSI-Aufschlüsselung, Themenlisten zuerst. Multi-Topic und Modellverbesserungen optional für spätere Iterationen.