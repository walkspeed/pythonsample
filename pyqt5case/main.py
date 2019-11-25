#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QFont 
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView,QWebEngineSettings


from tableViewWnd import *

def tableViewCase():
    app = QApplication(sys.argv)
    dlg = CTableViewWnd()
    dlg.show()
    sys.exit(app.exec_())

def webViewCase():
    app = QApplication(sys.argv)
    wevView = QWebEngineView()
    wevView.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
    wevView.load(QUrl("https://www.netflix.com"))
    wevView.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    webViewCase()