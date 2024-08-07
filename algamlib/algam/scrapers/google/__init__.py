def from_google():
    from .trends import get_current_trends
    from ...schema import Topics

    return Topics(topics=get_current_trends())