# -*- coding: utf-8 -*-

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import QVideoWidget
import logging

from ui_playerMainWindow import Ui_Dialog

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

class playerMainWindow(Ui_Dialog,QDialog):
    def __init__(self):
        super(Ui_Dialog, self).__init__()
        self.setupUi(self)
        self.isPause = False
        self.player = QMediaPlayer()
        vw = QVideoWidget(self.playframe)
        vw.setGeometry(self.playframe.geometry())
        self.player.setVideoOutput(vw)
        self.pbOpen.clicked.connect(self.loadFile)
        self.pbPlay.clicked.connect(self.play)
        self.pbStop.clicked.connect(self.stop)
        self.pbPause.clicked.connect(self.pause)
        self.player.positionChanged.connect(self.changeSlide)
    
    def loadFile(self):
        self.filepath = QFileDialog.getOpenFileUrl()[0]
        logger.info('[playerMainWindow.loadFile] self.filepath = %s.' % (self.filepath,))
    
    def play(self):
        self.player.setMedia(QMediaContent(QUrl('http://magica.club:8080/2sFsE7TCvH/PhSkilXO24/141')))#(self.filepath))
        self.player.play()
    
    def stop(self):
        self.player.stop()
    
    def pause(self):
        if self.isPause:
            self.isPause = False
            self.player.play()
            self.pbPause.setText('pause')
        else:
            self.isPause = True
            self.player.pause()
            self.pbPause.setText('resume')

    def changeSlide(self,position):
        self.vidoeLength = self.player.duration()+0.1
        self.playSlider.setValue(round((position/self.vidoeLength)*100))