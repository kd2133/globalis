from models.sentiment_analyzer import analyze_sentiment
from models.stance_analyzer import analyze_stance

def test_analyze_sentiment_range():
    val = analyze_sentiment("Das ist schlecht")
    assert -1.0 <= val <= 1.0
    val2 = analyze_sentiment("Das ist gut")
    assert -1.0 <= val2 <= 1.0

def test_analyze_stance_range():
    val = analyze_stance("Ich bin dagegen", "Inflation")
    assert -1.0 <= val <= 1.0
    val2 = analyze_stance("Ich bin dafür", "Healthcare")
    assert -1.0 <= val2 <= 1.0

def test_analyze_sentiment_empty():
    val = analyze_sentiment("")
    assert -1.0 <= val <= 1.0

def test_analyze_stance_empty():
    val = analyze_stance("", "Inflation")
    assert -1.0 <= val <= 1.0

def test_social_presence_calculation():
    from utils.globalis_pipeline import process_posts_pipeline
    posts = [
        {"text": "Prices are rising everywhere!", "lang": "en"},
        {"text": "I am worried about inflation.", "lang": "en"}
    ]
    df = process_posts_pipeline(posts, selected_topics=["Inflation"])
    assert df["social_presence_raw"].iloc[0] == 1 / 2  # 1 Post von 2 für Inflation
    assert 0 < df["social_presence"].iloc[0] <= 100
    assert df["topic"].iloc[0] == "Inflation"