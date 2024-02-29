from flask import Flask, render_template, request
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id="5d709f1e73ca41149dc6c52717bf42b8", 
                                                      client_secret="30215aa3aef043fd85e84f8d80faa776")
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)


app = Flask(__name__)
    
def remove_bracket(s):
    bracket_index = s.find('(')
    if bracket_index != -1:
        return s[:bracket_index] 
    return s  
    
def search(query):
    offset_value = 0
    track_list = []
    while offset_value <= 900:
        results = sp.search(q=query, limit=50, offset=offset_value)
        for track in results['tracks']['items']:
            track_info = {'name': track['name'], 
                          'artist': track['artists'][0]['name']}
            if (track_info['name'].lower() == query.lower()):
                return track_info
            else:
                break
        offset_value += 50

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        words = query.split(" ")
        tracks = []
        for word in words: 
            results = search(word)
            tracks.append(results)
        return render_template('results.html', tracks=tracks, query=query)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

