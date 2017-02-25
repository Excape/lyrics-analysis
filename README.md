# lyrics-analysis
## WORK IN PROGRESS

Fooling around with APIs to analyse sentiments of popular music lyrics over time

## Components
- `charts.py` gets the top-10 charts for every month for the last 20 years from billboard.com
- `lyrics.py` uses these charts and adds lyrics to every song. Uses the [Mixmatcher API](https://developer.musixmatch.com/) (needs an API key)
- `speech-analysis.py` uses the data from `lyrics.py` and runs every song through the [Google Natural Language API](https://cloud.google.com/natural-language/) to do a sentiment analysis. It awards a score from -1.0 (negative) to +1.0 (positive)
    - Uses the [Google Cloud Natural Language Client](https://cloud.google.com/natural-language/docs/reference/libraries)
    - Google Cloud SDK must be installed and set-up
- Every script outputs the data to a JSON-File in the same directory. Subsequent parts use these files if they exist

## APIs
- Billboard Charts: <https://github.com/guoguo12/billboard-charts>
- Lyrics: <https://developer.musixmatch.com/>
- Speech Analysis: <https://cloud.google.com/natural-language/>
