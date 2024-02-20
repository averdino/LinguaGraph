'''
PREPROCESSING TEST
'''
import sys
import os
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import re

# Download delle risorse NLTK necessarie
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')

def clean_text(text, language='en'):
    # Removing special characters \n, \r, \t
    text = re.sub(r'[\n\r\t]', ' ', text)

    # Tokenisation
    words = word_tokenize(text)

    # Removing stop-words
    stop_words = set(stopwords.words(language))
    words = [word for word in words if word.lower() not in stop_words]

    # Removing punctuation
    words = [word for word in words if word.isalpha()]

    # Lemmatisation
    lemmatizer = WordNetLemmatizer()
    lemmatized = [lemmatizer.lemmatize(word) for word in words]

    # Creating the clean text
    clean_text = ' '.join(lemmatized)
    return clean_text

def test_preprocessing():
    # ELLIPSE Corpus dataset URL
    url = 'https://raw.githubusercontent.com/scrosseye/ELLIPSE-Corpus/main/ELLIPSE_Final_github.csv'

    # Load the dataset from the URL
    data = pd.read_csv(url)

    # Please verify whether the 'full_text' column is present: either way, choose the column containing the text that needs to be pre-processed:
    if 'full_text' in data.columns:
        # Apply cleaning function to the columns
        data['clean_text'] = data['full_text'].apply(lambda x: clean_text(x, language='english'))
        # Print the first five lines to verify the result of the cleaning function:
        print(data[['full_text', 'clean_text']].head())

        # Save the processed data to a CSV file
        data.to_csv('../data/your_preprocessed_data.csv', index=False)
    else:
        print("The 'full_text' column was not found in the dataset. Please verify the column names.")

if __name__ == "__main__":
    test_preprocessing()



