import select
import socket
import bluetooth
import sys
import subprocess
import SongsQueue
import OknoGlowne
import os.path as path
import hashlib

from Song import Song


class bluetoothConEvent(object):

    clients = []

    inputs = []
    outputs = []

    # mapowanie socket-dane
    message_queues = {}


    def __init__(self):
        # hostMACAddress = '60:6D:C7:EF:BE:7C'
        hostMACAddress = '34:F6:4B:22:C6:39'
        PORT = 3
        self.BUFF = 1024
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.settimeout(10)
        self.sock.setblocking(0)
        self.sock.bind((hostMACAddress, PORT))
        self.alive = True
        self.inputs.append(self.sock)

    def recv_until(self, client, delimiter):
        result = ""
        data = b''
        while not result.endswith(delimiter):
            data = data + client.recv(1)
            result = data.decode('utf-8')
        return result


    def listen(self):
        self.sock.listen(10)
        print("Waiting for connection...")

        while self.inputs:
            readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs)

            # jesli zdarzenie nastapilo w liscie do czytania
            for r in readable:

                # jesli zdarzenie wywolalo gniazdo serwera
                if r is self.sock:

                    client, addr = self.sock.accept()
                    client.setblocking(0)
                    self.inputs.append(client)
                    self.clients.append(client)
                    self.message_queues[client] = ""

                # jesli zdarzenie wywolalo gniazdo klienta - tutaj obsluz komunikaty protokolu
                else:

                    data = self.recv_until(r, '\r\n')

                    if data:
                        self.message_queues[r] = data
                        if r not in self.outputs:
                            self.outputs.append(r)

                    # jesli nic nie przyszlo to ktos sie rozlaczyl
                    else:

                        if r in self.outputs:
                            self.outputs.remove(r)

                        self.inputs.remove(r)
                        self.clients.remove(r)
                        r.close()
                        del self.message_queues[r]

            # jesli zdarzenie nastapilo w liscie do pisania
            for w in writable:
                data = self.message_queues.get(w)

                print(data)

                #data handler
                handled = self.protocol_handler(data, w)

                del self.message_queues[w]
                self.outputs.remove(w)

                if handled == "TERMINATE":
                    self.inputs.remove(w)



            # jesli zdarzenie nastapilo w liscie odpowiedzialnej za monitorowanie bledow
            # for e in exceptional:
            #     self.inputs.remove(e)
            #     if e in self.outputs:
            #         self.outputs.remove(e)
            #     e.close()
            #     del self.message_queues[e]


    def protocol_handler(self, data, client):

        # starting new queue
        if data:
            print(data)

            # starting new queue
            if data.startswith("NEW_QUEUE") and SongsQueue.id == -1:
                SongsQueue.id = data[9:-2]
                # SongsQueue.id_hash = hashlib.sha256(SongsQueue.id.encode('utf-8')).hexdigest()
                # print(SongsQueue.id_hash)
                print("DEBUG: nowe id ", SongsQueue.id)
                client.send("NEW_QUEUE_OK\r\n".encode('utf-8'))
                print("Sending " + "NEW_QUEUE_OK to " + str(client))
            # starting new queue but it exists
            elif data.startswith("NEW_QUEUE") and SongsQueue.id != -1:
                client.send("NEW_QUEUE_ERROR\r\n".encode('utf-8'))
            # attach to existing queue
            elif data.startswith("NEW_UUID"):
                if SongsQueue.id == -1:
                    client.send("NEW_UUID_ERROR\r\n".encode('utf-8'))
                else:
                    SongsQueue.uuid = data[8:-2]
                    print("NEW UUID = " + SongsQueue.uuid)
                    client.send("NEW_UUID_OK\r\n".encode('utf-8'))
            elif data.startswith("ATTACH") and SongsQueue.id != -1:
                pin = data[6:-2]
                print(pin)
                if pin != SongsQueue.id:
                    print("attach err")
                    client.send("ATTACH_ERR\r\n".encode('utf-8'))
                    client.close()
                else:
                    print("attach ok")
                    client.send("ATTACH_OK\r\n".encode('utf-8'))
                    client.send("UUID_"+SongsQueue.uuid+"\r\n".encode('utf-8'))
            # get songs
            if data.startswith("NEW_SONG"):
                try:
                    directory = SongsQueue.dir_path
                    filename = data[8:-2] + ".mp3"
                    full_path = str(directory) + "/" + str(filename)
                    directory = directory.replace("/", "\\")

                    #check for path traversal
                    if (path.commonprefix((path.realpath(full_path), directory)) == directory):
                        print("Super")
                        SongsQueue.song_propositions.append(filename)
                        SongsQueue.queue.append(filename)
                        SongsQueue.songs_updated.set()
                        client.send("OK\r\n".encode('utf-8'))
                    else:
                        print("Path Traversal poss")
                        client.send("NEW_SONG_ERR\r\n".encode('utf-8')) #client handling
                except:
                    client.send("NEW_SONG_ERR\r\n".encode('utf-8'))
            elif data.startswith("PLAY\r\n"):
                if (SongsQueue.start == 0):
                    SongsQueue.player.play()
                    SongsQueue.player.positionChanged.connect(
                        OknoGlowne.Ui_MainWindow.update_position)  # zaktualizuje sie tylko raz
                    SongsQueue.player.durationChanged.connect(OknoGlowne.Ui_MainWindow.update_duration)
                    SongsQueue.start = 1

                else:
                    SongsQueue.player.pause()
                    SongsQueue.start = 0


            elif data.startswith("NEXT\r\n"):
                try:
                    # OknoGlowne.ui.nextSong() #nie dziala
                    pass
                except:
                    print(sys.exc_info()[0])
            elif data.startswith("PREV\r\n"):
                # OknoGlowne.Ui_MainWindow.prevSong()
                pass
            elif data.startswith("DETACH"):
                client.close()
                # remove this client from clients list, do it by searhing its index
                # since you don't know which thread is going to remove the first saved client
                self.clients.remove(client)

                # print("Removing client... Full list: " + str(self.clients))
                # print("Length: " + str(len(self.clients)))
                print("Client disconnected")

                # if everyone gets disconnected, reset ID
                if len(self.clients) == 0:
                    SongsQueue.id = -1
                return "TERMINATE"
            return ""
        else:
            print("PUSTA DATA - zamykanie klienta6")
            client.close()
            self.clients.remove(client)
            if len(self.clients) == 0:
                SongsQueue.id = -1
            return "TERMINATE"

    def updateAllClients(self):
        if SongsQueue.queue:
            current_song = Song(SongsQueue.queue[0])
            msg = "CURRENT_" + current_song.getTitle() + "_" + current_song.getArtist() + "\r\n"
            print("Sending message: " + msg)
            print("Ilosc podlaczonych klientow: " + str(len(self.clients)))
            for client in self.clients:
                client.send(msg.encode('utf-8'))
