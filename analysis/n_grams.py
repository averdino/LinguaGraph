'''
N-GRAMS
'''

from nltk import ngrams
from collections import Counter
from nltk.tokenize import word_tokenize

# Funzione per generare n-grammi dal testo
def generate_n_grams(text, n=2):
    """
    Genera e conta gli n-grammi in un dato testo.

    :param text: Il testo da cui generare gli n-grammi.
    :param n: Il numero di elementi in ogni n-gramma.
    :return: Un contatore degli n-grammi più comuni.
    """
    tokens = word_tokenize(text)
    n_grams = ngrams(tokens, n)
    return Counter(n_grams)

# Esempio di utilizzo:
# text = "Questo è un esempio di testo per generare bigrammi."
# bigrammi = generate_n_grams(text, 2)
# print(bigrammi.most_common(5))
