'''
CO-OCCURRENCE NETWORK BUILDING
'''

import networkx as nx
from nltk.tokenize import word_tokenize
from collections import Counter
import nltk

nltk.download('punkt')

def build_co_occurrence_network(text, top_n_words=30, window_size=4):
    """
    Builds a co-occurrence network for the top N most frequent words in the provided text.

    Parameters:
    - text: The text from which to build the co-occurrence network.
    - top_n_words: Number of most frequent words to consider for the network.
    - window_size: Number of words in the co-occurrence window.
    """
    # Tokenize the text
    tokens = word_tokenize(text.lower())

    # Calculate the frequency of all words in the text
    most_common_words = [word for word, freq in Counter(tokens).most_common(top_n_words)]

    # Initialize an undirected graph
    G = nx.Graph()

    # Build co-occurrence relationships
    for i in range(len(tokens) - window_size + 1):
        window = tokens[i:i+window_size]
        for word1 in window:
            for word2 in window:
                if word1 != word2:
                    if not G.has_edge(word1, word2):
                        G.add_edge(word1, word2, weight=0)
                    G[word1][word2]['weight'] += 1

    return G

# Example usage
if __name__ == "__main__":
    example_text = "This is a sample text for testing the co-occurrence network function. It includes some repeated words for co-occurrence."
    network = build_co_occurrence_network(example_text, top_n_words=10, window_size=4)
    print(network.edges(data=True))