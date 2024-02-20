import sys
import os
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'analysis')))
from topic_modeling import perform_lda  # Assicurati che questa funzione ritorni i topic in un formato utilizzabile
import matplotlib.pyplot as plt

def plot_topics(topics):
    """
    Visualizza i topic e le parole chiave con la loro importanza usando matplotlib.

    Parameters:
    - topics: Lista di topic ottenuti da LDA, dove ogni topic è rappresentato come una lista di tuple (parola, importanza)
    """
    for i, topic in enumerate(topics, start=1):
        plt.figure(figsize=(10, 4))
        words, weights = zip(*topic)
        plt.bar(words, weights)
        plt.title(f'Topic {i}')
        plt.xticks(rotation=45)
        plt.ylabel('Importance')
        plt.show()

if __name__ == "__main__":
    # Load your preprocessed data
    data_path = '../data/your_preprocessed_data.csv'  # Aggiusta questo percorso
    data = pd.read_csv(data_path)

    if 'clean_text' in data.columns:
        # Esegui LDA Topic Modeling
        print("Performing LDA Topic Modeling...")
        topics = perform_lda(data, 'clean_text', num_topics=5, num_words=5)  # Assicurati che perform_lda ritorni i dati in un formato adatto

        # Visualizza i topic con un grafico
        plot_topics(topics)
    else:
        print("Column 'clean_text' not found in the dataset.")