from transformers import pipeline

# Lade dein Fine-Tuned-Modell (Ordner: "fine_tuned_model")
sentiment_classifier = pipeline("sentiment-analysis", model="fine_tuned_model")

def analyze_sentiment(text):
    try:
        result = sentiment_classifier(text)[0]
        return result["score"]  # -1 bis 1
    except Exception as e:
        print(f"❌ Fehler bei Sentiment-Analyse: {e}")
        return 0.0