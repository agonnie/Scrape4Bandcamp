"""
Crisisiscris
08/09/18
"""
from bs4 import BeautifulSoup
from Source.Album import *
from urllib.request import urlopen
from urllib.request import urlretrieve
import os
import json
from Source.Tagger import *
import re


class Scraper:
    def __init__(self, path):
        self.path = path
        self.tagger = Tagger()

    def download(self, album_link):
        album = Album()
        finished = False
        while not finished:
            # Scrape the website for JSON
            json_text = self.get_json(album_link)
            # populate our Album object
            album.populate(json_text)
            # create folder to save into
            save_folder = self.path + str("/") + str(album.artist) + str("/") + str(album.title).rstrip() + str("/")
            os.makedirs(os.path.dirname(save_folder), exist_ok=True)
            print("Downloading:\nSaving in: " + save_folder)
            # Get album cover
            urlretrieve("https://f4.bcbits.com/img/a" + album.art_id + "_5.jpg", save_folder + "cover.jpg")
            # Download tracks & Tag them
            for track in album.tracks:
                self.download_track(track, save_folder)
            album.path = save_folder
            self.tagger.tag(album)
            finished = True

    @staticmethod
    def get_json(album_link):
        # Open the album link and get the album id
        html = BeautifulSoup(urlopen('%s' % album_link), "html.parser")
        album_id = str(html).splitlines()[-1][14:-4]
        # We use the embedded player since it returns clean JSON
        embedded_player = BeautifulSoup(urlopen("https://bandcamp.com/EmbeddedPlayer/v=2/album=" + str(album_id)),
                                        "html.parser")
        # The information we want is in the playerdata variable
        json_text = json.loads(str(embedded_player.find_all('script')[4]).split('var playerdata =')[1].split(';')[0])
        return json_text

    def download_track(self, track, save_folder):
        title = re.sub("[/:\"*?<>|]+", "-", track.title) + str(".mp3")
        if track.file is not None:
            url = track.file['mp3-128']
        else:
            print("-- Track: " + track.title + " is not available --\n")
            return
        print("-- Downloading: " + str(title) + " --")
        file_url = urlopen(url)  # this downloads it
        kb = 0
        with open(str(save_folder + title), 'wb') as f:
            block_sz = 32768
            while True:
                buffer = file_url.read(block_sz)
                if not buffer:
                    print("-- " + str(title) + " Has Downloaded --\n")
                    break
                f.write(buffer)
                kb += block_sz
                if (kb // 1024) % 100 == 0:
                    print("\t" + str((kb // 1024) / 1024) + " MB Downloaded")
            f.close()
