import sys
from PyQt5 import QtWidgets, Qt, QtGui, QtCore

from packet import *

class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Wacky GUI'
        self.words = []
        self.packets = []
        self.left = 100
        self.top = 100
        self.width = 540
        self.height = 720
        self.initUI()
        self.show()

    def initUI(self):
        vbox = QtWidgets.QVBoxLayout()
        self.listbox = QtWidgets.QVBoxLayout()
        self.wordlist = QtWidgets.QListWidget()
        self.wordlist.resize(self.wordlist.sizeHint())
        vbox.addWidget(self.wordlist)

        btn2 = QtWidgets.QPushButton("Search Online Dictionaries")
        btn2.resize(btn2.sizeHint())
        btn2.clicked.connect(self.updatePackets)
        vbox.addWidget(btn2)

        mp3btn = QtWidgets.QPushButton("Create MP3 File")
        mp3btn.resize(mp3btn.sizeHint())
        mp3btn.setStyleSheet("background-color:orange")
        vbox.addWidget(mp3btn)

        pdfbtn = QtWidgets.QPushButton("Create PDF File")
        pdfbtn.resize(pdfbtn.sizeHint())
        pdfbtn.setStyleSheet("background-color:orange")
        vbox.addWidget(pdfbtn)

        mainwindow = QtWidgets.QWidget()
        mainwindow.setLayout(vbox)

        self.statusBar()
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('&File')
        toolMenu = menubar.addMenu('&Tools')

        openAct = QtWidgets.QAction('Open...', self)
        openAct.triggered.connect(self.extractWordsFromFile)
        fileMenu.addAction(openAct)

        settingAct = QtWidgets.QAction('Settings...', self)
        fileMenu.addAction(settingAct)

        self.setCentralWidget(mainwindow)
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)


    def extractWordsFromFile(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                            "Open File", "",
                            "All Files (*);;Python Files (*.py)", options=options)

        with open(fileName, 'r') as f:
            fileContent = f.readlines()
        self.words = [line.strip() for line in fileContent]

        for i, word in enumerate(self.words):
            packet = Packet(word, i+1)
            self.packets.append(packet)
            plistitem, pwidget = packet.get_packet_widget()

            plistitem.setSizeHint(pwidget.sizeHint())

            self.wordlist.addItem(plistitem)
            self.wordlist.setItemWidget(plistitem, pwidget)

    def updateWordList(self):
        for i in range(self.wordlist.count()):
            item = self.wordlist.item(i)
            if item.checkState() != 0:          # Item checked on the list
                self.words.append(item.text())
        print(self.words)

    def updatePackets(self):
        progress = QtWidgets.QProgressDialog()
        progress.setRange(0, len(self.packets))
        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.canceled.connect(progress.close)
        progress.setCancelButtonText("Stop")
        progress.setWindowTitle("Please wait...")
        progress.setValue(0)
        progress.show()


        for i, packet in enumerate(self.packets):
            packet.fetch_content()
            packet.pwidget.def1_edit.setText(packet.contents[0]['define'])
            progress.setValue(i+1)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())