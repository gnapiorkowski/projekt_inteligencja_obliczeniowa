import requests, bs4, time
import getSong


auth_list_old = {'marek_grechuta':6, 'lona_i_webber':2, 'wilki':4, 'bunkier':2,'maryla_rodowicz':13, 'kombii':3, 'strachy_na_lachy':3, 'perfect':5,'lady_pank':7, 'Lzy':4, 'dzem':4, 'budka_suflera':8, 'maria_koterbska':5, 'ich_troje':8, 'maanam':5, 'elektryczne_gitary':6, 'czerwone_gitary':8, 'felicjan_andrzejczak':4, 'kult':8, 'franek_kimono':1, 'golec_uorkiestra':4, 'kobranocka':3, 'krzysztof_krawczyk':12, 'kasia_sobczyk':2, 'jamal':3}
auth_list = {'myslovitz':5} 

def get_songs_list(author, pages):
    songs = []
    year = []
    for page in range(pages):
        url = 'https://www.tekstowo.pl/piosenki_artysty,' + author + ',alfabetycznie,strona,' + str(page + 1) + '.html'
        res = requests.get(url)
        res.encoding = 'utf-8'
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        for i in (range(30)):
            try:
                songs.append(soup.select('.ranking-lista > div:nth-child(' + str(i + 1) + ') > a:nth-child(2)')[0].getText())
                # print('Got : ' + songs[i] + ' -- with index: ' + str(i+1))
            except IndexError:
                print("Index error at i: {}, page {}", (i + 1), (page + 1))
    return songs


def get_author_title(author, pages):
    song_titles = get_songs_list(author, pages)
    for i, title in enumerate(song_titles):
        song_titles[i] = title.replace('(', '_')
        song_titles[i] = song_titles[i].replace(')', '_')
        song_titles[i] = song_titles[i].lower()
        song_titles[i] = song_titles[i].replace('ą', 'a')
        song_titles[i] = song_titles[i].replace('ć', 'c')
        song_titles[i] = song_titles[i].replace('ę', 'e')
        song_titles[i] = song_titles[i].replace('ł', 'l')
        song_titles[i] = song_titles[i].replace('ń', 'n')
        song_titles[i] = song_titles[i].replace('ó', 'o')
        song_titles[i] = song_titles[i].replace('ś', 's')
        song_titles[i] = song_titles[i].replace('ś', 's')
        song_titles[i] = song_titles[i].replace('ż', 'z')
        song_titles[i] = song_titles[i].replace('ź', 'z')
        song_titles[i] = song_titles[i].replace("'", '_')
        song_titles[i] = song_titles[i].replace('...', '_')
        song_titles[i] = song_titles[i].replace('.', '_')
        song_titles[i] = song_titles[i].replace(',', '_')
        song_titles[i] = song_titles[i].split(' - ')
        song_titles[i][0] = song_titles[i][0].replace('-', '_')
        song_titles[i][1] = song_titles[i][1].replace('-', '_')
        song_titles[i][0] = song_titles[i][0].rstrip()
        song_titles[i][0] = song_titles[i][0].lstrip()
        song_titles[i][1] = song_titles[i][1].rstrip()
        song_titles[i][1] = song_titles[i][1].lstrip()
        song_titles[i][0] = song_titles[i][0].replace(' ', '_')
        song_titles[i][1] = song_titles[i][1].replace(' ', '_')
        if author != song_titles[i][0]:
            print('Changed author from "' + author + '" to "' + song_titles[i][0] + '" at index: ' + str(i))
            author = song_titles[i][0]
        song_titles[i] = song_titles[i][1]
        # print(song_titles[i] + ' -- i: ' + str(i))

    return [author, song_titles]
        
for aut, pages in auth_list.items():
    print('working on: ' + aut)
    author_title = get_author_title(aut, pages)
    print('GOT TITLES, GETTING WORDS')
    getSong.save_song_to_file(author_title[0], author_title[1])