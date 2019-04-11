from difflib import SequenceMatcher
import spacy


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


print(similar("horse", "ors"))


nlp = spacy.load('en_core_web_lg')  # make sure to use larger model!
tokens = nlp(u'lion tiger')

for token1 in tokens:
    for token2 in tokens:
        print(token1.text, token2.text, token1.similarity(token2))