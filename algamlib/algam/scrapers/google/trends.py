from pytrends.request import TrendReq
from ...schema import Topic

def compute_popularity(trend: str) -> int:
    """
    Function to compute popularity of a trend since pytrends does not provide this information.

    We compute popularity as the haromonic mean of:
    - sum of the interest over time for the last 4 hours
    and
    - sum of the interest over time for the last hour
    """
    pytrend = TrendReq(hl='en-US', tz=360)
    trends = pytrend.trending_searches()[0].tolist()

    values = []

    for timeframe in ["now 1-H", "now 4-H"]:
        pytrend.build_payload(kw_list=[trend], timeframe=timeframe)

        interest_over_time_df = pytrend.interest_over_time()

        # TODO: Handle the case where the trend is not found / error occurs

        values.append(interest_over_time_df[trend].sum())

    return int(2 / ((1 / values[0]) + (1 / values[1])))

def get_current_trends() -> list[str]:
    pytrend = TrendReq(hl='en-US', tz=360)
    trends = pytrend.trending_searches()[0].tolist()

    assert isinstance(trends, list), f"Expected a list but got {type(trends)}"

    results = [Topic(name=trend, source="Google", popularity=compute_popularity(trend)) for trend in trends]

    # Normalize the popularities (0-100)
    max_popularity = max([topic.popularity for topic in results])
    for topic in results:
        topic.popularity = int((topic.popularity / max_popularity) * 100)

    # Sort the results by popularity
    results.sort(key=lambda x: x.popularity, reverse=True)

    return results