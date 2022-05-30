# -*- coding: utf-8 -*-
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from bs4 import BeautifulSoup
import requests
import sys
from dataclasses import dataclass


@dataclass
class UserSettings:
    absolute_path: str
    filename: str
    create_json: bool


user_settings = UserSettings(
    absolute_path=os.getcwd(),
    create_json=False,
    filename='file'
)


class SettingsWindow(QWidget):
    def __init__(self, parent, **kwargs):
        super().__init__(parent=None, **kwargs)
        self.resize(500, 200)
        self.setFixedSize(500, 200)
        self.setWindowTitle("Settings")
        self.setWindowIcon(QIcon('icons/settings.svg'))
        self.selectDirectoryWindow = QtWidgets.QFileDialog()
        self.selectDirectoryWindow.setWindowTitle('Select directory')
        self.selectDirectoryWindow.setWindowIcon(QIcon('icons/settings.svg'))

        self.error_message = QLabel(self)
        self.createJson = QCheckBox()
        self.fieldDirectoryPath = QLineEdit(self)
        self.filename = QLineEdit(self)
        self.buttonDirectoryPath = QPushButton('...', self)
        self.buttonSave = QPushButton('Save', self)
        self.createJson = QCheckBox(self)
        self.setup_ui()

    def setup_ui(self) -> None:
        self.error_message.setFont(QFont('Arial', 10))
        self.error_message.move(40, 10)
        self.error_message.setVisible(False)

        self.fieldDirectoryPath.setPlaceholderText('Path to folder: ')
        self.fieldDirectoryPath.textChanged.connect(self.path_field_changed)
        self.fieldDirectoryPath.resize(370, 40)
        self.fieldDirectoryPath.move(40, 40)
        self.fieldDirectoryPath.setText(user_settings.absolute_path)

        self.filename.setPlaceholderText('Filename: ')
        self.filename.resize(370, 40)
        self.filename.move(40, 100)
        self.filename.setText(user_settings.filename)

        self.createJson.setText('Create JSON')
        self.createJson.move(40, 150)
        self.createJson.setChecked(user_settings.create_json)

        self.buttonDirectoryPath.resize(40, 40)
        self.buttonDirectoryPath.move(420, 40)
        self.buttonDirectoryPath.clicked.connect(self.click_select_directory)

        self.buttonSave.clicked.connect(self.click_save)
        self.buttonSave.resize(50, 35)
        self.buttonSave.move(360, 145)

    def click_select_directory(self) -> None:
        self.selectDirectoryWindow.show()
        self.selectDirectoryWindow.setFileMode(self.selectDirectoryWindow.Directory)
        self.selectDirectoryWindow.setOptions(self.selectDirectoryWindow.DontUseNativeDialog)
        if self.selectDirectoryWindow.exec_() == QDialog.Accepted:
            path = self.selectDirectoryWindow.selectedFiles()[0]
            self.fieldDirectoryPath.setText(path)

    def click_save(self) -> None:
        path = self.fieldDirectoryPath.text()
        if os.path.exists(path):
            user_settings.absolute_path = self.fieldDirectoryPath.text()
            user_settings.filename = self.filename.text()
            user_settings.create_json = self.createJson.isChecked()
            self.close()
        else:
            self.invalid_path()

    def set_path_field_red_color(self) -> None:
        self.fieldDirectoryPath.setStyleSheet("QLineEdit"
                                              "{"
                                              "background-color : #ff6161;"
                                              "}"
                                              )

    def set_path_field_white_color(self) -> None:
        self.fieldDirectoryPath.setStyleSheet("QLineEdit"
                                              "{"
                                              "background-color : white;"
                                              "}"
                                              )

    def invalid_path(self) -> None:
        self.set_path_field_red_color()
        self.error_message.setText('Invalid path')
        self.error_message.setVisible(True)

    def path_field_changed(self) -> None:
        self.set_path_field_white_color()
        self.error_message.setVisible(False)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.high = 700
        self.weight = 200
        self.resize(self.high, self.weight)
        self.centralWidget()
        self.setFixedSize(self.high, self.weight)

        self.error_message = QLabel(self)
        self.button = QPushButton('Parse', self)
        self.settings_button = QPushButton('Settings', self)
        self.textbox = QLineEdit(self)
        self.textbox2 = QLineEdit(self)
        self.setWindowTitle("Parser")
        self.setWindowIcon(QIcon('icons/icon-planet.svg'))

        self.setup_ui()

    def setup_ui(self) -> None:
        """initialize components"""
        self.error_message.setFont(QFont('Arial', 12))
        self.error_message.resize(120, 40)
        self.error_message.move(40, 0)
        self.error_message.setVisible(False)

        self.textbox.move(40, 40)
        self.textbox.resize(500, 40)
        self.textbox.textChanged.connect(self.url_text_box_changed)
        self.textbox.setPlaceholderText('Input url:')

        self.textbox2.move(40, 90)
        self.textbox2.resize(500, 40)
        self.textbox2.setPlaceholderText('Input tag:')

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
        self.settings_button.move(440, 140)

    def parse_click(self) -> None:
        """Check url exists and save html file"""
        try:
            url = self.textbox.text()
            request_status = requests.head(url).status_code
            print(request_status)
            if 300 > request_status >= 200:
                request_html = requests.get(url).text
                with open('index.html', 'w', encoding='utf-8') as file:
                    file.write(request_html)
            else:
                self.url_not_found()
        except OSError:
            # fix nvidia error
            self.invalid_input()

    def open_settings_dialog(self) -> None:
        """Open window with settings(save path)"""
        self.settingsWindow = SettingsWindow(self)
        self.settingsWindow.show()

    def set_textbox_white_color(self) -> None:
        self.textbox.setStyleSheet("QLineEdit"
                                   "{"
                                   "background-color : white;"
                                   "}"
                                   )

    def set_textbox_red_color(self) -> None:
        self.textbox.setStyleSheet("QLineEdit"
                                   "{"
                                   "background-color : #ff6161;"
                                   "}"
                                   )

    def url_text_box_changed(self) -> None:
        # self.textbox.palette().setColor(QPalette.Highlight, QColor('white'))
        self.set_textbox_white_color()
        self.error_message.setVisible(False)

    def invalid_input(self) -> None:
        self.set_textbox_red_color()
        self.error_message.setText('Invalid input')
        self.error_message.setVisible(True)

    def url_not_found(self) -> None:
        self.set_textbox_red_color()
        self.error_message.setText('Url not found')
        self.error_message.setVisible(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
