import pandas as pd
from itertools import combinations

df = pd.read_csv('topics_per_song.csv')
artists = dict()
for i, (word, weight, auth_tit) in enumerate(zip(df['Topic 0 words'], df['Topic 0 weights'], df['author_title'])):
    if(auth_tit not in artists):
        artists[auth_tit] = dict()
    if('words' not in artists[auth_tit]):
        artists[auth_tit]['words'] = []
        artists[auth_tit]['weights'] = []
    artists[auth_tit]['words'].append(word) 
    artists[auth_tit]['weights'].append(weight) 


result=dict()
result['artist1'] = []
result['artist2'] = []
result['similarity'] = []
for X, Y in combinations(artists.keys(), 2):
    x_w_sum = sum(artists[X]['weights'])
    y_w_sum = sum(artists[Y]['weights'])
    similarity = 0
    for i, w in enumerate(artists[X]['words']):
        if w in artists[Y]['words']:
            similarity += (artists[X]['weights'][i]/x_w_sum + artists[Y]['weights'][artists[Y]['words'].index(w)]/y_w_sum)/2
    if similarity > 0:
        result['artist1'].append(X)
        result['artist2'].append(Y)
        result['similarity'].append(similarity)
df = pd.DataFrame(result)
df = df.sort_values('similarity', ascending=False)
df.to_csv('topics_similarities.csv')