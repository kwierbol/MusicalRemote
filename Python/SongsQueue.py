from threading import Event

#user proposals - buffer
from PyQt5.QtMultimedia import QMediaPlayer

song_propositions = []
songs_updated = Event()

#start or stop player
start = 0  # 0 = wstrzymaj, 1 = start, 2 = stop
player = QMediaPlayer()

#next/prev song in playlist
nextSong = False
prevSong = False

#actual queue keeping track of the current song
queue = []

id = -1
uuid = ""
id_hash = ""

dir_path = ""


