def calculate_social_presence_score(social_presence, median_presence=0.5, threshold=0.05):
    if not isinstance(social_presence, (int, float)) or social_presence < 0:
        return 0.0
    if social_presence < threshold:
        return 0.0
    try:
        return round(50 + 50 * ((social_presence - median_presence) / (1 - median_presence)), 2)
    except ZeroDivisionError:
        return 0.0


def calculate_social_engagement_score(likes, shares, comments, views,
                                      median_likes=1.0, median_shares=1.0, median_comments=1.0,
                                      engagement_threshold=0.02, max_engagement=0.10):
    if not isinstance(views, (int, float)) or views <= 0:
        return 0.0
    try:
        engagement_raw = (median_likes * likes + median_shares * shares + median_comments * comments) / views

        capped_engagement = min(engagement_raw, max_engagement)

        if capped_engagement < engagement_threshold:
            return 0.0

        return round(((capped_engagement - engagement_threshold) / (max_engagement - engagement_threshold)) * 100, 2)
    except ZeroDivisionError:
        return 0.0


def calculate_social_visibility(presence_score, engagement_score):
    return round(0.5 * presence_score + 0.5 * engagement_score, 2)


def calculate_visibility_factor(visibility_score):
    return round(visibility_score / 100, 4)


def calculate_sentiment_scaled(sentiment_raw):
    if not isinstance(sentiment_raw, (int, float)) or sentiment_raw < 0 or sentiment_raw > 100:
        return 50.0
    return round(sentiment_raw, 2)


def calculate_impact_score(visibility_factor, sentiment_scaled):
    return round(visibility_factor * (sentiment_scaled - 50) + 50, 2)


def get_news_contrast(social_presence_score, news_presence):
    news_threshold = 0.5
    social_threshold = 50
    if social_presence_score > social_threshold and news_presence > news_threshold:
        return "Starkes Thema mit breiter medialer und öffentlicher Aufmerksamkeit ✔️"
    elif social_presence_score > social_threshold and news_presence <= news_threshold:
        return "Underreported: Die Menschen sind betroffen, aber die Medien schweigen ⚠️"
    elif social_presence_score <= social_threshold and news_presence > news_threshold:
        return "Overreported: Medien pushen es, aber niemanden juckt es eigentlich ❗"
    else:
        return "Kein relevantes Thema – low impact, low coverage"

