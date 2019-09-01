import bluetooth  # trzeba miec pybluez
import threading
import subprocess
from PyQt5.QtCore import QObject
import time
import OknoGlowne
from Song import Song
import SongsQueue
import sys


class bluetoothCon(object):
    clients = []

    def __init__(self):
        # hostMACAddress = '60:6D:C7:EF:BE:7C'
        # hostMACAddress = self.read_btaddress()
        hostMACAddress = '34:F6:4B:22:C6:39'
        PORT = 3
        self.BUFF = 1024
        self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.socket.settimeout(10)
        self.socket.bind((hostMACAddress, PORT))
        self.alive = True

    def recv_until(self, client, delimiter):
        result = ""
        data = b''
        while not result.endswith(delimiter):
            data = data + client.recv(1)
            result = data.decode('utf-8')
        return result

    def listen(self):
        self.socket.listen(10)
        print("Waiting for connection...")

        while self.alive:
            try:
                client, clientInfo = self.socket.accept()
                # client.settimeout(60)
                print("Connected: " + str(clientInfo))
                self.clients.append(client)
                # print("Appending client... Full list: " + str(self.clients))
                # print("Length: " + str(len(self.clients)))
                thr1 = threading.Thread(target=self.bluetoothListenToClient, args=(client, clientInfo))
                thr1.start()
                # thr1.join()
            except bluetooth.BluetoothError:
                pass

    def read_btaddress(self):
        cmd = "hciconfig"
        device_id = "hci0"
        status, output = subprocess.getstatusoutput(cmd)
        bt_mac = output.split("{}:".format(device_id))[1].split("BD Address: ")[1].split(" ")[0].strip()
        # print("SERVER BLUETOOTH ADAPTER MAC ADDRESS: " + bt_mac) #debug
        return bt_mac

    def bluetoothListenToClient(self, client, clientInfo):

        a = True
        while a:
            try:
                client.settimeout(120)
                data = self.recv_until(client, '\r\n')

                # debug
                print("Data from client: " + data)
                print("SongsQueue.id: " + str(SongsQueue.id))

                if data:
                    # starting new queue
                    if data.startswith("NEW_QUEUE") and SongsQueue.id == -1:
                        SongsQueue.id = data[9:-2]
                        print("DEBUG: nowe id ", SongsQueue.id)
                        client.send("NEW_QUEUE_OK\r\n".encode('utf-8'))
                    # starting new queue but it exists
                    elif data.startswith("NEW_QUEUE") and SongsQueue.id != -1:
                        client.send("NEW_QUEUE_ERROR\r\n".encode('utf-8'))
                    # attach to existing queue
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
                    # get songs
                    if data.startswith("NEW_SONG"):
                        try:
                            title = data[8:-2] + ".mp3"
                            SongsQueue.song_propositions.append(title)
                            SongsQueue.queue.append(title)
                            SongsQueue.songs_updated.set()
                            client.send("OK\r\n".encode('utf-8'))
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
                        a = False
                else:
                    print("PUSTA DATA - zamykanie klienta6")
                    client.close()
            except:

                print("Closing client")
                if self.clients:
                    try:
                        self.clients.remove(client)
                        # print("Removing client... Full list: " + str(self.clients))
                        # print("Length: " + str(len(self.clients)))
                    except:
                        print("Error while removing client from clients list. Might not exist")
                    # if everyone gets disconnected, reset ID
                if len(self.clients) == 0:
                    SongsQueue.id = -1
                client.close()
                a = False

        return ""

    def updateAllClients(self):

        if SongsQueue.queue:
            current_song = Song(SongsQueue.queue[0])
            msg = "CURRENT_" + current_song.getTitle() + "_" + current_song.getArtist() + "\r\n"
            print("Sending message: " + msg)
            print("Ilosc podlaczonych klientow: " + str(len(self.clients)))
            for client in self.clients:
                client.send(msg.encode('utf-8'))

    def bluetoothClose(self):
        self.socket.close()
        self.alive = False


