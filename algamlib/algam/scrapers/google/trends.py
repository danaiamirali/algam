from pytrends.request import TrendReq
from ...schema import Topic

def get_current_trends() -> list[str]:
    pytrend = TrendReq(hl='en-US', tz=360)
    trends = pytrend.trending_searches()[0].tolist()

    assert isinstance(trends, list), f"Expected a list but got {type(trends)}"

    return [Topic(name=topic, source="Google Trends") for topic in trends]