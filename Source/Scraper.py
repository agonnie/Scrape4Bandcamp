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


class JsonException(Exception):
    pass


class Scraper:
    def __init__(self, path):
        self.path = path
        self.tagger = Tagger()

    def download(self, album_link):
        album = Album()
        # Scrape the website for JSON
        json_text = self.get_json(album_link)
        # populate our Album object
        album.populate(json_text)
        # create folder to save into
        # TODO: Sanitize title
        save_folder = "%s/%s/%s/" % (self.path, str(album.artist), str(album.title).rstrip())
        os.makedirs(os.path.dirname(save_folder), exist_ok=True)
        print("Downloading:\nSaving in: %s" % save_folder)
        # Get album cover
        urlretrieve(album.art_url, save_folder + "cover.jpg")
        # Download tracks & Tag them
        for track in album.tracks:
            self.download_track(track, save_folder)
        album.path = save_folder
        self.tagger.tag(album)

    @staticmethod
    def get_json(album_link):
        # Open the album link and get the album id
        html = BeautifulSoup(urlopen('%s' % album_link), "html.parser")
        match = re.search(r"album_id\":([0-9]+)", str(html))
        album_id = match.group(1)
        # We use the embedded player since it returns clean JSON
        embedded_player = BeautifulSoup(urlopen("https://bandcamp.com/EmbeddedPlayer/v=2/album=" + str(album_id)),
                                        "html.parser")
        try:
            # The information we want is in the playerdata variable
            match = re.search(r"var playerdata = ({.*);", str(embedded_player))
            json_text = json.loads(match.group(1))
            return json_text
        except json.decoder.JSONDecodeError:
            raise


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
