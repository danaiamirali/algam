def from_reddit():
    from ...schema import Topics
    from .subreddit import get_topics

    return Topics(topics=get_topics(topic_type="hot"))