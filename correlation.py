from difflib import SequenceMatcher
import spacy


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def sentiment_analysis(a, b):
    nlp = spacy.load('en_core_web_lg')  # make sure to use larger model!
    string = a+' '+b
    tokens = nlp(string)
    return tokens[0].similarity(tokens[1])


def calculate_correlation(a, b):
    sim = similar(a, b)
    if sim > 0.6:
        return 1
    else:
        return sentiment_analysis(a, b)