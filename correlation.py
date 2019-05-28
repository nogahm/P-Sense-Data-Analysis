from difflib import SequenceMatcher
import spacy
# import fastsemsim
# from sematch.semantic.similarity import WordNetSimilarity
import nltk
# nltk.download()
from nltk.corpus import stopwords

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def sentiment_analysis(a, b):
    nlp = spacy.load('en_core_web_lg')  # make sure to use larger model!
    string = a+' '+b
    tokens = nlp(string)
    return tokens[0].similarity(tokens[1])


def clean(a):
    # split into words
    from nltk.tokenize import word_tokenize
    tokens = word_tokenize(a)
    # convert to lower case
    tokens = [w.lower() for w in tokens]
    # remove punctuation from each word
    import string
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    # remove remaining tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]
    # filter out stop words
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
    stop_words.add('see')
    words = [w for w in words if not w in stop_words]
    return ' '.join(words)


def calculate_correlation(a, b):
    a=clean(a)
    sim = similar(a, b)
    if sim > 0.6:
        return 1
    else:
        return sentiment_analysis(a, b)