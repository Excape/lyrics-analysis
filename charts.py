import billboard
import json


def fetch_billboard_year(year):
    """ returns top-10 for every month of the specified year """
    print("Get billboard charts for {}".format(year))
    return ((month, billboard.ChartData('hot-100', '{:d}-{:02d}-01'.format(year, month))[:10])
            for month in range(1, 13))


def fetch_billboard(start_year=1997, end_year=2017):
    """ returns top-100 for every year from start_year to end_year """
    return ((year, billboard.ChartData('hot-100', '{:d}-01-01'.format(year)))
            for year in range(start_year, end_year+1))


def clean_up_song(song):
    # Remove "Featuring..."
    i = song['artist'].find('Featuring')
    if i > 0:
        song['artist'] = song['artist'][:i-1]

    return song


def dump_charts(charts):
    with(open('charts.json', 'w')) as f:
        json.dump(charts, f)


def get_charts():
    charts = dict()
    for year in range(1997, 2017):
        charts[year] = dict()
        for month, chart in fetch_billboard_year(year):
            charts[year][month] = list()
            for entry in chart:
                song = {
                    'rank': entry.rank,
                    'artist': entry.artist,
                    'title': entry.title}
                charts[year][month].append(clean_up_song(song))
    dump_charts(charts)
    return charts


if __name__ == "__main__":
    get_charts()
