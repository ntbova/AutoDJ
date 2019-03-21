import json
import os.path

difffile = open('billboard_data_new', 'a')

with open('billboard_data', 'r') as newfile:
    with open('billboard_data_old', 'r') as oldfile:
        newsongs = json.load(newfile)
        oldsongs = json.load(oldfile)
        for newsong in newsongs:
            found = False
            for oldsong in oldsongs:
                if oldsong['song'] == newsong['song']:
                    if oldsong['artist'] == newsong['artist']:
                        found = True
                        break
            if not found:
                song_dict = {'song': newsong['song'], 'artist': newsong['artist']}
                song_str = json.dump(song_dict, difffile)
                difffile.write(',\n')


difffile.close()
