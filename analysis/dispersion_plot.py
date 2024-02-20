import nltk
from nltk.draw import dispersion_plot
from nltk.tokenize import word_tokenize

nltk.download('punkt')

def generate_dispersion_plot(text, target_words):
    tokens = word_tokenize(text.lower())
    dispersion_plot(tokens, target_words)