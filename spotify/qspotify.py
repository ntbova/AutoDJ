import spotipy

class QuerySpotify:

  def __init__(self, client_id, client_secret):
      self.cid = client_id
      self.cs = client_secret

  def authenticate():
      print('wow')

  def get_album_art(self, name='Radiohead'):
      results = spotify.search(q='artist:' + name, type='artist')
      items = results['artists']['items']
      if len(items) > 0:
          artist = items[0]
          print(artist['name'], artist['images'][0]['url'])
