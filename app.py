from flask import Flask, render_template, request
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id="5d709f1e73ca41149dc6c52717bf42b8", 
                                                      client_secret="30215aa3aef043fd85e84f8d80faa776")
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)


app = Flask(__name__)
    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        results = sp.search(q=query, type='track', limit=10)
        tracks = []
        for track in results['tracks']['items']:
            track_info = {
                'name': track['name'],
                'artist': track['artists'][0]['name']}
            tracks.append(track_info)
        return render_template('results.html', tracks=tracks, query=query)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
