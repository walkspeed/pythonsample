from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import QVideoWidget
import sys
if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = QMediaPlayer()
    vw = QVideoWidget()
    vw.show()
    player.setVideoOutput(vw)
    player.setMedia(QMediaContent(QFileDialog.getOpenFileUrl()[0]))
    player.play()
    sys.exit(app.exec_())
