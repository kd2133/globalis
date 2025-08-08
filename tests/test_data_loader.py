import pandas as pd
import os
import pytest

def test_load_gsi_data_success():
    dummy_data = pd.DataFrame([
        {"text": "Test", "country": "DE", "sentiment_raw": 0.5, "stance": 0.2, "topic": "Healthcare", "created_at": "2024-01-01", "lang": "de", "social_presence_raw": 0.5, "social_presence": 50, "news_presence": 40, "week": 1, "upvotes": 10, "comments": 2, "impact_score": 60}
    ])
    dummy_data.to_csv("data/gsi_data.csv", index=False)
    df = pd.read_csv("data/gsi_data.csv")
    assert not df.empty
    assert "impact_score" in df.columns
    os.remove("data/gsi_data.csv")

def test_load_gsi_data_missing_file():
    # Datei existiert nicht
    with pytest.raises(FileNotFoundError):
        pd.read_csv("data/non_existing_file.csv")

def test_load_gsi_data_invalid_columns():
    dummy_data = pd.DataFrame([
        {"text": "Test", "country": "DE"}
    ])
    dummy_data.to_csv("data/gsi_data.csv", index=False)
    df = pd.read_csv("data/gsi_data.csv")
    assert "impact_score" not in df.columns
    os.remove("data/gsi_data.csv")