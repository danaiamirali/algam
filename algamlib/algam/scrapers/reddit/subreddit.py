import praw
from typing import List, Union
from ...schema import Topic
from ...common import merge_and_reorder

# Get credentials
from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ID     = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")

class Subreddit():
    def __init__(self, name):
        self.name = name
        self.subreddit = praw.Reddit(
            client_id     = CLIENT_ID,
            client_secret = CLIENT_SECRET,
            user_agent    = "algam-scraper"
        ).subreddit(name)

    def get_hot_topics(self, limit=10):
        topics = self.subreddit.hot(limit=limit)
        return topics

    def get_trending_topics(self, limit=10):
        topics = self.subreddit.rising(limit=limit)
        return topics

def get_topics(topic_type: str = "trending", subreddits: List[str] = None, weights: List[Union[float, int]] = None) -> List[Topic]:
    assert topic_type in ["hot", "trending"], f"Invalid type: {topic_type}"

    topics = []

    if not subreddits:
        subreddits = [
            "news",
            "sports",
            "entertainment",
            "science"
        ]

    for subreddit in subreddits:
        sub = Subreddit(subreddit)
        subreddit_topics = []
        for topic in getattr(sub, f"get_{topic_type}_topics")():
            subreddit_topics.append(Topic(name=topic.title, source="Reddit"))

        topics.append(subreddit_topics)

    if not weights:
        topics = merge_and_reorder(30, *topics, method="weighted", weights=[3, 1, 1, 1])
    else:
        topics = merge_and_reorder(30, *topics, method="balanced")

    return topics