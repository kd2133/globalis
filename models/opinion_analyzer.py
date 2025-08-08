from transformers import pipeline

classifier = pipeline("text-classification", model="fine_tuned_opinion_model")

def analyze_opinion(text, threshold=0.65):
    result = classifier(text)[0]
    # Prüfe Label und Score
    if result["label"] == "LABEL_1" and result["score"] > threshold:
        return "Yes"
    else:
        return "No"