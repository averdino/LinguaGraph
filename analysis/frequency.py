'''
FREQUENCY ANALYSIS
'''

import spacy
from collections import Counter
nlp = spacy.load('en_core_web_sm')

def count_word_frequency(text, target_word):
    doc = nlp(text.lower())
    words = [token.lemma_ for token in doc if token.is_alpha]
    word_freq = Counter(words)
    return word_freq[target_word.lower()]

if __name__ == "__main__":
    sample_text = "Spacy is an amazing library for text analysis. Analyzing texts with Spacy is fun."
    target = "analyze"
    freq = count_word_frequency(sample_text, target)
    print(f"The word '{target}' appears {freq} times in the text.")