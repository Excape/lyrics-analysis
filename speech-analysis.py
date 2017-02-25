import os
import json
import charts
from google.cloud import language
import lyrics


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


def analyze_partition(part, lang='en'):
    sentiment_score = query_sentiment_score(part, lang)
    return {
        'part': part,
        'sentiment': sentiment_score
    }


def analyze_song(song):
    if song['lyrics'] is None:
        return song

    lang = song['lyrics']['lang']
    lyrics_parts = partition_lyrics(song['lyrics']['lyrics'])

    # Analyze whole song -> fewer requests to API
    lyrics_concat = '\n'.join(lyrics_parts)
    song['lyrics']['lyrics'] = lyrics_concat
    song['lyrics']['sentiment'] = query_sentiment_score(lyrics_concat, lang)

    # Analyze every line sepparately
    # analyzed_parts = [analyze_partition(part, lang) for part in lyrics_parts]

    # song['lyrics']['lyrics'] = analyzed_parts
    print(song)
    return song


def get_speech_analysis(data):
    return {year: list(map(analyze_song, chart)) for year, chart in data.items()}


def get_existing_lyrics():
    lyrics = None
    if os.path.exists('lyrics.json'):
        with(open('lyrics.json', 'r')) as f:
            lyrics = json.load(f)
    return lyrics


if __name__ == "__main__":
    data = get_existing_lyrics()
    if data is None:
        data = lyrics.get_existing_charts()
        if data is None:
            data = charts.get_charts()
        data = lyrics.get_lyrics(data)
    data = get_speech_analysis(data)

    with(open('speech_analysis.json', 'w')) as f:
        json.dump(data, f)
