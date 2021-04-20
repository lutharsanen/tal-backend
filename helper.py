from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

################### helper-function ################


def stemming_algo(word):
    ps = PorterStemmer()
    stemmed_word = ps.stem(word)
    return stemmed_word
