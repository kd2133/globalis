from transformers import pipeline

# Modell und Pipeline nur einmal laden!
model_path = "fine_tuned_topic_model"
classifier = pipeline("text-classification", model=model_path)

topic_map = {
    0: "Migration",
    1: "Environment",
    2: "Safety",
    3: "Energy",
    4: "Inflation",
    5: "Other"
}

def analyze_topic(text):
    result = classifier(text)[0]
    label_idx = int(result["label"].split("_")[1])
    return topic_map.get(label_idx, "Other")