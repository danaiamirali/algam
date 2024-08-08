from algam.scrapers import from_reddit
import pytest

def test_main():
    reddit_topics = from_reddit()

    for topic in reddit_topics:
        print(topic)
        print(type(topic))
    assert True

if __name__ == "__main__":
    test_main()