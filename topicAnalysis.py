from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
import re, os, nltk
import pandas as pd
from stop_words import get_stop_words



my_stopwords = set(get_stop_words('polish'))
word_rooter = nltk.stem.snowball.PorterStemmer(ignore_stopwords=False).stem
my_punctuation = '!"$%&\'()*+,-./:;<=>?[\\]^_`{|}~•@'

# cleaning master function
def clean_song(item, bigrams=False):
    item = item.replace('Tekst piosenki:', '')
    item = item.replace('Poznaj historię zmian tego tekstu', '')
    item = item.lower() # lower case
    item = re.sub('['+my_punctuation + ']+', ' ', item) # strip punctuation
    item = re.sub('\s+', ' ', item) #remove double spacing
    item = re.sub('([0-9]+)', '', item) # remove numbers
    item_token_list = [word for word in item.split(' ')
                            if word not in my_stopwords] # remove stopwords

    # item_token_list = [word_rooter(word) if '#' not in word else word
    #                     for word in item_token_list] # apply word rooter
    if bigrams:
        item_token_list = item_token_list+[item_token_list[i]+'_'+item_token_list[i+1]
                                            for i in range(len(item_token_list)-1)]
    item = ' '.join(item_token_list)
    return item

# songs = {}
# path = './piosenki/'
# songs['text'] = []
# songs['author_title'] = []
# for author in os.listdir(path):
#     for song in os.listdir(path + author):
#         with open(path + author + '/' + song) as file:
#             songs['text'].append(file.read())
#             songs['author_title'].append(author + '-' + song)

# df = pd.DataFrame(songs)
# df['text'] = df['text'].apply(clean_song)
# print(df.head())

# df.to_csv('songs.csv')
df = pd.read_csv('processed.csv')
df['text'] = df['stemmed_text'].apply(lambda s: s.replace('year', '').replace('s1', '').replace('v1', '').replace('v3', '') if (type(s) is str) else ' ')
df['text'] = df['text'].apply(lambda s: re.sub(':[a-z0-9]{1,2}', '', s))
print(df)

vectorizer = CountVectorizer(max_df=0.85, min_df=10, token_pattern='\w+|\w+|\$[\d\.]+|\S+')

tf = vectorizer.fit_transform(df['text']).toarray()

tf_feature_names = vectorizer.get_feature_names()

number_of_topics = 50
model = LatentDirichletAllocation(n_components=number_of_topics, random_state=0)

model.fit(tf)


def display_topics(model, feature_names, no_top_words):
    topic_dict = {}
    for topic_idx, topic in enumerate(model.components_):
        topic_dict["Topic %d words" % (topic_idx)]= ['{}'.format(feature_names[i])
                        for i in topic.argsort()[:-no_top_words - 1:-1]]
        topic_dict["Topic %d weights" % (topic_idx)]= ['{:.1f}'.format(topic[i])
                        for i in topic.argsort()[:-no_top_words - 1:-1]]
    return pd.DataFrame(topic_dict)

no_top_words = 10
topics = display_topics(model, tf_feature_names, no_top_words)
print('\n -----------Topics-----------\n')
print(topics)
topics.to_csv('topics_main.csv')