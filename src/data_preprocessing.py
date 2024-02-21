import spacy
nlp = spacy.load('en_core_web_sm')


def clean_text(text):
    doc = nlp(text)
    tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct]
    clean_text = ' '.join(tokens)
    return clean_text
if __name__ == "__main__":
    example_text = "Here's an example: Spacy is a powerful tool for NLP."
    cleaned_text = clean_text(example_text)
    print("Original Text:", example_text)
    print("Cleaned Text:", cleaned_text)