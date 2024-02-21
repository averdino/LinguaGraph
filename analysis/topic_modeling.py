import nltk
from nltk.tokenize import word_tokenize
from gensim import corpora, models

nltk.download('punkt')

def perform_lda(text, num_topics=5, num_words=5):
    """
    Performs LDA topic modeling on the given text.
    """
    tokens = word_tokenize(text.lower())
    dictionary = corpora.Dictionary([tokens])
    dictionary.filter_extremes(no_below=1, no_above=0.5)
    corpus = [dictionary.doc2bow(tokens)]
    lda_model = models.LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, passes=10)
    topics = lda_model.print_topics(num_words=num_words)
    return topics