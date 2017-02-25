import os
import json
from google.cloud import language
import lyrics

sentiment_cache = dict()


def partition_lyrics(lyrics):
    """ splits lyric string into lines """
    parts = lyrics.splitlines()
    parts = filter(lambda p: len(p) > 0, parts)
    parts = filter(lambda p: sum(c.isalpha() for c in p) > 5, parts)
    parts = filter(lambda p: 7*'*' not in p, parts)  # filter out copyright message
    return list(parts)


def query_sentiment_score(text, lang):
    language_client = language.Client()
    document = language_client.document_from_text(text, language=lang)
    sentiment = document.analyze_sentiment()
    return sentiment.score


def get_sentiment_score(artist, title, text, lang):
    if (artist, title) in sentiment_cache:
        print('{} - {}: Sentiment found in cache'.format(artist, title))
        return sentiment_cache[(artist, title)]
    sentiment_score = query_sentiment_score(text, lang)
    sentiment_cache[(artist, title)] = sentiment_score
    return sentiment_score


def analyze_partition(part, lang='en'):
    sentiment_score = query_sentiment_score(part, lang)
    return {
        'part': part,
        'sentiment': sentiment_score
    }


def analyze_song(song):
    if song['lyrics'] is None:
        return song

    print("Analyzing song {} - {}".format(song['artist'], song['title']))
    lang = song['lyrics']['lang']
    lyrics_parts = partition_lyrics(song['lyrics']['lyrics'])

    # Analyze whole song -> fewer requests to API
    lyrics_concat = '\n'.join(lyrics_parts)
    song['lyrics']['lyrics'] = lyrics_concat
    song['lyrics']['sentiment'] = get_sentiment_score(
        song['artist'], song['title'], lyrics_concat, lang)

    # Analyze every line sepparately
    # analyzed_parts = [analyze_partition(part, lang) for part in lyrics_parts]

    # song['lyrics']['lyrics'] = analyzed_parts
    return song


def get_speech_analysis_from_lyrics(data):
    return {year: {month: list(map(analyze_song, topten)) for month, topten in chart.items()}
            for year, chart in data.items()}


def get_existing_lyrics():
    data = None
    if os.path.exists('lyrics.json'):
        print("Load existing lyrics")
        with(open('lyrics.json', 'r')) as f:
            data = json.load(f)
    return data


def dump_speech_analysis(data):
    with(open('speech-analysis.json', 'w')) as f:
        json.dump(data, f)


def get_speech_analysis():
    data = get_existing_lyrics()
    if data is None:
        data = lyrics.get_lyrics()
    data = get_speech_analysis_from_lyrics(data)
    dump_speech_analysis(data)


if __name__ == "__main__":
    get_speech_analysis()
