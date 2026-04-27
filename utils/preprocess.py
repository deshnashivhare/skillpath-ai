import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def preprocess_text(text):

    tokens = word_tokenize(text.lower())

    filtered = []

    for word in tokens:
        if word.isalpha() and word not in stopwords.words('english'):
            filtered.append(word)

    return filtered
