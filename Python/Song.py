import SongsQueue
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

class Song:
    def __init__(self, queue_element):
        #zrob nazwe ze sciezki i z nazwy pliku przechowywanej w kolejce
        localiser = SongsQueue.dir_path + "/" + str(queue_element)
        audio = MP3(localiser)
        try:
            self.artist = str(audio['TALB'].text)
            self.artist = self.artist[2:-2]
        except KeyError:
            self.artist = "No metadata"
        self.title = queue_element

    def getTitle(self):
        #assuming the extension has 3 chars
        return str(self.title[:-4])

    def getArtist(self):
        return self.artist