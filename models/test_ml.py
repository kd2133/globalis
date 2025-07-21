from data_loader import load_data
from sentiment_analyzer import analyze_sentiment
from topic_analyzer import classify_topic

data = load_data("csv")
test_texts = [
         {"text": "Rising prices are hitting the economy in DE", "topic": "inflation", "country": "DE"},
         {"text": "Access to healthcare is improving in US", "topic": "environment", "country": "US"},
         {"text": "Economic growth is slow in UK", "topic": "economy", "country": "UK"},
         {"text": "Technology advances are boosting freedom in JP", "topic": "technology", "country": "JP"}
     ]
for d in test_texts:
         sentiment = analyze_sentiment(d["text"])
         topic = classify_topic(d["text"])
         print(f"Text: {d['text']}, Sentiment: {sentiment}, Topic: {topic}, Expected Topic: {d['topic']}")