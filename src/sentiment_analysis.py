'''
SENTIMENT ANALYSIS
'''

from textblob import TextBlob

def analyze_sentiment(text):
    """Analyzes the sentiment of the provided text, returning both polarity and a sentiment label."""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    label = 'neu'
    if polarity > 0:
        label = 'pos'
    elif polarity < 0:
        label = 'neg'
    return polarity, label