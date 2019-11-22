class Album:
    def __init__(self):
        self.title = None
        self.artist = None
        self.art_id = None
        self.band_url = None
        self.publish_date = None
        self.tracks = []
        self.album_id = 0
        self.art_url = ""
        self.path = ""

    def add_tracks(self, dictionary):
        for track in dictionary:
            track_object = Track(track)
            track_object['total_tracks'] = len(dictionary)
            self.tracks.append(track_object)

    def populate(self, json_object):
        self.title = json_object['album_title']
        self.artist = json_object['artist']
        self.art_id = str(json_object['album_art_id'])
        self.art_url = str("https://f4.bcbits.com/img/a" + self.art_id + "_5.jpg")
        self.band_url = json_object['band_url']
        self.publish_date = json_object['publish_date']
        self.album_id = json_object['album_id']
        self.add_tracks(json_object['tracks'])


class Track:
    def __init__(self, dictionary):
        for key in dictionary:
            setattr(self, key, dictionary[key])

    def __setitem__(self, key, value):
        setattr(self, key, value)