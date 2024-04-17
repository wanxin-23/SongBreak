from flask import Flask, render_template, request, url_for, redirect
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id="dfb3a6aafe8e43f584f850a55ca600a5", 
                                                                         client_secret="2f383981757f410289d8c16106b017d2"))
app = Flask(__name__)
    
def search(query):
    offset_value = 0
    while offset_value <= 900:
        results = sp.search(q=query,type="track", limit=50, offset=offset_value)
        for track in results['tracks']['items']:
            track_info = {'name': track['name'], 
                          'artist': track['artists'][0]['name'],
                          'artwork': track['album']['images'][0]['url']}
            if (track_info['name'].lower() == query.lower()):
                return track_info
        offset_value += 50

def get_uri(query):
    offset_value = 0
    while offset_value <= 900:
        results = sp.search(q=query,type="track,artist", limit=50, offset=offset_value)
        for track in results['tracks']['items']:
            track_info = {'name': track['name'], 
                          'artist': track['artists'][0]['name']}
            if (track_info['name'].lower() == query.lower()):
                return track['uri']
        offset_value += 50

uris = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    if request.method == 'POST':
        query = request.form['query']
        words = query.split(" ")
        tracks = []
        i = 0
        global uris
        word = words[i]
        while i < len(words):
            results = search(word)
            uri = get_uri(word)
            if results:
                tracks.append(results)
                uris.append(uri)
                i += 1
                if i < len(words):
                    word = words[i]
                else:
                    break
            else:
                if i != (len(words) -1):
                    word = word + " " + words[i+1]
                    i += 1
                else:
                    tracks.append({'name': 'NOT FOUND', 'artist': 'NOT FOUND'})
                    return render_template('results.html', tracks=tracks, query=query)
        return render_template('results.html', tracks=tracks, query=query)

@app.route('/new_page', methods=['POST'])
def new_page():
    return redirect(url_for('index'))  
        
if __name__ == '__main__':
    app.run(debug=True)


