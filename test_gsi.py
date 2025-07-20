# tests/test_gsi.py
# Unittests für GSI-Kernfunktionen

import unittest
import os
import sys
from pathlib import Path

# Stelle sicher, dass Globalis/ im Python-Pfad ist
sys.path.append(str(Path(__file__).resolve().parent.parent))

try:
    from data_loader import load_data
    from models.gsi_score import calculate_gsi_impact
    from models.gsi_weighted import calculate_weighted_gsi
    from utils.helpers import get_news_contrast
except ImportError as e:
    raise ImportError(f"Fehler beim Importieren der Module: {e}")

class TestGSI(unittest.TestCase):
    def setUp(self):
        """Setup: Beispiel-Daten für Tests"""
        self.sample_data = [
            {
                "topic": "Inflation",
                "country": "Germany",
                "impact_score": None,
                "social_presence": 0.8,
                "sentiment_raw": 20.5,
                "news_presence": 0.6,
                "likes": 1000,
                "shares": 200,
                "comments": 150,
                "views": 5000
            },
            {
                "topic": "Climate Change",
                "country": "USA",
                "impact_score": None,
                "social_presence": 0.9,
                "sentiment_raw": 15.0,
                "news_presence": 0.7,
                "likes": 1200,
                "shares": 300,
                "comments": 200,
                "views": 6000
            }
        ]
        self.data_dir = "data"
        self.db_path = os.path.join(self.data_dir, "gsi_data.db")
        self.json_path = os.path.join(self.data_dir, "historical_data.json")

    def test_load_data_db(self):
        """Test: Datenladen aus SQLite"""
        if not os.path.exists(self.db_path):
            self.skipTest(f"DB-Datei {self.db_path} nicht gefunden")
        try:
            data = load_data(source="db")
            self.assertIsInstance(data, list, "Daten sollten eine Liste sein")
            self.assertGreater(len(data), 0, "Daten sollten nicht leer sein")
            required_keys = {"topic", "country", "social_presence", "sentiment_raw", "news_presence", "likes", "shares", "comments", "views"}
            for d in data:
                self.assertTrue(required_keys.issubset(d.keys()), f"Daten fehlen Schlüssel: {d}")
        except Exception as e:
            self.fail(f"Fehler beim Laden der DB-Daten: {e}")

    def test_load_data_json(self):
        """Test: Datenladen aus JSON"""
        if not os.path.exists(self.json_path):
            self.skipTest(f"JSON-Datei {self.json_path} nicht gefunden")
        try:
            data = load_data(source="json")
            self.assertIsInstance(data, list, "Daten sollten eine Liste sein")
            self.assertGreater(len(data), 0, "Daten sollten nicht leer sein")
        except Exception as e:
            self.fail(f"Fehler beim Laden der JSON-Daten: {e}")

    def test_calculate_gsi_impact(self):
        """Test: Impact Score-Berechnung"""
        try:
            data = self.sample_data[0]
            result = calculate_gsi_impact(data)
            self.assertIn("Final Impact Score", result, "Impact Score sollte berechnet werden")
            self.assertIsInstance(result["Final Impact Score"], float, "Impact Score sollte Float sein")
            self.assertGreaterEqual(result["Final Impact Score"], 0, "Impact Score sollte nicht negativ sein")
        except Exception as e:
            self.fail(f"Fehler bei Impact Score-Berechnung: {e}")

    def test_calculate_weighted_gsi(self):
        """Test: Gewichteter GSI"""
        try:
            for d in self.sample_data:
                d["impact_score"] = calculate_gsi_impact(d)["Final Impact Score"]
            gsi = calculate_weighted_gsi(self.sample_data)
            self.assertIsInstance(gsi, float, "GSI sollte Float sein")
            self.assertGreaterEqual(gsi, 0, "GSI sollte nicht negativ sein")
        except Exception as e:
            self.fail(f"Fehler bei GSI-Berechnung: {e}")

    def test_get_news_contrast(self):
        """Test: Kontrastfolie"""
        try:
            result = get_news_contrast(80.0, 60.0)  # social_presence * 100, news_presence * 100
            expected_values = [
                "Underreported",
                "Overreported",
                "Balanced",
                "Unknown",
                "Starkes Thema mit breiter medialer und öffentlicher Aufmerksamkeit ✔️"
            ]
            self.assertIn(result, expected_values, f"Ungültiger Kontrastwert: {result}")
        except Exception as e:
            self.fail(f"Fehler bei Kontrastfolie: {e}")

if __name__ == "__main__":
    unittest.main()