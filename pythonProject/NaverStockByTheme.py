import sys
import os
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QDesktopWidget, QMessageBox, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTime, QDate, Qt
#  유투브 순수 영상 주소 https://www.youtube.com/embed/M7lc1UVf-VE
IconPath = "{0}\\naver.png".format(os.path.abspath(os.getcwd()))


class NaverStockByTheme(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(IconPath))
        self.setWindowTitle('네이버 주식 테마 조지기')
        self.bottomStatus('init')
        self.btnQuit = QPushButton('종료', self)
        self.btnTest = QPushButton('테스트', self)
        self.btnSetCenter = QPushButton('창중앙이동', self)
        self.current_date = QDate.currentDate()
        self.makeButton()
        self.initUI()

    def bottomStatus(self, types):
        self.statusBar().setStyleSheet("background-color: rgb( 0, 51, 0); color: white;")
        if types is None:
            types = 'init'
        if types == 'init':
            self.statusBar().showMessage('준비')
        elif types == 'proc':
            self.statusBar().showMessage('검색중')
        elif types == 'err':
            self.statusBar().showMessage('에러발생')
        elif types == 'off':
            self.statusBar().clearMessage()
        elif types == 'time':
            current_time = QTime.currentTime().toString(Qt.DefaultLocaleShortDate)
            self.statusBar().showMessage(self.current_date.toString(Qt.DefaultLocaleLongDate) + " | " + current_time)

    def makeButton(self):
        # 종료버튼
        self.btnQuit.move(1520, 850)
        self.btnQuit.resize(self.btnQuit.sizeHint())
        self.btnQuit.released.connect(lambda: self.messageBox('에러 없이 종료는 무서워'))
        # 가운데로 창이동
        self.btnSetCenter.move(1360, 850)
        self.btnSetCenter.resize(self.btnSetCenter.sizeHint())
        self.btnSetCenter.clicked.connect(self.windowToCenter)
        # 테스트 버튼
        self.btnTest.move(1440, 850)
        self.btnTest.resize(self.btnTest.sizeHint())
        self.btnTest.clicked.connect(lambda: self.bottomStatus('time'))

    def windowToCenter(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def messageBox(self, types):
        if type(types) != str:
            text = "어떻게 할래요 ?"
        else:
            text = types

        QMessageBox.about(self, '알림', text)

    def initUI(self):
        self.setGeometry(512, 250, 1600, 900)  # 창의 위치 , 창의 크기
        self.show()

    @staticmethod
    def closeWindow():
        QCoreApplication.instance().quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = NaverStockByTheme()
    sys.exit(app.exec_())
