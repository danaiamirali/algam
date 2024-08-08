from .common import merge_and_reorder
from .schema import Topic, Topics
from typing import List, Union

def get_topics(*platforms: List[str], weights: List[Union[float, int]] = None, num_topics: int = 30) -> Topics:
    """
    Get a list of topics based on the selected platforms.

    :param platforms: Platforms to get topics from. e.g. "google", "reddit".

    :return: A list of topics.
    """
    topics = []

    for platform in platforms:
        if   platform.upper() == "GOOGLE":
            from .scrapers import from_google
            trends = from_google()

            topics.append(trends)
        elif platform.upper() == "REDDIT":
            from .scrapers import from_reddit
            reddit_topics = from_reddit()

            topics.append(reddit_topics)
        else:
            raise ValueError(f"Invalid platform: {platform}")

    if weights:
        topics = merge_and_reorder(num_topics, *topics, weights=weights, method="weighted")
    else:
        topics = merge_and_reorder(num_topics, *topics, method="balanced")

    return Topics(topics=topics)