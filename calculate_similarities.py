import json
from itertools import combinations
import textAnalysis
import pandas as pd

text = {}
with open('processed_texts.json', 'r') as file:
    text = json.loads(file.read())
for key in text.keys():
    text[key].append([])

df = pd.read_csv('processed.csv')
for author_title, stemmed_text in zip(df['author_title'], df['stemmed_text']):
    author = author_title.split('-')[0]
    if type(stemmed_text) is str:
        text[author][3] += (stemmed_text.replace('year', '').replace('s1', '').replace('v1', '').replace('v3', '').split(' '))
    else:
        pass


def take_first(elem):
    return elem[0]



def text_similarities(text):
    similarities = []
    for X, Y in combinations(text.keys(), 2):
        similarities.append((textAnalysis.cosineSimilarity(text[X][2], text[Y][2]), str( X ) + " and " + str( Y )))
        
        # print("Cosine similarity of " + str(X) + " and " + str( Y ) + " ", textAnalysis.cosineSimilarity(text[X][2], text[Y][2]))
    sorted_sim = sorted(similarities, key = take_first)
    for i in sorted_sim:
        print(i)

def plot_similarities(text):
    similarities = {}
    similarities['from'] = []
    similarities['to'] = []
    similarities['value'] = []
    for X, Y in combinations(text.keys(), 2):
        similarities['from'].append(str(X))
        similarities['to'].append(str(Y))
        similarities['value'].append(textAnalysis.cosineSimilarity(text[X][3], text[Y][3]))
    import pandas as pd
    import networkx as nx
    from matplotlib import pyplot as plt
    import numpy as np
    df = pd.DataFrame(similarities)
    print(df)
    df['value'] = df['value'].apply(lambda x: round((x*10)**2, 2))
    df = df.loc[df['value']>5]
    print(df.sort_values('value'))
    
    G=nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.Graph() )
    
 
    # Custom the nodes:
    nx.draw(G, with_labels=True, node_color='skyblue', node_size=1500, edge_color=df['value'], width=4.0, edge_cmap=plt.cm.Blues)
    plt.show()




# FOR SIMILARITIES PLOT UNCOMMENT BELOW
plot_similarities(text)


from wordcloud import WordCloud


def save_wordcloud_img(analyzed, author):
    print('Generating WordCloud')
    wordcloud = WordCloud(background_color="white", width=1600, height=800).generate(' '.join(analyzed))

    wordcloud.to_file('./wordcloud2/' + author + '.png')


for author, songs in text.items():
    save_wordcloud_img(songs[3], author)


def save_to_json(text):
    with open('processed_stemmed_texts.json', 'w') as file:
        json.dump(text, file)
        file.close()


save_to_json(text)