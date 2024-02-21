'''
N-GRAMS
'''

from nltk import ngrams
from collections import Counter
from nltk.tokenize import word_tokenize


def generate_n_grams(text, n=2):
    """
    Generating and counting the n-grams in the text.

    :param text: The input text for the n-grams.
    :param n: The number of the elements in every n-gram.
    :return: An n-gram counter for the most common n-grams.
    """
    tokens = word_tokenize(text)
    n_grams = ngrams(tokens, n)
    return Counter(n_grams)
