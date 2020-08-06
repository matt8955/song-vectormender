import gensim
from fuzzywuzzy import process
import numpy as np
from gensim.models import Word2Vec
from collections import Counter

model = Word2Vec.load("models/artist2vec/v2/artist2vec.model")

def recommend(*argv):
    '''queries user for multiple artists and fuzzy matches to an artist in the
    vocabulary of the model, then makes a reccomendation'''
    #check if artist even in vocab of model
    print(argv)
    if argv[0] == None:
        return ['Select an artist.....']
    elif argv[0] == []:
         return ['Select an artist.....']
    vectors = [model[artist] for artist in argv]
    avg = sum(vectors)/len(argv)
    similar = model.wv.most_similar(positive=avg, topn=len(argv[0])+15)
    similar = [x[0] for x in similar]
    result = [x for x in similar if x not in argv[0]]

    return result
