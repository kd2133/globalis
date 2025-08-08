import pytest
import pandas as pd
from unittest.mock import patch
from utils.globalis_pipeline import GlobalisPipeline
from utils.explain_results import explain_topic_result
from utils.helpers import calculate_combined_score

@pytest.fixture
def pipeline():
    return GlobalisPipeline()

@pytest.fixture
def mock_posts():
    return [
        "New safety regulations are a joke, accidents still happening!",  # Safety
        "Inflation is killing us, prices up 10% in a month!",  # Inflation
        "Why isn’t anyone doing more for the environment?",  # Environment
        "Migration policies are failing, borders are a mess.",  # Migration
        "Energy costs are through the roof, need renewables now!",  # Energy
        "Crime rates are up, where’s the safety we were promised?",  # Safety
        "Can’t afford groceries anymore, inflation is out of control!",  # Inflation
        "Climate change is real, floods ruined my town.",  # Environment
        "We need better integration for migrants, this isn’t working.",  # Migration
        "Solar energy is the only way forward, fossil fuels suck.",  # Energy
        "Streets feel unsafe at night, what’s the government doing?",  # Safety
        "My rent went up again, thanks to inflation!",  # Inflation
        "Protecting our planet should be priority one!",  # Environment
        "Migration numbers are stable, but tensions are high.",  # Migration
        "Wind turbines are saving us money, more please!",  # Energy
        "Safety report shows no improvement, so frustrating.",  # Safety
        "Inflation forecast is grim, no relief in sight.",  # Inflation
        "Deforestation is killing our ecosystems, act now!",  # Environment
        "Refugee crisis is getting worse, need solutions.",  # Migration
        "Renewable energy is the future, let’s invest!",  # Energy
        # Weitere realistische Posts (80 weitere, für insgesamt 100)
        "Can’t believe gas prices, inflation is insane!",  # Inflation
        "More solar farms needed, energy bills are too high!",  # Energy
        "Climate protests are growing, people are fed up.",  # Environment
        "Border security is a mess, migration policies failing.",  # Migration
        "Safety measures in schools are not enough!",  # Safety
        "Groceries cost a fortune now, thanks inflation.",  # Inflation
        "Loving the new wind energy project in my town!",  # Energy
        "Pollution is out of control, save our rivers!",  # Environment
        "Migrants need support, not walls.",  # Migration
        "Crime stats are worrying, safety first!",  # Safety
        "Inflation is eating my savings, help!",  # Inflation
        "Solar panels are a game-changer for energy costs.",  # Energy
        "Why no action on climate? It’s urgent!",  # Environment
        "Migration debates are so heated right now.",  # Migration
        "Feeling unsafe walking home, more police needed.",  # Safety
        "Prices for everything are up, inflation sucks!",  # Inflation
        "Renewables are the only way to save energy costs.",  # Energy
        "Air quality is terrible, environment needs help.",  # Environment
        "Integration programs for migrants are failing.",  # Migration
        "Safety concerns in my neighborhood are real.",  # Safety
        "Can’t keep up with rising costs, inflation is brutal!",  # Inflation
        "Energy transition to renewables is too slow!",  # Energy
        "Climate change is hitting us hard, floods everywhere.",  # Environment
        "Migration policies need a complete overhaul.",  # Migration
        "Safety patrols aren’t enough, crime is up.",  # Safety
        "Inflation is making life unaffordable!",  # Inflation
        "Wind energy is great, but we need more!",  # Energy
        "Our forests are disappearing, save the environment!",  # Environment
        "Migrant camps are overcrowded, do something!",  # Migration
        "Safety issues are ignored, people are scared.",  # Safety
        "Inflation is ruining small businesses!",  # Inflation
        "Energy prices are crazy, renewables now!",  # Energy
        "Climate change is a crisis, act faster!",  # Environment
        "Migration rules are too strict, need balance.",  # Migration
        "No one feels safe here anymore, fix it!",  # Safety
        "Can’t afford rent, inflation is killing me!",  # Inflation
        "Solar power is amazing, let’s expand it!",  # Energy
        "Environment is in trouble, stop ignoring it!",  # Environment
        "Migrant crisis needs urgent attention.",  # Migration
        "Safety stats are alarming, take action!",  # Safety
        "Inflation is out of hand, prices are nuts!",  # Inflation
        "Energy costs are killing us, go renewable!",  # Energy
        "Climate change is destroying our crops!",  # Environment
        "Migration policies aren’t working, chaos!",  # Migration
        "Safety is a big issue, more needs to be done.",  # Safety
        "Inflation makes everything so expensive!",  # Inflation
        "Renewable energy is our only hope!",  # Energy
        "Pollution is choking our cities, act now!",  # Environment
        "Migrants deserve better treatment, fix it!",  # Migration
        "Crime is up, where’s the safety plan?",  # Safety
        "Inflation is crushing families, help us!",  # Inflation
        "Energy bills are insane, renewables please!",  # Energy
        "Climate change is scary, we need action!",  # Environment
        "Migration system is broken, reform it!",  # Migration
        "Safety concerns are growing, do something!",  # Safety
        "Can’t afford basics anymore, inflation!",  # Inflation
        "Solar energy is the way to go!",  # Energy
        "Environment needs saving, stop delays!",  # Environment
        "Migration issues are causing tension.",  # Migration
        "Safety is getting worse, help!",  # Safety
        "Inflation is a nightmare, prices soaring!",  # Inflation
        "Energy prices are too high, go green!",  # Energy
        "Climate change is real, save our planet!",  # Environment
        "Migration policies need to change now!",  # Migration
        "Safety is a priority, act fast!",  # Safety
        "Inflation is killing my budget!",  # Inflation
        "Renewables are the future, invest now!",  # Energy
        "Environment is in crisis, do something!",  # Environment
        "Migration crisis is out of control!",  # Migration
        "Safety measures aren’t working, fix it!",  # Safety
        "Prices are crazy, inflation is brutal!",  # Inflation
        "Energy costs are insane, renewables now!",  # Energy
        "Climate change is urgent, act today!",  # Environment
        "Migration needs better solutions!",  # Migration
        "Safety is a huge concern, help us!",  # Safety
    ]

@pytest.fixture
def mock_sentiments():
    return {
        "New safety regulations are a joke, accidents still happening!": -0.7,
        "Inflation is killing us, prices up 10% in a month!": -0.9,
        "Why isn’t anyone doing more for the environment?": -0.6,
        "Migration policies are failing, borders are a mess.": -0.8,
        "Energy costs are through the roof, need renewables now!": -0.5,
        "Crime rates are up, where’s the safety we were promised?": -0.65,
        "Can’t afford groceries anymore, inflation is out of control!": -0.85,
        "Climate change is real, floods ruined my town.": -0.75,
        "We need better integration for migrants, this isn’t working.": -0.55,
        "Solar energy is the only way forward, fossil fuels suck.": 0.8,
        "Streets feel unsafe at night, what’s the government doing?": -0.6,
        "My rent went up again, thanks to inflation!": -0.8,
        "Protecting our planet should be priority one!": 0.7,
        "Migration numbers are stable, but tensions are high.": -0.3,
        "Wind turbines are saving us money, more please!": 0.75,
        "Safety report shows no improvement, so frustrating.": -0.5,
        "Inflation forecast is grim, no relief in sight.": -0.9,
        "Deforestation is killing our ecosystems, act now!": -0.65,
        "Refugee crisis is getting worse, need solutions.": -0.7,
        "Renewable energy is the future, let’s invest!": 0.85,
        # Weitere Sentiments (80 weitere, realistisch verteilt)
        "Can’t believe gas prices, inflation is insane!": -0.85,
        "More solar farms needed, energy bills are too high!": -0.5,
        "Climate protests are growing, people are fed up.": -0.6,
        "Border security is a mess, migration policies failing.": -0.75,
        "Safety measures in schools are not enough!": -0.65,
        "Groceries cost a fortune now, thanks inflation.": -0.9,
        "Loving the new wind energy project in my town!": 0.7,
        "Pollution is out of control, save our rivers!": -0.7,
        "Migrants need support, not walls.": 0.4,
        "Crime stats are worrying, safety first!": -0.6,
        "Inflation is eating my savings, help!": -0.85,
        "Solar panels are a game-changer for energy costs.": 0.75,
        "Why no action on climate? It’s urgent!": -0.65,
        "Migration debates are so heated right now.": -0.4,
        "Feeling unsafe walking home, more police needed.": -0.55,
        "Prices for everything are up, inflation sucks!": -0.9,
        "Renewables are the only way to save energy costs.": 0.65,
        "Air quality is terrible, environment needs help.": -0.7,
        "Integration programs for migrants are failing.": -0.6,
        "Safety concerns in my neighborhood are real.": -0.65,
        "Can’t keep up with rising costs, inflation is brutal!": -0.85,
        "Energy transition to renewables is too slow!": -0.5,
        "Climate change is hitting us hard, floods everywhere.": -0.75,
        "Migration policies need a complete overhaul.": -0.7,
        "Safety patrols aren’t enough, crime is up.": -0.6,
        "Inflation is making life unaffordable!": -0.9,
        "Wind energy is great, but we need more!": 0.7,
        "Our forests are disappearing, save the environment!": -0.65,
        "Migrant camps are overcrowded, do something!": -0.7,
        "Safety issues are ignored, people are scared.": -0.65,
        "Inflation is ruining small businesses!": -0.85,
        "Energy prices are crazy, renewables now!": -0.5,
        "Climate change is a crisis, act faster!": -0.75,
        "Migration rules are too strict, need balance.": -0.4,
        "No one feels safe here anymore, fix it!": -0.6,
        "Can’t afford rent, inflation is killing me!": -0.9,
        "Solar power is amazing, let’s expand it!": 0.8,
        "Environment is in trouble, stop ignoring it!": -0.7,
        "Migrant crisis needs urgent attention.": -0.65,
        "Safety stats are alarming, take action!": -0.6,
        "Inflation is out of hand, prices are nuts!": -0.85,
        "Energy costs are too high, go renewable!": -0.5,
        "Climate change is scary, we need action!": -0.75,
        "Migration system is broken, reform it!": -0.7,
        "Safety concerns are growing, do something!": -0.65,
        "Can’t afford basics anymore, inflation!": -0.9,
        "Solar energy is the way to go!": 0.75,
        "Environment needs saving, stop delays!": -0.7,
        "Migration issues are causing tension.": -0.4,
        "Safety is getting worse, help!": -0.6,
        "Inflation is a nightmare, prices soaring!": -0.85,
        "Energy prices are too high, go green!": -0.5,
        "Climate change is real, save our planet!": -0.75,
        "Migration policies need to change now!": -0.7,
        "Safety is a priority, act fast!": -0.65,
        "Inflation is killing my budget!": -0.9,
        "Renewables are the future, invest now!": 0.8,
        "Environment is in crisis, do something!": -0.7,
        "Migration crisis is out of control!": -0.65,
        "Safety measures aren’t working, fix it!": -0.6,
        "Prices are crazy, inflation is brutal!": -0.85,
        "Energy costs are insane, renewables now!": -0.5,
        "Climate change is urgent, act today!": -0.75,
        "Migration needs better solutions!": -0.7,
        "Safety is a huge concern, help us!": -0.65,
        "Inflation is crushing families, help us!": -0.9,
        "Energy bills are insane, renewables please!": -0.5,
        "Climate change is scary, we need action!": -0.75,
        "Migration system is broken, reform it!": -0.7,
        "Safety concerns are growing, do something!": -0.65,
        "Can’t afford basics anymore, inflation!": -0.9,
        "Solar energy is the way to go!": 0.75,
        "Environment needs saving, stop delays!": -0.7,
        "Migration issues are causing tension.": -0.4,
        "Safety is getting worse, help!": -0.6,
        "Inflation is a nightmare, prices soaring!": -0.85,
        "Energy prices are too high, go green!": -0.5,
        "Climate change is real, save our planet!": -0.75,
        "Migration policies need to change now!": -0.7,
        "Safety is a priority, act fast!": -0.65,
        "Inflation is killing my budget!": -0.9,
        "Renewables are the future, invest now!": 0.8,
        "Environment is in crisis, do something!": -0.7,
        "Migration crisis is out of control!": -0.65,
        "Safety measures aren’t working, fix it!": -0.6,
        "Prices are crazy, inflation is brutal!": -0.85,
        "Energy costs are insane, renewables now!": -0.5,
        "Climate change is urgent, act today!": -0.75,
        "Migration needs better solutions!": -0.7,
        "Safety is a huge concern, help us!": -0.65
    }

def test_pipeline_logic(pipeline, mock_posts, mock_sentiments):
    with patch('models.topic_analyzer.analyze_topic') as mock_topic, \
         patch('models.opinion_analyzer.analyze_opinion') as mock_opinion, \
         patch('models.sentiment_analyzer.analyze_sentiment') as mock_sentiment, \
         patch('utils.helpers.load_historical_stats') as mock_stats:
        
        topic_map = {
            "New safety regulations are a joke, accidents still happening!": "Safety",
            "Inflation is killing us, prices up 10% in a month!": "Inflation",
            "Why isn’t anyone doing more for the environment?": "Environment",
            "Migration policies are failing, borders are a mess.": "Migration",
            "Energy costs are through the roof, need renewables now!": "Energy",
            "Crime rates are up, where’s the safety we were promised?": "Safety",
            "Can’t afford groceries anymore, inflation is out of control!": "Inflation",
            "Climate change is real, floods ruined my town.": "Environment",
            "We need better integration for migrants, this isn’t working.": "Migration",
            "Solar energy is the only way forward, fossil fuels suck.": "Energy",
            "Streets feel unsafe at night, what’s the government doing?": "Safety",
            "My rent went up again, thanks to inflation!": "Inflation",
            "Protecting our planet should be priority one!": "Environment",
            "Migration numbers are stable, but tensions are high.": "Migration",
            "Wind turbines are saving us money, more please!": "Energy",
            "Safety report shows no improvement, so frustrating.": "Safety",
            "Inflation forecast is grim, no relief in sight.": "Inflation",
            "Deforestation is killing our ecosystems, act now!": "Environment",
            "Refugee crisis is getting worse, need solutions.": "Migration",
            "Renewable energy is the future, let’s invest!": "Energy",
            "Can’t believe gas prices, inflation is insane!": "Inflation",
            "More solar farms needed, energy bills are too high!": "Energy",
            "Climate protests are growing, people are fed up.": "Environment",
            "Border security is a mess, migration policies failing.": "Migration",
            "Safety measures in schools are not enough!": "Safety",
            "Groceries cost a fortune now, thanks inflation.": "Inflation",
            "Loving the new wind energy project in my town!": "Energy",
            "Pollution is out of control, save our rivers!": "Environment",
            "Migrants need support, not walls.": "Migration",
            "Crime stats are worrying, safety first!": "Safety",
            "Inflation is eating my savings, help!": "Inflation",
            "Solar panels are a game-changer for energy costs.": "Energy",
            "Why no action on climate? It’s urgent!": "Environment",
            "Migration debates are so heated right now.": "Migration",
            "Feeling unsafe walking home, more police needed.": "Safety",
            "Prices for everything are up, inflation sucks!": "Inflation",
            "Renewables are the only way to save energy costs.": "Energy",
            "Air quality is terrible, environment needs help.": "Environment",
            "Integration programs for migrants are failing.": "Migration",
            "Safety concerns in my neighborhood are real.": "Safety",
            "Can’t keep up with rising costs, inflation is brutal!": "Inflation",
            "Energy transition to renewables is too slow!": "Energy",
            "Climate change is hitting us hard, floods everywhere.": "Environment",
            "Migration policies need a complete overhaul.": "Migration",
            "Safety patrols aren’t enough, crime is up.": "Safety",
            "Inflation is making life unaffordable!": "Inflation",
            "Wind energy is great, but we need more!": "Energy",
            "Our forests are disappearing, save the environment!": "Environment",
            "Migrant camps are overcrowded, do something!": "Migration",
            "Safety issues are ignored, people are scared.": "Safety",
            "Inflation is ruining small businesses!": "Inflation",
            "Energy prices are crazy, renewables now!": "Energy",
            "Climate change is a crisis, act faster!": "Environment",
            "Migration rules are too strict, need balance.": "Migration",
            "No one feels safe here anymore, fix it!": "Safety",
            "Can’t afford rent, inflation is killing me!": "Inflation",
            "Solar power is amazing, let’s expand it!": "Energy",
            "Environment is in trouble, stop ignoring it!": "Environment",
            "Migrant crisis needs urgent attention.": "Migration",
            "Safety stats are alarming, take action!": "Safety",
            "Inflation is out of hand, prices are nuts!": "Inflation",
            "Energy costs are too high, go renewable!": "Energy",
            "Climate change is scary, we need action!": "Environment",
            "Migration system is broken, reform it!": "Migration",
            "Safety concerns are growing, do something!": "Safety",
            "Can’t afford basics anymore, inflation!": "Inflation",
            "Solar energy is the way to go!": "Energy",
            "Environment needs saving, stop delays!": "Environment",
            "Migration issues are causing tension.": "Migration",
            "Safety is getting worse, help!": "Safety",
            "Inflation is a nightmare, prices soaring!": "Inflation",
            "Energy prices are too high, go green!": "Energy",
            "Climate change is real, save our planet!": "Environment",
            "Migration policies need to change now!": "Migration",
            "Safety is a priority, act fast!": "Safety",
            "Inflation is killing my budget!": "Inflation",
            "Renewables are the future, invest now!": "Energy",
            "Environment is in crisis, do something!": "Environment",
            "Migration crisis is out of control!": "Migration",
            "Safety measures aren’t working, fix it!": "Safety",
            "Prices are crazy, inflation is brutal!": "Inflation",
            "Energy costs are insane, renewables now!": "Energy",
            "Climate change is urgent, act today!": "Environment",
            "Migration needs better solutions!": "Migration",
            "Safety is a huge concern, help us!": "Safety",
            "Inflation is crushing families, help us!": "Inflation",
            "Energy bills are insane, renewables please!": "Energy",
            "Climate change is scary, we need action!": "Environment",
            "Migration system is broken, reform it!": "Migration",
            "Safety concerns are growing, do something!": "Safety",
            "Can’t afford basics anymore, inflation!": "Inflation",
            "Solar energy is the way to go!": "Energy",
            "Environment needs saving, stop delays!": "Environment",
            "Migration issues are causing tension.": "Migration",
            "Safety is getting worse, help!": "Safety",
            "Inflation is a nightmare, prices soaring!": "Inflation",
            "Energy prices are too high, go green!": "Energy",
            "Climate change is real, save our planet!": "Environment",
            "Migration policies need to change now!": "Migration",
            "Safety is a priority, act fast!": "Safety"
        }
        
        # Mock historical stats mit med_rel=0.1667 für Safety, Environment, Migration und 0.25 für Inflation, Energy
        mock_stats.return_value = {
            topic: {'min_rel': 0.01, 'med_rel': 0.16666666666666666, 'max_rel': 0.5, 'history': []}
            for topic in ['Safety', 'Environment', 'Migration']
        }
        mock_stats.return_value.update({
            'Inflation': {'min_rel': 0.01, 'med_rel': 0.25, 'max_rel': 0.5, 'history': []},
            'Energy': {'min_rel': 0.01, 'med_rel': 0.25, 'max_rel': 0.5, 'history': []}
        })
        
        mock_topic.side_effect = lambda x: topic_map[x]
        mock_opinion.return_value = True
        mock_sentiment.side_effect = lambda x: mock_sentiments[x]

        df, gsi_weighted, total_analyzed = pipeline.run(mock_posts)

        # Grundlegende Konsistenz
        assert len(df) == 100, f"Erwartete 100 Posts, aber {len(df)} gefunden"
        assert total_analyzed == 100, f"Erwartete 100 analysierte Posts, aber {total_analyzed} gefunden"
        assert set(df['topic'].unique()) == set(pipeline.selected_topics), "Nicht alle Topics vertreten"

        # Topic- und Sentiment-Konsistenz
        for _, row in df.iterrows():
            post = row['text']
            assert row['topic'] == topic_map[post], f"Falsches Topic für '{post}': Erwartet {topic_map[post]}, erhalten {row['topic']}"
            assert abs(row['sentiment'] - mock_sentiments[post]) < 0.0001, \
                   f"Falsches Sentiment für '{post}': Erwartet {mock_sentiments[post]}, erhalten {row['sentiment']}"

        # Impact Score Logik
        for _, row in df.iterrows():
            post, topic, sentiment, presence_ratio, impact_score = row['text'], row['topic'], row['sentiment'], row['presence_ratio'], row['impact_score']
            topic_stats = mock_stats.return_value[topic]
            min_rel, med_rel, max_rel = topic_stats['min_rel'], topic_stats['med_rel'], topic_stats['max_rel']
            
            # Dynamisch berechneter Impact Score
            calculated_score = calculate_combined_score(presence_ratio, min_rel, med_rel, max_rel, sentiment)
            assert abs(impact_score - calculated_score) < 0.1, \
                   f"Impact Score für '{post}' falsch: Erwartet {calculated_score:.2f}, erhalten {impact_score:.2f}"
            
            # Logik-Checks
            assert 0 <= impact_score <= 100, f"Impact Score für '{post}' außerhalb [0, 100]: {impact_score}"
            if abs(sentiment) < 0.1:
                assert abs(impact_score - 50.0) < 5, f"Neutraler Sentiment ({sentiment:.2f}) für '{post}' sollte Score ≈ 50 haben: {impact_score}"
            elif sentiment > 0.3:
                assert impact_score > 50, f"Positiver Sentiment ({sentiment:.2f}) für '{post}' sollte Score > 50 haben: {impact_score}"
            elif sentiment < -0.3:
                assert impact_score < 50, f"Negativer Sentiment ({sentiment:.2f}) für '{post}' sollte Score < 50 haben: {impact_score}"

        # Stance Logik
        for _, row in df.iterrows():
            sentiment, stance = row['sentiment'], row['stance']
            if sentiment < -0.3:
                assert stance == "Contra", f"Falsche Stance für Sentiment {sentiment:.2f}: Erwartet Contra, erhalten {stance}"
            elif sentiment > 0.3:
                assert stance == "Pro", f"Falsche Stance für Sentiment {sentiment:.2f}: Erwartet Pro, erhalten {stance}"
            else:
                assert stance == "Neutral", f"Falsche Stance für Sentiment {sentiment:.2f}: Erwartet Neutral, erhalten {stance}"

        # Topic-Aggregation
        topic_results = []
        topic_counts = df['topic'].value_counts().to_dict()
        for topic in pipeline.selected_topics:
            topic_df = df[df['topic'] == topic]
            if not topic_df.empty:
                expected_presence_ratio = topic_counts[topic] / total_analyzed
                assert abs(topic_df['presence_ratio'].iloc[0] - expected_presence_ratio) < 0.0001, \
                       f"Falsche Presence Ratio für {topic}: Erwartet {expected_presence_ratio:.4f}, erhalten {topic_df['presence_ratio'].iloc[0]:.4f}"
                avg_impact_score = topic_df['impact_score'].mean()
                topic_results.append({
                    'topic': topic,
                    'presence_ratio': topic_df['presence_ratio'].iloc[0],
                    'avg_impact_score': avg_impact_score
                })

        # GSI Logik
        assert 0 <= gsi_weighted <= 100, f"GSI außerhalb [0, 100]: {gsi_weighted}"
        calculated_gsi = (df['impact_score'] * df['presence_ratio']).sum() / df['presence_ratio'].sum() if df['presence_ratio'].sum() > 0 else 0.0
        assert abs(gsi_weighted - calculated_gsi) < 0.1, f"GSI falsch: Erwartet {calculated_gsi:.2f}, erhalten {gsi_weighted:.2f}"

        # Visuelle Ausgabe
        print("\n=== Pipeline Topic Results ===")
        for topic_result in topic_results:
            explain_topic_result(topic_result)
        print(f"Weighted GSI: {gsi_weighted:.2f}")