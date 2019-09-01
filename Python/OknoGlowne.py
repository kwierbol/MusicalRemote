# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Multipilot.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!
#w kolejnym watku bedzie przeszukiwanie listy i folderu
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import QUrl, QDirIterator, Qt, QObject
from PyQt5.QtMultimedia import QMediaContent, QMediaPlaylist, QMediaPlayer
from PyQt5.QtWidgets import QFileDialog
import datetime
import threading
import BluetoothConnection
import BluetoothEventTriggered
import SongsQueue

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)


class Ui_MainWindow(object):


    color = 0 # 0 - ciemny, 1 - jasny

    def setupUi(self, MainWindow):
        self.main_window = MainWindow
        #self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        SongsQueue.player.setPlaylist(self.playlist)

        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        #pasek pokazujący ile upłynęło
        self.progressBar = QtWidgets.QSlider(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(20, 400, 641, 23))
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))

        #czas do końca piosenki
        #self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.currentTime = QtWidgets.QLabel(self.centralwidget)
        self.currentTime.setGeometry(QtCore.QRect(700, 400, 64, 23))
        self.currentTime.setObjectName(_fromUtf8("lcdNumber"))

        #start
        self.pushStart = QtWidgets.QPushButton(self.centralwidget)
        self.pushStart.setGeometry(QtCore.QRect(20, 480, 97, 27))
        self.pushStart.setObjectName(_fromUtf8("pushStart"))

        #Wstrzymaj
        self.pushPause = QtWidgets.QPushButton(self.centralwidget)
        self.pushPause.setGeometry(QtCore.QRect(120, 480, 97, 27))
        self.pushPause.setObjectName(_fromUtf8("pushPause"))

        #zakończ
        self.pushStop = QtWidgets.QPushButton(self.centralwidget)
        self.pushStop.setGeometry(QtCore.QRect(220, 480, 97, 27))
        self.pushStop.setObjectName(_fromUtf8("pushStop"))

        #lista z piosenkami
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 761, 351))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.listView = QtWidgets.QListWidget(self.horizontalLayoutWidget)
        self.listView.setGeometry(QtCore.QRect(20, 20, 761, 351))
        self.listView.setObjectName(_fromUtf8("listView"))
        #self.verticalLayout.addWidget(self.listView)

    #    self.verticalLayout.setGeometry(QtCore.QRect(20, 20, 761, 351))

        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(610, 470, 160, 29))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName(_fromUtf8("horizontalSlider"))

        #głośnosc
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(660, 490, 66, 17))
        self.label.setObjectName(_fromUtf8("label"))

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))

        #Plik
        self.menuAs = QtWidgets.QMenu(self.menubar)
        self.menuAs.setObjectName(_fromUtf8("menuAs"))

        self.menuEdytuj = QtWidgets.QAction(self.menubar)
        self.menuEdytuj.setObjectName(_fromUtf8("menuEdytuj"))
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        #co się znajduje z rozwijanym menu
        self.actionWybierz_plik = QtWidgets.QAction(MainWindow)
        self.actionWybierz_plik.setObjectName(_fromUtf8("actionWybierz_plik"))

        self.actionWyjd = QtWidgets.QAction(MainWindow)
        self.actionWyjd.setObjectName(_fromUtf8("actionWyjd"))

        self.actionWybierz_folder = QtWidgets.QAction(MainWindow)
        self.actionWybierz_folder.setObjectName(_fromUtf8("actionWybierz_folder"))

        self.menuAs.addAction(self.actionWybierz_plik)
        self.menuAs.addAction(self.actionWybierz_folder)
        self.menuAs.addSeparator()
        self.menuAs.addAction(self.actionWyjd)

        self.menubar.addAction(self.menuAs.menuAction())
        self.menubar.addAction(self.menuEdytuj)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        #klikanie w buttony

        self.folder = None #folder z ktorego wybieramy piosenki
        self.actionWybierz_folder.triggered.connect(self.chooseFolder) #wybieranie folderu
        self.actionWybierz_plik.triggered.connect(self.addPropositions) #dodaj do playlisty piosenke ktora podajemy z terminala

        self.actionWyjd.triggered.connect(self.close)
        self.menuEdytuj.triggered.connect(self.after_clik_buttonEdytuj)

        self.pushStart.clicked.connect(self.after_click_buttonStart)
        self.pushPause.clicked.connect(self.after_click_buttonPause)
        self.pushStop.clicked.connect(self.after_click_buttonStop)


        self.horizontalSlider.valueChanged.connect(SongsQueue.player.setVolume)
        self.progressBar.valueChanged.connect(SongsQueue.player.setPosition)

        SongsQueue.player.positionChanged.connect(self.update_position)  # gdzie piosenka znajduje sie na pasku
        SongsQueue.player.durationChanged.connect(self.update_duration)  # ile trwa piosenka

    def update_position(self, position):
        if position >= 0:
            self.currentTime.setText(str(self.hhmmss(position)))

        self.progressBar.blockSignals(True)
        self.progressBar.setValue(position)
        self.progressBar.blockSignals(False)

    def update_duration(self, duration):
        self.progressBar.setMaximum(duration)


    def hhmmss(self, ms):
        ms = datetime.datetime.utcfromtimestamp(ms/1000.0)
        ms = ms.strftime('%H:%M:%S')
        return ms



    def retranslateUi(self, MainWindow):

        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushStart.setText(_translate("MainWindow", "Start", None))
        self.pushPause.setText(_translate("MainWindow", "Wstrzymaj", None))
        self.pushStop.setText(_translate("MainWindow", "Zakończ", None))
        self.label.setText(_translate("MainWindow", "Głośność", None))
        self.menuAs.setTitle(_translate("MainWindow", "Plik", None))
        self.menuEdytuj.setText(_translate("MainWindow", "Edytuj", None))
        self.actionWybierz_plik.setText(_translate("MainWindow", "Wybierz plik", None))
        self.actionWyjd.setText(_translate("MainWindow", "Wyjdź", None))
        self.actionWybierz_folder.setText(_translate("MainWindow", "Wybierz folder", None))

    #functions for server buttons (play, pause, stop)
    def after_click_buttonStart(self):
        SongsQueue.player.play()

    def after_click_buttonStop(self):
        SongsQueue.player.stop()

    def after_click_buttonPause(self):
        SongsQueue.player.pause()

    def nextSong(self):
        print("bla bla bla")
        #self.playlist.next()

    def prevSong(self):
        self.playlist.previous()

    def addSongToPlaylist(self,piosenka):

        if self.folder != None:
            #piosenka = input("Podaj nazwe: ")
            it = QDirIterator(self.folder)
            it.next()
            while it.hasNext():
                if it.fileInfo().isDir() == False and it.filePath() != '.':
                    fInfo = it.fileInfo()
                    if fInfo.suffix() in ('mp3', 'ogg', 'wav', 'm4a'):
                        if it.fileName() == piosenka:
                            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(it.filePath())))
                            self.listView.addItem(it.fileName())
                it.next()
            if it.fileInfo().isDir() == False and it.filePath() != '.':
                fInfo = it.fileInfo()
                if fInfo.suffix() in ('mp3', 'ogg', 'wav', 'm4a'):
                    if it.fileName() == piosenka:
                        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(it.filePath())))
                        self.listView.addItem(it.fileName())

    def chooseFolder(self):
        self.folder = QFileDialog.getExistingDirectory(None, 'Open Music Folder', '~')
        SongsQueue.dir_path = self.folder

    def close(self):
        pass


    #po wciśnięciu edytuj - nowe okno
    def after_clik_buttonEdytuj(self):
        SongsQueue.song_propositions.append("hud_music.mp3")
        SongsQueue.queue.append("hud_music.mp3")
        SongsQueue.songs_updated.set()
        #Edytuj.show()

    def addPropositions(self):
        while True:
            length = len(SongsQueue.song_propositions)
            if len(SongsQueue.song_propositions) > 0:
                for i in range(length):
                    #print("Z tej f: ",SongsQueue.song_propositions[i])
                    self.addSongToPlaylist(SongsQueue.song_propositions[i])
                    SongsQueue.song_propositions.pop()
            SongsQueue.songs_updated.wait()
            SongsQueue.songs_updated.clear()




class Ui_Edytuj(Ui_MainWindow):

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 170)

        self.pushButtonZmienKolor = QtWidgets.QPushButton(Dialog)
        self.pushButtonZmienKolor.setGeometry(QtCore.QRect(20, 40, 97, 27))
        self.pushButtonZmienKolor.setObjectName("pushButtonZmienKolor")

        self.pushButtonOpcja1 = QtWidgets.QPushButton(Dialog)
        self.pushButtonOpcja1.setGeometry(QtCore.QRect(150, 40, 97, 27))
        self.pushButtonOpcja1.setObjectName("pushButtonOpcja1")

        self.pushButtonOpcja2 = QtWidgets.QPushButton(Dialog)
        self.pushButtonOpcja2.setGeometry(QtCore.QRect(280, 40, 97, 27))
        self.pushButtonOpcja2.setObjectName("pushButtonOpcja3")

        self.pushButtonOpcja3 = QtWidgets.QPushButton(Dialog)
        self.pushButtonOpcja3.setGeometry(QtCore.QRect(20, 100, 97, 27))
        self.pushButtonOpcja3.setObjectName("pushButtonOpca4")

        self.pushButtonOpcja4 = QtWidgets.QPushButton(Dialog)
        self.pushButtonOpcja4.setGeometry(QtCore.QRect(150, 100, 97, 27))
        self.pushButtonOpcja4.setObjectName("pushButtonOpcja4")

        self.pushButtonOpcja5 = QtWidgets.QPushButton(Dialog)
        self.pushButtonOpcja5.setGeometry(QtCore.QRect(280, 100, 97, 27))
        self.pushButtonOpcja5.setObjectName("pushButtonOpcja5")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.pushButtonZmienKolor.clicked.connect(self.zmienKolor)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButtonZmienKolor.setText(_translate("Dialog", "Zmień kolor"))
        self.pushButtonOpcja1.setText(_translate("Dialog", "Opcja1"))
        self.pushButtonOpcja2.setText(_translate("Dialog", "Opcja2"))
        self.pushButtonOpcja3.setText(_translate("Dialog", "Opcja3"))
        self.pushButtonOpcja4.setText(_translate("Dialog", "Opcja4"))
        self.pushButtonOpcja5.setText(_translate("Dialog", "Opcja5"))

    def zmienKolor(self):

        app.setStyle("Fusion")
        palette = QPalette()
        if self.color == 0:
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(235, 101, 54))
            palette.setColor(QPalette.Highlight, QColor(235, 101, 54))
            palette.setColor(QPalette.HighlightedText, Qt.black)
            app.setPalette(palette)
            self.color = 1
        elif self.color == 1:
            palette.setColor(QPalette.Window, Qt.white)
            palette.setColor(QPalette.WindowText, Qt.black)
            palette.setColor(QPalette.Base, QColor(240, 240, 240))
            palette.setColor(QPalette.AlternateBase, Qt.white)
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.black)
            palette.setColor(QPalette.Button, Qt.white)
            palette.setColor(QPalette.ButtonText, Qt.black)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(66, 155, 248))
            palette.setColor(QPalette.Highlight, QColor(66, 155, 248))
            palette.setColor(QPalette.HighlightedText, Qt.black)
            app.setPalette(palette)
            self.color = 0

if __name__ == "__main__":
    my_bluetooth = BluetoothConnection.bluetoothCon()
    threadBluetooth = threading.Thread(target=my_bluetooth.listen)
    #
    # my_bluetooth =BluetoothEventTriggered.bluetoothConEvent()
    # threadBluetooth = threading.Thread(target=my_bluetooth.listen)

    def window():
        app = QtWidgets.QApplication(sys.argv)
        Multi = QtWidgets.QMainWindow()

        ui = Ui_MainWindow()
        ui.setupUi(Multi)
        Edytuj = QtWidgets.QMainWindow()

        uiE = Ui_Edytuj()
        uiE.setupUi(Edytuj)
        Multi.show()


        #trigger - current song changed -> update all clients about it
        def updt():
            #update clients on change
            my_bluetooth.updateAllClients()
            if SongsQueue.queue:
                print("Current: " + SongsQueue.queue[0])
                SongsQueue.queue.remove(SongsQueue.queue[0])
            print("Next to go: ")
            print(SongsQueue.queue)

        trigger = ui.playlist.currentMediaChanged
        trigger.connect(updt)
        #trigger.emmit()

        def close(event):
            event.accept()
            app.quit()
            my_bluetooth.bluetoothClose()


        Multi.closeEvent = close

        threadAddSongsToPlaylist = threading.Thread(target=ui.addPropositions)
        threadAddSongsToPlaylist.start()


        sys.exit(app.exec_())


    threadBluetooth.start()
    window()
    #threadBluetooth.join()



