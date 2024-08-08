from algam import get_topics

topics = get_topics("google", "reddit", weights = [0.8, 0.2], num_topics=10)

for topic in topics:
    print(topic)