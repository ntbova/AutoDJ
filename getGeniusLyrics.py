import requests
import json
import os.path
from bs4 import BeautifulSoup

# TODO: take a JSON file make it an array of objects

with open("data/billboard_data") as f:
  songs = json.load(f)

# songs = []
# songs.append({
#   'title': 'africa',
#   'artist': 'toto',
# })
# songs.append({
#   'title': 'stay',
#   'artist': 'post malone',
# })
# songs.append({
#   'title': 'fade into you',
#   'artist': 'mazzy star',
# })
# songs.append({
#   'title': 'landslide',
#   'artist': 'fleetwood mac',
# })
# songs.append({
#   'title': 'good vibrations',
#   'artist': 'the beach boys',
# })

base_url = "http://api.genius.com"
headers = {"Authorization": "Bearer pkrTfTFBg0uY-L4k2cAnuEXyFng81xyFV2ETvK-DwU-yUHp2ZCZ39d88mBtpypvn"}

def lyrics_from_song_api_path(song_api_path):
  song_url = base_url + song_api_path
  response = requests.get(song_url, headers=headers)
  json = response.json()
  path = json["response"]["song"]["path"]
  #gotta go regular html scraping... come on Genius
  page_url = "http://genius.com" + path
  page = requests.get(page_url)
  html = BeautifulSoup(page.text, "html.parser")
  #remove script tags that they put in the middle of the lyrics
  [h.extract() for h in html("script")]
  #at least Genius is nice and has a tag called "lyrics"!
  lyrics = html.find("div", class_="lyrics").get_text() #updated css where the lyrics are based in HTML
  return lyrics

if __name__ == "__main__":

  # discover_objects = []

  for song in songs:
    search_url = base_url + "/search"
    params = {"q": song['song']}
    response = requests.get(search_url, params=params, headers=headers)
    jsonR = response.json()
    song_info = None
    for hit in jsonR["response"]["hits"]:
      if hit["result"]["primary_artist"]["name"].lower() == song['artist'].lower():
        song_info = hit
        break
    if song_info:
      song_api_path = song_info["result"]["api_path"]

      # add song['song'], song['artist'] and lyrics to discover json object
      lyrics = lyrics_from_song_api_path(song_api_path)

      object_for_discover = {
        'song': song['song'],
        'artist': song['artist'],
        'lyrics': lyrics
      }

      title = song['song'].replace("/", "_")
      title = title.replace("?","")
      title = title.replace("\"","")
      artist = song['artist'].replace("/", "_")

      if not os.path.isfile("./lyrics/"+title+"_"+artist+".json"):
        with open("./lyrics/"+title+"_"+artist+".json", 'w') as outfile:
          json.dump(object_for_discover, outfile)
        # discover_objects.append(object_for_discover)
        print(song['song'] + ' has been written to ' + outfile.name)

  # at this point we have an array of all songs, artists, and their lyrics
  # export each one as a JSON file