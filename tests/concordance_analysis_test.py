'''
CONCORDANCE ANALYSIS
'''

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'analysis')))

from concordance_analysis import find_concordance
import pandas as pd

if __name__ == "__main__":
    data_path = '../data/your_preprocessed_data.csv'
    data = pd.read_csv(data_path)
    full_text = ' '.join(data['clean_text'].dropna())

    while True:
        word = input("\nEnter the word to find concordances (or type 'exit' to quit): ")
        if word.lower() == 'exit':  # Permette all'utente di uscire dal ciclo
            break
        concordance_list = find_concordance(full_text, word)
        if concordance_list:
            for concordance in concordance_list:
                print(concordance.line)
        else:
            print(f"No concordances found for '{word}'.")