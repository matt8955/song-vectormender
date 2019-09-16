import gensim
from fuzzywuzzy import process
import numpy as np
from fuzzywuzzy import process
from gensim.models import Word2Vec
from collections import Counter

#load w2v model
model = Word2Vec.load("10window_word2vec.model")

def remove_artists(artist):
    '''removes artists that are bad suggestions on a whole'''
    bad = ['Thunderstorms', 'Thunderstorm Global Project from TraxLab','Sheikh Saad Al Ghamdi',
          'Sheikh Mishary Alafasy']
    if artist in bad:
        return np.nan
    else:
        return artist

def too_many(x, threshold):
    '''checks if one artist is above a certain thereshold in list
    if yes then remove playlist'''

    c = Counter(x)
    for value in c.values():
        if (value/len(x)) >= threshold:
            return np.nan
    return x

def most_similar(artist):
    x = process.extractOne(artist,list(model.wv.vocab))[0]
    print(f'searching for {x}.....')
    matches = model.wv.most_similar(x)
    #print matching artists
    for match in matches:
        print(match[0])
        
def did_you_mean(user, artist):
    ans  = input(f'You entered {user}: Did you mean {artist}? (y/n)')
    return ans

def many_artist(*argv):
    '''queries user for multiple artists and fuzzy matches to an artist in the
    vocabulary of the model, then makes a reccomendation'''
    #check if artist even in vocab of model
    artists = []
    field = list(model.wv.vocab)
    for arg in argv:
        i = 0 
        while i != 4:
            results = process.extractBests(arg, field)
            for result in results:
                ans = did_you_mean(arg, result[0])
                if ans == 'y':
                    artists.append(result[0])
                    i = 4
                    break
                elif ans == 'n':
                    if i == 4:
                        #end of results 
                        print(f'Support for {arg} will be in a future release :(')
                        break
                    else:
                        i += 1
                        continue
                else:
                    dick = 0
                    while ans not in ['y', 'n']:
                        if dick == 2:
                            ans = input('Stop being a d**k, y or n....')
                            dick +=1
                        if dick > 2:
                            print('DUDE')
                            ans = 'y'
                            i=4
                        else:
                            ans = input('Please type y or n....')
                            dick += 1
                    break
                            
    if len(artists) > 0:                   
        #get avg of all artist vectors then get closest to that vector
        vectors = [model[x] for x in artists]
        avg = sum(vectors)/len(argv)
        similar = model.wv.most_similar(positive=[avg], topn=len(artists)+10)
        similar = [x[0] for x in similar]
        result = [x for x in similar if x not in artists]
        #print in some way?
        return result
            
            
                
        
