from transformers import pipeline

def classify_topic(text):
         try:
             classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
             topics = ["Healthcare Access and Quality", "Economic Inflation", "Personal Freedom and Rights"]
             result = classifier(text, topics, multi_label=False)
             return result["labels"][0].split(" ")[0]  # Extrahiere Hauptthema (z. B. "Healthcare")
         except Exception as e:
             print(f"❌ Fehler bei Themen-Klassifikation: {e}")
             return None