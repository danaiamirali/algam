"""Uniform schema for all scrapers to conform to."""

from typing import List, Optional
from pydantic import BaseModel, Field

class Topic(BaseModel):
    """An individual topic and were it came from."""

    name: str = Field(..., title="Topic", description="The name of the topic. E.g. 'Bitcoin price surge'")
    source: str = Field(..., title="Source", description="The source of the topic. E.g. Google, Reddit, etc.")

class Topics(BaseModel):
    """A list of topics."""

    topics: List[Topic] = Field(..., title="Topics", description="A list of topics.")

    def __iter__(self):
        return iter(self.topics)

    def __len__(self):
        return len(self.topics)

    def __getitem__(self, i):
        return self.topics[i]

    def __setitem__(self, i, value):
        self.topics[i] = value

    def __delitem__(self, i):
        del self.topics[i]

    def __contains__(self, item):
        return item in self.topics

    def __add__(self, other):
        return Topics(topics=self.topics + other.topics) 

    def pop(self, i: Optional[int] = None):
        return self.topics.pop(i)
