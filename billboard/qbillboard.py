# Script used to get top songs from Billboard based on genre
import billboard
import sys
import json

chart = billboard.ChartData(sys.argv[1])
with open('data/billboard_data', 'a') as outfile:
    for song in chart:
        song_dict = {'song': song.title, 'artist': song.artist}
        song_str = json.dump(song_dict, outfile)
        outfile.write('\n')

# print(song_file_name)
