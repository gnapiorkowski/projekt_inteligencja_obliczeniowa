import morfeusz2
import os
import pandas as pd

df = pd.read_csv('songs.csv')
print(df)

def print_interpretation(df):
    morf = morfeusz2.Morfeusz()

    for line in df['text']:
        if type(line) is str:
            for word in line.split(' '):
                print("-----TEXT: ", word)
                analysis = morf.analyse(word.decode('utf-8'))
                for intepretation in analysis:
                    print('-----INTERPRETATION: ', intepretation[2][1].encode('utf-8'))
                

def stem2(text):
    if type(text) is str:
        morf = morfeusz2.Morfeusz()
        result_words = []
        for word in text:
            analysis = morf.analyse(word.decode('utf-8'))
            for intepretation in analysis:
                result_words.append(intepretation[2][1].encode('utf-8'))
    return ' '.join(result_words)

def stem(text):
    if type(text) is str and ' ' in text:
        morf = morfeusz2.Morfeusz()
        result_words = []
        for word in text.split(' '):
            try:
                analysis = morf.analyse(word.decode('utf-8'))
                if len(analysis) > 0:
                    result_words.append(analysis[0][2][1].encode('utf-8'))
            except:
                result_words.append(word)
        result = ' '.join(result_words)
        return result
    else:
        return text
def apply_stem(df):
    df['stemmed_text'] = df['text'].apply(stem)
    return df
for i in range(3200, 3350, 50):
    apply_stem(df.loc[(df['id'] >= i) & (df['id'] < (i+50))]).to_csv('./dataframe/{}.csv'.format(i+1))
    print('Processing ids: [{}, {}]'.format(i, i+50))
