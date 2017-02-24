import billboard
import json


def fetch_billboard(start_year=1997, end_year=2017):
    return ((year, billboard.ChartData('hot-100', '%d-01-01' % year))
            for year in range(start_year, end_year))


def clean_up_song(song):
    # Remove "Featuring..."
    i = song['artist'].find('Featuring')
    if i > 0:
        song['artist'] = song['artist'][:i-1]

    return song


def get_charts():
    charts = dict()
    for year, chart in fetch_billboard():
        charts[year] = list()
        for entry in chart:
            song = {
                'rank': entry.rank,
                'artist': entry.artist,
                'title': entry.title}
            charts[year].append(clean_up_song(song))
    return charts


if __name__ == "__main__":
    charts = get_charts()
    with(open('charts.json', 'w')) as f:
        json.dump(charts, f)
