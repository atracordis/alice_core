from .preprocess import *


def predict(text, processor, branch):
    text = preprocess_text(text)
    vectorized = processor[branch]["vectorizer"].transform([text])
    result = processor[branch]["model"].predict(vectorized)[0]
    return str(result)
