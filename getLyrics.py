import requests

songs = []
songs.append({
  'title': 'africa',
  'artist': 'toto',
})
songs.append({
  'title': 'stay',
  'artist': 'post malone',
})
songs.append({
  'title': 'fade into you',
  'artist': 'mazzy star',
})
songs.append({
  'title': 'landslide',
  'artist': 'fleetwood mac',
})
songs.append({
  'title': 'good vibrations',
  'artist': 'the beach boys',
})

apikey = 'fee290f2065c3a2c7a821e6dffc4f3ba'
base_url = 'https://api.musixmatch.com/ws/1.1/matcher.lyrics.get'

for song in songs:
  url = base_url + '?apikey=' + apikey + '&q_track=' + song['title'] + '&q_artist=' + song['artist']

  response = requests.get(url).json()
  copy = response['message']['body']['lyrics']['lyrics_copyright']

  if 'Unfortunately' in copy:
    print('********************************************************************************')
    print('Can\'t display lyrics for ' + song['title'] + ' by ' + song['artist'])
    print('********************************************************************************')
  else:
    lyrics = response['message']['body']['lyrics']['lyrics_body'].rsplit('...\n\n******* This Lyrics is NOT for Commercial use *******', 1)[0]
    print(lyrics)
