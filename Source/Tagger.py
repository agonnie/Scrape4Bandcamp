import eyed3
import datetime
import re

class Tagger:
    @staticmethod
    def tag(album):
        # Get album cover
        with open(album.path + "cover.jpg", "rb") as imageFile:
            file = imageFile.read()
            image_bytes = bytearray(file)
        for track in album.tracks:
            if track.file is not None:
                print("tagging " + track.title)
                audio_file = eyed3.load(album.path + re.sub("[/:\"*?<>|]+", "-", track.title) + ".mp3")
                if audio_file:
                    audio_file.initTag()
                    audio_file.tag.artist = track.artist
                    audio_file.tag.title = track.title
                    audio_file.tag.album = album.title
                    audio_file.tag.track_num = (track.tracknum + 1, track.total_tracks)
                    audio_file.tag.release_date = datetime.datetime.strptime(album.publish_date, "%d %b %Y %H:%M:%S %Z").strftime('%Y-%m-%d')
                    audio_file.tag.comments.set("Downloaded using Scrape4Bandcamp " + "Track Link: " + track.title_link)
                    audio_file.tag.images.set(3, image_bytes, "image/jpeg", "")
                    audio_file.tag.save()
                else:
                    print("Invalid File")
