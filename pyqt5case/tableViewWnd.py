from PyQt5.QtWidgets import QDialog,QHeaderView
from Ui_tableViewWnd import *

class CTableViewWnd(QDialog,Ui_tableViewDlg):
    def __init__(self,*args, **kwargs):
        super(CTableViewWnd, self).__init__(*args, **kwargs)
        self.setupUi( self )
        self.tableViewWnd.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)