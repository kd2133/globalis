from transformers import pipeline

def combine_all_factors(sentiment_score, toxicity_score, emotion_score, emotion_label):
         """Kombiniert Sentiment, Toxizität und Emotionen objektiv."""
         # Skaliere Toxizität auf -1 bis 0
         toxicity_adjustment = -toxicity_score  # 0 bis -1, direkt vom Modell
         
         # Skaliere Emotion auf -1 bis +1
         if emotion_label in ["joy", "love"]:
             emotion_adjustment = emotion_score  # 0 bis +1
         elif emotion_label in ["anger", "fear", "sadness"]:
             emotion_adjustment = -emotion_score  # 0 bis -1
         else:
             emotion_adjustment = 0.0  # Kein Einfluss für andere Emotionen (z. B. surprise)
         
         # Objektiver Durchschnitt
         final_score = (sentiment_score + toxicity_adjustment + emotion_adjustment) / 3
         
         # Begrenze auf -1 bis +1
         return max(min(final_score, 1.0), -1.0)

def analyze_sentiment(text):
         try:
             # Toxizitätsfilter mit unitary/toxic-bert
             toxicity_classifier = pipeline("text-classification", model="unitary/toxic-bert")
             toxicity_result = toxicity_classifier(text)[0]
             toxicity_score = toxicity_result["score"] if toxicity_result["label"] == "toxic" else 0.0
             if toxicity_score > 0.7:
                 print(f"⚠️ Toxischer Text erkannt: {text}")

             # Sentiment-Analyse mit cardiffnlp/twitter-roberta-base-sentiment
             sentiment_classifier = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")
             sentiment_result = sentiment_classifier(text)[0]
             if sentiment_result["label"] == "LABEL_2":  # Positiv
                 sentiment_score = sentiment_result["score"] * 2 - 1  # Skaliere auf 0 bis +1
             elif sentiment_result["label"] == "LABEL_0":  # Negativ
                 sentiment_score = -sentiment_result["score"] * 2 + 1  # Skaliere auf -1 bis 0
             else:  # Neutral
                 sentiment_score = 0.0

             # Emotionserkennung mit korrektem Modell
             emotion_classifier = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")
             emotion_result = emotion_classifier(text)[0]
             emotion_label = emotion_result["label"]
             emotion_score = emotion_result["score"]
             if emotion_label in ["joy", "love"] and emotion_score > 0.8:
                 print(f"🎉 Euphorischer Text erkannt: {text}")

             # Kombiniere alle Faktoren
             final_score = combine_all_factors(sentiment_score, toxicity_score, emotion_score, emotion_label)
             return final_score
         except Exception as e:
             print(f"❌ Fehler bei Sentiment-Analyse: {e}")
             return 0.0  # Default: neutral