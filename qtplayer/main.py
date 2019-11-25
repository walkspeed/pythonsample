#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication
from playerMainWindow import playerMainWindow
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    vieo_gui = playerMainWindow()
    vieo_gui.show()
    sys.exit(app.exec_())