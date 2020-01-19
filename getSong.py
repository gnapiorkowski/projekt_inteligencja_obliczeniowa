import os
import requests, bs4, re


def get_song_words(url):
    print('Starting download of: ' + url)
    res = requests.get(url)
    assert res.status_code == requests.codes.ok, 'Not OK response code.'
    res.encoding = 'utf-8'
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    words = soup.select('.song-text')
    metric = soup.select('.metric')

    return [metric, words]


def save_song_to_file(author, titles):
    autorzy = os.listdir('./piosenki')
    if author not in os.listdir('./piosenki'): os.mkdir('./piosenki/' + author)
    total = len(titles)
    with open('./piosenki/' + author + '/' + 'metric', 'w') as file:
        file.write('\n')
        file.close()
    for i, title in enumerate(titles):
        url = 'https://www.tekstowo.pl/piosenka,' + author + ',' + title + '.html'
        try:
            metric, words = get_song_words(url)

            with open('./piosenki/' + author + '/' + title, 'w') as file:
                for line in words:
                    file.write(line.getText())
                file.close()
            try:
                year = re.findall('\d\d\d\d', metric[0].text)
            except IndexError:
                year = ' '
            with open('./piosenki/' + author + '/' + 'metric', 'a') as file:
                for y in year:
                    file.write('\nyear:' + title + ':\n' + y)
                # for line in metric:
                #     file.write('\n' + title + ':\n' + line.text + '\n<endOfMetric>')
                file.close()
        except AssertionError:
            print('-------------Error downloading and saving words from: ' + author + ' : ' + title)
        print('Succesfully saved ' + author + ' : ' + title + '\n {}/{}', (i + 1), total)
    print("Succesfully saved files")

