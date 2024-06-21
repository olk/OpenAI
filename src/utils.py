import nltk
import numpy as np


def cosine_similarity(x, y):
    return np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))


def download_nltk_data():
    # check and downlaod the 'punkt' tokenizer models
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    # check and downlaod the 'stopwords' corpus
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')


def preprocess_text(text):
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer
    from nltk.tokenize import word_tokenize
    # tokenize text
    tokens = word_tokenize(text)
    # convert to lower case
    tokens = [word.lower() for word in tokens]
    # remove punktuation
    words = [word for word in tokens if word.isalpha()]
    # filter out stop words
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    # stemming
    stemmer = PorterStemmer()
    stemmed_words = [stemmer.stem(word) for word in words]
    return ' '.join(stemmed_words)
