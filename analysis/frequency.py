'''
FREQUENCY ANALYSIS
'''

import spacy
from collections import Counter

# Carica il modello di spacy per l'inglese
nlp = spacy.load('en_core_web_sm')

def count_word_frequency(text, target_word):
    # Processa il testo con spacy
    doc = nlp(text.lower())
    # Conta le occorrenze di tutte le parole
    words = [token.lemma_ for token in doc if token.is_alpha]  # token.is_alpha per escludere la punteggiatura
    word_freq = Counter(words)
    # Restituisci il conteggio della parola target
    return word_freq[target_word.lower()]

if __name__ == "__main__":
    # Esempio di utilizzo
    sample_text = "Spacy is an amazing library for text analysis. Analyzing texts with Spacy is fun."
    target = "analyze"  # Questa parola comparirà come "analyzing" nel testo
    freq = count_word_frequency(sample_text, target)
    print(f"The word '{target}' appears {freq} times in the text.")