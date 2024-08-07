import random
import logging
from typing import List, Union

from .schema import Topics, Topic

def merge_and_reorder(k: int, *args: Topics, method: str = "balanced", weights: List[Union[int, float]] = None) -> List[str]:
    """
    Merge and reorder elements from n lists into a single list of k elements.

    :param k: Number of elements to sample.
    :param args: Lists of elements to sample from.
    :param method: Method to use for merging. Options are "balanced" and "weighted".
    :param weights: Weights for each list when using the "weighted" method.

    :return: A list of k elements sampled from the input lists.

    Method "balanced" will sample elements from each list in order until k elements are sampled.
    Method "weighted" will sample elements from each list in order, but with the final distribution of elements based on the weights provided.
    If the method is "weighted", the weights parameter must be provided.
    """
    merged = []

    if method == "balanced":
        for i in range(k):
            for arg in args:
                if i < len(arg):
                    merged.append(arg[i])
    elif method == "weighted":
        if weights is None:
            logging.warning("No weights provided for weighted merging. Using balanced method instead.")
            return merge_and_reorder(k, *args, method="balanced")
        if len(weights) != len(args):
            raise ValueError("Number of weights must match number of lists.")

        # Calculate the total weight
        total_weight = sum(weights)

        # Create a list of tuples (list, probability)
        weighted_args = [(arg, weight / total_weight) for arg, weight in zip(args, weights)]

        # Now, we take from each list in order but such that
        # the amount of elements from each list in the final merged array
        # is proportional to the weights

        while len(merged) < k:
            for arg, weight in weighted_args:
                if len(merged) < k and random.random() < weight:
                    if arg:
                        merged.append(arg.pop(0))
    else:
        raise ValueError(f"Invalid method: {method}")

    return merged

def extract_topics(text: str, n: int = 5) -> List[str]:
    """
    Extract topics from a given text.

    :param text: Text to extract topics from.
    :param n: Number of topics to extract.

    :return: A list of n topics extracted from the text.
    """
    # To extract topics, we will leverage topic modeling techniques
    # LDA, LSA, NMF
    ...