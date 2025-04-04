import spacy
from pprint import pprint

lines = ["銀座で寿司を食べる。"]


nlp = spacy.load("ja_ginza_electra")

for line in lines:
    doc = nlp(line)
    for sent in doc.sents:
        for token in sent:
            print(token.tag_)
        print("EOS")
