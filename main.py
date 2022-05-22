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
        self.high = 600
        self.weight = 600
        self.setup_ui()

    def setup_ui(self):
        self.resize(self.high, self.weight)
        self.centralWidget()
        self.setFixedSize(self.high, self.weight)
        self.textbox = QLineEdit(self)
        self.textbox.move(100, 100)
        self.textbox.resize(400, 40)
        self.textbox2 = QLineEdit(self)
        self.textbox2.move(100, 200)
        self.textbox2.resize(400, 40)
        self.label = QLabel('<h1>Enter url<h1>', self)
        self.label.resize(600, 50)
        self.label.move(0, 55)
        self.button = QPushButton('Parse', self)
        self.button.resize(100, 50)
        self.button.clicked.connect(self.parse_click)
        self.label.setAlignment(Qt.AlignCenter)
        self.button.setStyleSheet("QPushButton"
                                  "{"
                                  "background-color : lightblue;"
                                  "border-radius : 5px"
                                  "}"
                                  "QPushButton::pressed"
                                  "{"
                                  "background-color : yellow;"
                                  "}")
        self.button.move(250, 300)

    def parse_click(self):
        url = self.textbox.text()
        html = requests.get(url).text
        print(html)
        with open('index.html', 'w', encoding='utf-8') as file:
            file.write(html)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()

    win.show()
    sys.exit(app.exec_())
