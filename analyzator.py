import os
import textAnalysis
from wordcloud import WordCloud, ImageColorGenerator
from matplotlib import pyplot as plt
from itertools import combinations
import json
import pickle

text = {}
path = './piosenki/'
for author in os.listdir(path):
    text[author] = ''
    for song in os.listdir(path+author):
        if(song != 'metric'):
            with open(path + author +'/' + song) as file:
                text[author] += file.read()


def save_wordcloud_img(analyzed):
    print('Generating WordCloud')
    wordcloud = WordCloud(background_color="white", width=1600, height=800).generate(' '.join(analyzed))

    wordcloud.to_file('./wordcloud/' + author + '.png')


for author, songs in text.items():
    item = songs
    item = item.replace('Tekst piosenki:', '')
    item = item.replace('Poznaj historię zmian tego tekstu', '')
    item = item.lower()
    item = item.replace('"', '')
    analyzed = textAnalysis.doTheThing(item, 2)
    text[author] = textAnalysis.doTheThing(item, 2)
    # save_wordcloud_img(analyzed[1])



    # Display the generated image:
    # the matplotlib way:
    # plt.imshow(wordcloud, interpolation='bilinear')
    # plt.axis("off")
    # plt.show()

    # if author == 'marek_grechuta':
    #     analyzed[2].plot(30)
    
def take_first(elem):
    return elem[0]


def save_to_json(text):
    with open('processed_texts.json', 'w') as file:
        json.dump(text, file)
        file.close()


def save_to_pickle(text):
    with open('precessed_texts.pickle', 'wb') as file:
        pickle.dump(text, file, pickle.HIGHEST_PROTOCOL)
        file.close()

def save_to_file(text):
    for key, item in text.items():
        with open('dict/' + key, 'w') as file:
            for line in item[1]:
                file.write(line+'\n')

def save_to_csv(text):
    

# save_to_file(text)
save_to_json(text)


def calculate_similarities(text):
    similarities = []
    for X, Y in combinations(text.keys(), 2):
        similarities.append(([textAnalysis.cosineSimilarity(text[X][2], text[Y][2])], str( X ) + " and " + str( Y )))
        
        # print("Cosine similarity of " + str(X) + " and " + str( Y ) + " ", textAnalysis.cosineSimilarity(text[X][2], text[Y][2]))
    sorted_sim = sorted(similarities, key = take_first)
    
    for i in sorted_sim:
        print(i)
    return sorted_sim
# calculate_similarities(text)