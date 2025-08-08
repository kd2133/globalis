import matplotlib.pyplot as plt

def explain_topic_result(topic_result, gsi_weighted=None):
    """
    Gibt eine verständliche Erklärung für ein Topic-Ergebnis aus, inklusive Impact Score Bedeutung.
    Optional: Zeigt den Weighted GSI mit einer allgemeinen Interpretation an.
    
    Args:
        topic_result (dict): Dictionary mit 'topic', 'presence_ratio', 'avg_impact_score'.
        gsi_weighted (float, optional): Weighted Globalis Intelligence Score (GSI).
    """
    print("\n📊 Topic Analysis:")
    print(f"Topic: {topic_result['topic']}")
    print(f"Presence Ratio: {topic_result['presence_ratio']:.4f} (Share of posts for this topic)")
    print(f"Average Impact Score: {topic_result['avg_impact_score']:.2f}")
    print("Impact Score Meaning:")
    if topic_result['avg_impact_score'] > 75:
        print("  🌟 High positive impact: Strong positive sentiment and high topic presence drive significant public attention.")
    elif topic_result['avg_impact_score'] > 55:
        print("  ✅ Moderate positive impact: Notable sentiment and presence, influencing public perception.")
    elif topic_result['avg_impact_score'] >= 45:
        print("  ⚖️ Neutral impact: Either low topic presence or neutral sentiment, limited influence.")
    elif topic_result['avg_impact_score'] >= 25:
        print("  ⚠️ Moderate negative impact: Notable negative sentiment and presence, signaling public concern.")
    else:
        print("  🚨 High negative impact: Strong negative sentiment and high topic presence, indicating major public dissatisfaction.")
    print("─" * 50)
    
    if gsi_weighted is not None:
        print("\n🌍 Overall Topic Impact:")
        print(f"Weighted GSI: {gsi_weighted:.2f}")
        print("This value reflects the aggregated public sentiment across key topics.")
        if gsi_weighted > 75:
            print("  🌟 High positive impact: Strong positive sentiment across topics, driving widespread public support.")
        elif gsi_weighted > 55:
            print("  ✅ Moderate positive impact: Balanced sentiment with notable positive influence on public perception.")
        elif gsi_weighted >= 45:
            print("  ⚖️ Near-neutral impact: Mixed sentiment across topics, with limited overall influence.")
        elif gsi_weighted >= 25:
            print("  ⚠️ Moderate negative impact: Notable negative sentiment, signaling public concern across multiple topics.")
        else:
            print("  🚨 High negative impact: Strong negative sentiment, indicating significant public dissatisfaction or crisis.")

def plot_topic_scores(topic_results):
    """
    Generiert ein Balkendiagramm für die Average Impact Scores pro Topic.
    
    Args:
        topic_results (list): Liste von Dictionaries mit 'topic' und 'avg_impact_score'.
    """
    topics = [r['topic'] for r in topic_results]
    scores = [r['avg_impact_score'] for r in topic_results]
    plt.figure(figsize=(10, 6))
    plt.bar(topics, scores, color=['#FF6B6B' if s < 50 else '#4ECDC4' for s in scores])
    plt.xlabel('Topics')
    plt.ylabel('Average Impact Score')
    plt.title('Topic Impact Scores')
    plt.ylim(0, 100)
    plt.savefig('topic_impact_scores.png')
    plt.close()
    print("Plot saved as 'topic_impact_scores.png'")
