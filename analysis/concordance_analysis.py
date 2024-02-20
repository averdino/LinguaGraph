import nltk
from nltk.tokenize import word_tokenize
from nltk.text import Text

# Assicurati che il pacchetto punkt sia stato scaricato
nltk.download('punkt')

def find_concordance(text_data, word):
    tokens = word_tokenize(text_data.lower())
    text = Text(tokens)
    concordance_list = text.concordance_list(word, width=80)
    return concordance_list