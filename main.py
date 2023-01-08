import sys
import widget
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pyupbit


form_class = uic.loadUiType("resource/main.ui")[0]


class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.overViewWidget = widget.OverviewWidget(None,'KRW-BTC')#시가를 보여주는 위젯

        comboBox = QComboBox(self)#코인을 선택하는 위젯
        ticker = pyupbit.get_tickers(fiat="KRW")
        for i in ticker:
            comboBox.addItem(i)
        comboBox.activated[str].connect(self.onActivated)

        layout = self.gridLayout
        layout.addWidget(self.overViewWidget, 0, 0)
        layout.addWidget(comboBox, 0, 1)

    def onActivated(self, text):#코인 선택위젯에서 코인 선택했을때
        self.overViewWidget.changeTicker(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    exit(app.exec_())
