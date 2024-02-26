from flask import Flask, render_template, request
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id="5d709f1e73ca41149dc6c52717bf42b8", 
                                                      client_secret="30215aa3aef043fd85e84f8d80faa776")
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)


app = Flask(__name__)
    
@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    song = request.form['song']
    results = sp.search(q=song, limit=20)
    for idx, track in enumerate(results['tracks']['items']):
        print(idx, track['name'])
    return "thank you!"

if __name__ == '__main__':
    app.run()