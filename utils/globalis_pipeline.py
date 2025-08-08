import numpy as np
import pandas as pd
import logging
from utils.helpers import calculate_combined_score, load_historical_stats, save_historical_stats
from models.topic_analyzer import analyze_topic
from models.opinion_analyzer import analyze_opinion
from models.sentiment_analyzer import analyze_sentiment
from statistics import median

DEFAULT_STATS = {'min_rel': 0.01, 'med_rel': 0.05, 'max_rel': 0.5, 'history': []}

logger = logging.getLogger(__name__)

class GlobalisPipeline:
    def __init__(self):
        print("INIT PIPELINE")
        self.selected_topics = ['Inflation', 'Migration', 'Environment', 'Energy', 'Safety']
        self.historical_stats_path = 'data/social_presence_stats.json'

    def calculate_weighted_gsi(self, df):
        try:
            if df.empty:
                logger.warning("DataFrame ist leer, GSI wird als 0 zurückgegeben.")
                return 0.0
            total_weight = df['presence_ratio'].sum()
            if total_weight == 0:
                return 0.0
            weighted_sum = (df['impact_score'] * df['presence_ratio']).sum()
            return round(weighted_sum / total_weight, 2)
        except Exception as e:
            logger.error(f"Fehler bei GSI-Berechnung: {e}")
            return 0.0

    def run(self, posts):
        print("START PIPELINE")
        historical_stats = load_historical_stats()
        results = []
        topic_counts = {topic: 0 for topic in self.selected_topics}
        total_analyzed_posts = 0
        valid_posts = []
        topic_impact_scores = {topic: [] for topic in self.selected_topics}

        for post in posts:
            try:
                topic = analyze_topic(post)
                logger.info(f"Topic classification for '{post}': {topic}")
                if topic not in self.selected_topics:
                    logger.info(f"Überspringe Post mit Topic '{topic}': {post}")
                    continue
                if not analyze_opinion(post):
                    logger.info(f"Überspringe nicht-meinungsbasieren Post: {post}")
                    continue
                valid_posts.append((post, topic))
                total_analyzed_posts += 1
                topic_counts[topic] += 1
            except Exception as e:
                logger.error(f"Fehler bei der Verarbeitung von Post '{post}': {e}")
                continue

        for post, topic in valid_posts:
            try:
                sentiment = analyze_sentiment(post)
                logger.info(f"Sentiment for '{post}' (topic: {topic}): {sentiment:.4f}")
                stance = "Contra" if sentiment < -0.3 else "Pro" if sentiment > 0.3 else "Neutral"
                presence_ratio = topic_counts[topic] / total_analyzed_posts if total_analyzed_posts > 0 else 0.0
                logger.info(f"Presence ratio for '{post}' (topic: {topic}): {presence_ratio:.4f}")

                topic_stats = historical_stats.get(topic, DEFAULT_STATS)
                min_rel = topic_stats['min_rel']
                med_rel = topic_stats['med_rel']
                max_rel = topic_stats['max_rel']

                print(f"DEBUG: topic={topic}, presence_ratio={presence_ratio}, min_rel={min_rel}, med_rel={med_rel}, max_rel={max_rel}, sentiment={sentiment}")
                impact_score = calculate_combined_score(
                    presence_ratio, min_rel, med_rel, max_rel, sentiment
                )
                topic_impact_scores[topic].append(impact_score)
                logger.info(f"Impact score for '{post}' (topic: {topic}): {impact_score:.4f}")

                results.append({
                    'text': post,
                    'topic': topic,
                    'sentiment': sentiment,
                    'stance': stance,
                    'presence_ratio': presence_ratio,
                    'impact_score': impact_score
                })

            except Exception as e:
                logger.error(f"Fehler bei der Verarbeitung von Post '{post}': {e}")
                continue

        topic_results = []
        for topic in self.selected_topics:
            if topic_impact_scores[topic]:
                avg_impact_score = sum(topic_impact_scores[topic]) / len(topic_impact_scores[topic])
                topic_results.append({
                    'topic': topic,
                    'presence_ratio': topic_counts[topic] / total_analyzed_posts if total_analyzed_posts > 0 else 0.0,
                    'avg_impact_score': avg_impact_score
                })

        for topic in self.selected_topics:
            if topic in topic_counts and topic_counts[topic] > 0:
                presence_ratio = topic_counts[topic] / total_analyzed_posts
                historical_stats.setdefault(topic, DEFAULT_STATS)
                historical_stats[topic]['history'].append(presence_ratio)
                historical_stats[topic]['history'] = historical_stats[topic]['history'][-30:]
                historical_stats[topic]['med_rel'] = median(historical_stats[topic]['history'])
                if presence_ratio < historical_stats[topic]['min_rel']:
                    historical_stats[topic]['min_rel'] = presence_ratio
                if presence_ratio > historical_stats[topic]['max_rel']:
                    historical_stats[topic]['max_rel'] = presence_ratio

        if not results:
            logger.warning("Keine Posts nach der Verarbeitung übrig.")
            return pd.DataFrame(), 0.0, 0

        df = pd.DataFrame(results)
        save_historical_stats(historical_stats)
        gsi_weighted = self.calculate_weighted_gsi(df)

        print("\n=== Topic Impact Scores ===")
        for topic_result in topic_results:
            print(f"Topic: {topic_result['topic']}, Presence Ratio: {topic_result['presence_ratio']:.4f}, "
                  f"Average Impact Score: {topic_result['avg_impact_score']:.2f}")
        print(f"Weighted GSI: {gsi_weighted:.2f}")

        logger.info(f"Pipeline verarbeitet: {len(df)} Posts")
        return df, gsi_weighted, total_analyzed_posts
