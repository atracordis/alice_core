import nltk
from nltk.corpus import stopwords
from nltk.tokenize import NLTKWordTokenizer

stop_words = set(stopwords.words('english'))
stop_words.update(["'ve", "", "'ll", "'s", ".", ",", "?", "!", "(", ")", "..", "'m", "n", "u"])


def preprocess_text(text):
    tokenizer = NLTKWordTokenizer()
    text = text.lower()

    tokens = tokenizer.tokenize(text)
    tokens = [t for t in tokens if t not in stop_words]

    return ' '.join(tokens)
