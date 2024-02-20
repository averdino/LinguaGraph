'''
CO-OCCURRENCE NETWORK TEST
'''

import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from nltk.tokenize import word_tokenize
from collections import Counter
import nltk

nltk.download('punkt')

# Adjust the path to find the analysis directory for importing
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'analysis')))

def build_co_occurrence_network(data, column='clean_text', top_n_words=300, window_size=4):
    """
    Costruisce una rete di co-occorrenza per le top N parole più frequenti.
    """
    # Calcola la frequenza delle parole in tutto il dataset
    all_words = [word for text in data[column] for word in word_tokenize(text)]
    most_common_words = [word for word, freq in Counter(all_words).most_common(top_n_words)]

    G = nx.Graph()
    for text in data[column]:
        words = word_tokenize(text)
        # Filtra le parole per includere solo quelle nel set delle parole più frequenti
        words = [word for word in words if word in most_common_words]
        for i in range(len(words) - window_size + 1):
            window = words[i:i+window_size]
            for word1 in window:
                for word2 in window:
                    if word1 != word2:
                        if not G.has_edge(word1, word2):
                            G.add_edge(word1, word2, weight=0)
                        G[word1][word2]['weight'] += 1
    return G

def plot_co_occurrence_network(G, title="Co-occurrence Network", background_color="lightgray"):
    plt.figure(figsize=(10, 10))
    pos = nx.spring_layout(G, k=0.15, iterations=20)
    edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=50, edge_color='black',
            width=edge_weights, font_size=8, font_color='white', alpha=0.6)  # font_color set to 'white' for visibility
    plt.title(title)
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    # Assuming the preprocessed data file is in the 'data' directory
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'your_preprocessed_data.csv')
    data = pd.read_csv(data_path)

    if 'clean_text' in data.columns:
        G = build_co_occurrence_network(data, 'clean_text', top_n_words=30, window_size=4)
        plot_co_occurrence_network(G)
    else:
        print("The 'clean_text' column was not found. Please verify the column names.")