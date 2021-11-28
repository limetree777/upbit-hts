import pyupbit
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import changeLanguage
import upbitWebsocket

class OverviewWidget(QWidget):
    def __init__(self, parent=None, ticker="KRW-BTC"):
        super().__init__(parent)
        uic.loadUi("resource/overview.ui", self)

        self.ticker = ticker

        self.ovw = OverViewWorker(ticker)
        self.ovw.dataSent.connect(self.fillData)
        self.ovw.start()

    def changeTicker(self, ticker):#코인을 변경한다.
        self.ovw.alive = False
        self.ovw.terminate()
        self.ticker = ticker

        self.ovw = OverViewWorker(ticker)
        self.ovw.dataSent.connect(self.fillData)
        self.ovw.start()


    def fillData(self, code, currPrice, chgRate, value):#overviewworker한테 받은 데이터를 표시한다
        self.label_1.setText(changeLanguage.changeKor(self.ticker))
        self.label_2.setText(code)
        self.label_3.setText(f"{currPrice:,}")
        self.label_4.setText(f"{chgRate*100:,.2f}%")
        self.label_5.setText(f"{value/1000000:,.0f} 백만")
        self.__updateStyle()

    def __updateStyle(self): # 등락률에 따라 배경색을 변경한다.
        if '-' in self.label_4.text():
            self.label_3.setStyleSheet("color:blue;")
            self.label_4.setStyleSheet("background-color:blue;color:white")
        else:
            self.label_3.setStyleSheet("color:red;")
            self.label_4.setStyleSheet("background-color:red;color:white")

class OverViewWorker(QThread):
    dataSent = pyqtSignal(str, float, float, float)

    def __init__(self, ticker):
        super().__init__()
        self.ticker = ticker
        self.alive = True

    def run(self): #웹소켓으로 코인 데이터를 받아 전송해준다
        #wm = WebSocketManager("ticker", [self.ticker])
        wm = upbitWebsocket.WebSocketManager("ticker", [self.ticker])
        while self.alive:
            data = wm.get()
            self.dataSent.emit(str  (data['code'               ]),
                               float(data['trade_price'        ]),
                               float(data['signed_change_rate' ]),
                               float(data['acc_trade_price_24h']))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ob = OverviewWidget()
    ob.show()
    exit(app.exec_())
