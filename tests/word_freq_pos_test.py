import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'analysis')))
from word_freq_pos import word_freq_by_pos
import pandas as pd

if __name__ == "__main__":
    data_path = '../data/your_preprocessed_data.csv'
    data = pd.read_csv(data_path)

    full_text = ' '.join(data['clean_text'].dropna())

    while True:
        pos_input = input("Enter the POS tags separated by commas (e.g., nn,vb) or type 'exit' to quit: ")
        if pos_input.lower() == 'exit':
            break

        # Converti l'input dell'utente in uppercase per corrispondere ai tag POS attesi
        desired_pos = [pos.strip().upper() for pos in pos_input.split(',')]

        print(f"Calculating frequency for POS {desired_pos}:")

        freq_dist = word_freq_by_pos(full_text, desired_pos)

        for word, freq in freq_dist:
            print(f"{word}: {freq}")