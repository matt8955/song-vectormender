import gensim
from fuzzywuzzy import process
import numpy as np

from gensim.models import Word2Vec

model = Word2Vec.load("10window_word2vec.model")

def most_similar(artist):
    '''matches an artists with its name in the vocab and prints similar artists
    also returns a list of those artists with its similarity score'''
    x = process.extractOne(artist,list(model.wv.vocab))[0]
    print(f'searching for {x}.....')
    matches = model.wv.most_similar(x)
    #print matching artists
    for match in matches:
        print(match[0])
    return matches
