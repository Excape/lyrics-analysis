import os
import json
import requests
import charts

lyrics_cache = dict()


def fetch_track_lyrics(artist, title):
    """ Returns lyrics when found, None when not found """

    MUSIXMATCH_KEY = get_musixmatch_key()
    api_query = 'https://api.musixmatch.com/ws/1.1/matcher.lyrics.get?'
    api_query += 'q_track=%s&' % title
    api_query += 'q_artist=%s&' % artist
    api_query += 'apikey=%s' % MUSIXMATCH_KEY

    response = requests.get(api_query)
    if response.status_code != 200:
        raise Exception("Mixmatcher API not accessible")

    res_body = json.loads(response.text)
    message = res_body['message']
    if message['header']['status_code'] != 200:
        return None
    body = message['body']
    if 'lyrics' not in body:
        return None
    lyrics = body['lyrics']

    return {
        'lyrics': lyrics['lyrics_body'],
        'lang': lyrics['lyrics_language']
    }


def get_track_lyrics(artist, title):
    if (artist, title) in lyrics_cache:
        print('{} - {} found in cache'.format(artist, title))
        return lyrics_cache[(artist, title)]
    lyrics = fetch_track_lyrics(artist, title)
    lyrics_cache[(artist, title)] = lyrics
    return lyrics


def get_musixmatch_key(path='api-keys/musixmatch'):
    if not os.path.exists(path):
        raise Exception('Provide Musixmatch API-Key in file %s' % path)
    with(open(path, 'r')) as f:
        return f.read()


def get_lyrics_from_charts(charts):
    for year, chart in charts.items():
        for month, topten in chart.items():
            print("Process {}-{}".format(year, month))
            for song in topten:
                print("Getting lyrics for {} - {}".format(song['artist'], song['title']))
                lyrics = get_track_lyrics(song['artist'], song['title'])
                song['lyrics'] = lyrics
                if lyrics is None:
                    print("No lyrics found for {} - {}".format(song['artist'], song['title']))
    return charts


def get_existing_charts():
    charts = None
    if os.path.exists('charts.json'):
        print("Load existing charts")
        with(open('charts.json', 'r')) as f:
            charts = json.load(f)
    return charts


def dump_lyrics(data):
    with(open('lyrics.json', 'w')) as f:
        json.dump(data, f)


def get_lyrics():
    data = get_existing_charts()
    if data is None:
        data = charts.get_charts()
    data = get_lyrics_from_charts(data)
    dump_lyrics(data)


if __name__ == "__main__":
    get_lyrics()
