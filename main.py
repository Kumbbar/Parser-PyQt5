from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from bs4 import BeautifulSoup
import requests
import sys


class MainWindow(QMainWindow):  # главное окно
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Parser")
        self.setWindowIcon(QIcon('icons/icon-planet.svg'))
        self.high = 700
        self.weight = 200
        self.setup_ui()

    def setup_ui(self):
        """initialize components"""
        self.resize(self.high, self.weight)
        self.centralWidget()
        self.setFixedSize(self.high, self.weight)
        self.textbox = QLineEdit(self)
        self.textbox.move(30, 30)
        self.textbox.resize(500, 40)
        self.textbox.setPlaceholderText('Input url:')
        self.textbox2 = QLineEdit(self)
        self.textbox2.move(30, 80)
        self.textbox2.resize(500, 40)
        self.textbox2.setPlaceholderText('Input tag:')
        self.button = QPushButton('Parse', self)
        self.button.resize(100, 200)
        self.button.clicked.connect(self.parse_click)
        self.button.setStyleSheet("QPushButton"
                                  "{"
                                  "background-color : #e0dbd7;"
                                  "border-radius : 5px"
                                  "}"
                                  "QPushButton::pressed"
                                  "{"
                                  "background-color : white;"
                                  "}"
                                  "{"
                                  "text-color : white;"
                                  "}"
                                  )
        self.button.move(600, 0)

        self.settings_button = QPushButton('Save settings', self)
        self.settings_button.resize(100, 40)
        self.settings_button.clicked.connect(self.open_settings_dialog)
        self.settings_button.setStyleSheet("QPushButton"
                                           "{"
                                           "background-color : #e0dbd7;"
                                           "border-radius : 5px"
                                           "}"
                                           "QPushButton::pressed"
                                           "{"
                                           "background-color : white;"
                                           "}"
                                           "{"
                                           "text-color : white;"
                                           "}"
                                           )
        self.settings_button.move(430, 130)

    def parse_click(self):
        """Check url exists and save html file"""
        try:
            url = self.textbox.text()
            request_status = requests.head(url).status_code
            print(request_status)
            if 300 > request_status >= 200:
                request_html = requests.get(url).text
                with open('index.html', 'w', encoding='utf-8') as file:
                    file.write(request_html)
        except ValueError:
            return 0

    def open_settings_dialog(self):
        """Open window with settings(save path)"""
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
