from algam.scrapers.google import from_google
import pytest

def test_main():
    google_topics = from_google()

    for topic in google_topics:
        print(topic)
        print(type(topic))
    assert True

if __name__ == "__main__":
    test_main()