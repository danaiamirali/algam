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

        try:
            interest_over_time_df = pytrend.interest_over_time()
        except Exception as e:
            raise Exception(f"Error while fetching interest over time of trend {trend}: {e}")

        try:
            values.append(interest_over_time_df[trend].sum())
        except KeyError:
            # If the trend is not in the interest_over_time_df, it means it has no data and we can ignore it
            values.append(999999)

    return int(2 / ((1 / values[0]) + (1 / values[1])))

def get_current_trends() -> list[str]:
    try:
        pytrend = TrendReq(hl='en-US', tz=360)
    except Exception as e:
        raise Exception(f"Error while connecting to Google Trends: {e}")
    try:
        trends = pytrend.trending_searches()
        trends = trends[0].tolist()
    except Exception as e:
        raise Exception(f"Error while fetching current trends: {e}")

    assert isinstance(trends, list), f"Expected a list but got {type(trends)}"

    results = [Topic(name=trend, source="Google", popularity=compute_popularity(trend)) for trend in trends]

    # Normalize the popularities (0-100)
    max_popularity = max([topic.popularity for topic in results])
    for topic in results:
        topic.popularity = int((topic.popularity / max_popularity) * 100)

    # Sort the results by popularity
    results.sort(key=lambda x: x.popularity, reverse=True)

    return results