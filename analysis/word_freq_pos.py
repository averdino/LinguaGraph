'''
WORD FREQUENCY DIVIDED BY PART-OF-SPEECH
'''

import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from collections import Counter

# Assicurati che i pacchetti necessari siano stati scaricati
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def word_freq_by_pos(text_data, desired_pos=['NN', 'JJ', 'VB']):
    tokens = word_tokenize(text_data.lower())
    tagged_tokens = pos_tag(tokens)
    filtered_words = [word for word, tag in tagged_tokens if tag in desired_pos]
    freq_dist = Counter(filtered_words)
    return freq_dist.most_common(10)