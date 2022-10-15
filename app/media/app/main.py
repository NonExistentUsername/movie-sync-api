from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import (
    Qt, QObject, pyqtSignal, QRunnable, pyqtSlot, QThreadPool, QCoreApplication
)
from datetime import datetime
import requests
import time
import urllib.request

# APP_GET_LAST_UPDATE: str = "https://ekxb35fje-private-web-api.herokuapp.com/app/last_update"
# APP_DOWNLOAD_URL: str = "https://ekxb35fje-private-web-api.herokuapp.com/app/download"

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("MirumApp")

        self.label = QtWidgets.QLabel(text="Text", parent=self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.adjustSize()

        self.progress_bar = QtWidgets.QProgressBar(parent=self)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximumHeight(10)

        button = QtWidgets.QPushButton("Test")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label, 0)
        # layout.addWidget(self.progress_bar, 2)
        layout.addWidget(button)
        layout.setContentsMargins(20, 10, 20, 10)

        self.setFixedSize(300, 50)
        self.setLayout(layout)

    def change_label_to_extracting(self, extracting_start: bool):
        if extracting_start:
            self.label.setText("Extracting")
            self.label.adjustSize()

    def update_progress(self, n: int):
        self.progress_bar.setValue(n)
