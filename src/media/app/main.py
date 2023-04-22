import threading

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import Qt, QObject, pyqtSignal, QRunnable, pyqtSlot, QThreadPool, QCoreApplication, QEvent
from datetime import datetime
from app.api import *
import requests
import os
import asyncio
import webbrowser
from pynput.keyboard import Key, Controller

APP_GET_LAST_UPDATE: str = "http://127.0.0.1:8000/app/last_update"
APP_DOWNLOAD_URL: str = "http://127.0.0.1:8000/app/download"

DATE_FORMAT: str = "%Y-%m-%dT%H:%M:%S.%f"

EXCLUDE_PATHS = [
    "__MACOSX/",
]


keyboard = Controller()

handlers = {}


def add_handler(command):
    def decorator(func):
        handlers[command] = func
        return func

    return decorator


@add_handler(command="start")
def start_playing(param):
    keyboard.tap(Key.media_play_pause)


@add_handler(command="pause")
def stop_playing(param):
    print("PAUSE")
    keyboard.tap(Key.media_play_pause)


@add_handler(command="next")
def next_video(param):
    keyboard.tap(Key.media_next)


@add_handler(command="open_url")
def open_url(param):
    if isinstance(param, str):
        webbrowser.open(param)


def handle_command(command: str, param: str) -> bool:
    if command in handlers:
        handlers[command](param)
        return True
    return False


class RegisterWindow(QWidget):
    open_login_window = pyqtSignal()
    try_register = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("MirumApp Register")

        self.label = QtWidgets.QLabel(text="Register", parent=self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.adjustSize()
        self.label.setMaximumHeight(15)

        self.username = QtWidgets.QLineEdit(parent=self)
        self.username.setPlaceholderText("Username")
        self.username.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.password = QtWidgets.QLineEdit(parent=self)
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.cofirm_password = QtWidgets.QLineEdit(parent=self)
        self.cofirm_password.setPlaceholderText("Confirm password")
        self.cofirm_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        register_button = QtWidgets.QPushButton("Register")
        register_button.setFixedWidth(100)
        register_button.setMaximumHeight(45)
        register_button.clicked.connect(self.try_register_clicked)

        login_button = QtWidgets.QPushButton("Login")
        login_button.setFixedWidth(100)
        login_button.setMaximumHeight(45)
        login_button.clicked.connect(lambda: self.open_login_window.emit())

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.cofirm_password)
        layout.addWidget(register_button)
        layout.setAlignment(register_button, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(login_button)
        layout.setAlignment(login_button, Qt.AlignmentFlag.AlignCenter)

        layout.setContentsMargins(20, 10, 20, 10)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)
        self.setFixedSize(300, 210)

    def try_register_clicked(self):
        if self.password.text() != self.cofirm_password.text():
            result = QtWidgets.QMessageBox.critical(
                self, "Error", "Passwords doesn't match.", QtWidgets.QMessageBox.StandardButton.Close
            )
        else:
            self.try_register.emit(self.username.text(), self.password.text())


class LoginWindow(QWidget):
    open_register_window = pyqtSignal()
    try_login = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("MirumApp Login")

        self.label = QtWidgets.QLabel(text="Login", parent=self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.adjustSize()
        self.label.setMaximumHeight(15)

        self.username = QtWidgets.QLineEdit(parent=self)
        self.username.setPlaceholderText("Username")
        self.username.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.password = QtWidgets.QLineEdit(parent=self)
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        login_button = QtWidgets.QPushButton("Login")
        login_button.setFixedWidth(100)
        login_button.setMaximumHeight(45)
        login_button.clicked.connect(self.try_login_clicked)

        register_button = QtWidgets.QPushButton("Register")
        register_button.setFixedWidth(100)
        register_button.setMaximumHeight(45)
        register_button.clicked.connect(lambda: self.open_register_window.emit())

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(login_button)
        layout.setAlignment(login_button, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(register_button)
        layout.setAlignment(register_button, Qt.AlignmentFlag.AlignCenter)

        layout.setContentsMargins(20, 10, 20, 10)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)
        self.setFixedSize(300, 180)

    def try_login_clicked(self):
        self.try_login.emit(self.username.text(), self.password.text())


class JoinRoomWindow(QWidget):
    try_join_room = pyqtSignal(str, str)
    join_room_closed = pyqtSignal()

    def __init__(self):
        super(JoinRoomWindow, self).__init__()
        self.setWindowTitle("Join Room")

        self.room_name = QtWidgets.QLineEdit(parent=self)
        self.room_name.setPlaceholderText("Name")
        self.room_name.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.room_key = QtWidgets.QLineEdit(parent=self)
        self.room_key.setPlaceholderText("Key")
        self.room_key.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        join_room_button = QtWidgets.QPushButton("Join room")
        join_room_button.setFixedWidth(100)
        join_room_button.setMaximumHeight(45)
        join_room_button.clicked.connect(lambda: self.try_join_room.emit(self.room_name.text(), self.room_key.text()))

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.room_name)
        layout.addWidget(self.room_key)
        layout.addWidget(join_room_button)
        layout.setAlignment(join_room_button, Qt.AlignmentFlag.AlignCenter)

        layout.setContentsMargins(20, 10, 20, 10)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)
        self.setFixedSize(300, 100)

    def closeEvent(self, event):
        self.join_room_closed.emit()


class MainWindow(QWidget):
    logout = pyqtSignal()

    def __show_error(self, error_message):
        result = QtWidgets.QMessageBox.critical(
            self, "Error", str(error_message), QtWidgets.QMessageBox.StandardButton.Close
        )

    def __get_all_rooms(self) -> List[Room]:
        result = []

        cur_page = 1
        page_size = 50
        rooms = self.client.get_rooms(page=cur_page, size=page_size)
        total_room_names = rooms.total
        result.extend(rooms.items)
        while total_room_names > len(result):
            rooms = self.client.get_rooms()
            result.extend(rooms.items)
            total_room_names = rooms.total
        return result

    def __try_join_to_room(self, room_name: str, room_key: str):
        try:
            self.client.join_room(room_name, room_key)
            self.__update_list_of_rooms()

            if self.join_room_window:
                self.join_room_window.close()
                self.join_room_window = None

        except ApiException as e:
            self.__show_error(e.message)

    def __clear_join_window(self):
        self.join_room_window = None

    def __open_join_room_window(self):
        if self.join_room_window is None:
            self.join_room_window = JoinRoomWindow()
            self.join_room_window.try_join_room.connect(self.__try_join_to_room)
            self.join_room_window.join_room_closed.connect(self.__clear_join_window)
            self.join_room_window.show()

    def __try_get_all_rooms(self) -> List[Room]:
        try:
            return self.__get_all_rooms()
        except ApiException as e:
            self.__show_error(e.message)
            return []

    def __update_list_of_rooms(self):
        if self.client.me.have_access:
            rooms = self.__try_get_all_rooms()
            self.list_of_rooms.clear()
            for room in rooms:
                self.list_of_rooms.addItem(room.room_name)

    def __receive_command(self, command: Command):
        handle_command(command.command, command.param)
        return self.__run_listening_function

    def __listening_function(self):
        while self.__run_listening_function:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            loop.run_until_complete(self.client.ws_get_command(self.__receive_command))
            loop.close()
        self.start_button.setDisabled(False)

    def __stop_start_listening(self):
        if self.client.me.have_access:
            if not self.__run_listening_function:
                self.__run_listening_function = True
                self.__listening_thread = threading.Thread(target=self.__listening_function, daemon=True)
                self.__listening_thread.start()
                self.start_button.setText("Stop")
            else:
                self.__run_listening_function = False
                self.start_button.setText("Start")
                self.start_button.setDisabled(True)
        else:
            self.__show_error("You don't have access.")

    def __init__(self, client: Client):
        super().__init__()
        self.__run_listening_function = False
        self.join_room_window = None
        self.client = client

        self.setWindowTitle("MirumApp")

        top_bar_layout = QtWidgets.QHBoxLayout()
        logout_button = QtWidgets.QPushButton("Logout")
        logout_button.setMaximumWidth(60)
        user_info_button = QtWidgets.QPushButton("Info")
        user_info_button.setMaximumWidth(60)
        client_me: User = self.client.me
        username_label = QtWidgets.QLabel(client_me.username)

        top_bar_layout.addWidget(username_label)
        top_bar_layout.addWidget(user_info_button)
        top_bar_layout.addWidget(logout_button)

        self.list_of_rooms = QtWidgets.QListWidget(self)
        self.leave_room_menu = QtWidgets.QMenu(self.list_of_rooms)
        self.leave_room_menu.addAction("Leave", self.__leave_from_selected_rooms)
        self.list_of_rooms.installEventFilter(self)
        self.__update_list_of_rooms()

        self.start_button = QtWidgets.QPushButton("Start")
        self.start_button.clicked.connect(self.__stop_start_listening)
        join_room_button = QtWidgets.QPushButton("Join room")
        join_room_button.clicked.connect(self.__open_join_room_window)
        footer_layout = QtWidgets.QHBoxLayout()
        footer_layout.addWidget(self.start_button)
        footer_layout.addWidget(join_room_button)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(top_bar_layout)
        layout.addWidget(self.list_of_rooms)
        layout.addLayout(footer_layout)
        # layout.setAlignment(join_room_button, Qt.AlignmentFlag.AlignRight)

        layout.setContentsMargins(20, 10, 20, 10)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)
        self.setFixedSize(300, 300)

    def __leave_from_selected_rooms(self):
        selected_items = self.list_of_rooms.selectedItems()
        for item in selected_items:
            try:
                self.client.leave_room(item.text())
            except ApiException as e:
                pass
        self.__update_list_of_rooms()

    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.ContextMenu:
            if source == self.list_of_rooms and len(self.list_of_rooms.selectedItems()) > 0:
                self.leave_room_menu.exec(event.globalPos())
                return True
        return super().eventFilter(source, event)


class Controller:
    def __try_load_authorization(self) -> Optional[Authorization]:
        if not os.path.isfile(self.__authorization_file_name):
            return None

        result = None
        with open(self.__authorization_file_name, "r") as file:
            try:
                result = Authorization(**json.load(file))
            except Exception as e:
                pass
        return result

    def __try_save_authorization(self):
        if self.client.is_authorized:
            with open(self.__authorization_file_name, "w") as file:
                try:
                    json.dump(self.client.authorization.asdict(), file)
                except Exception as e:
                    pass

    def __init__(self):
        self.__authorization_file_name = "authorization.json"
        self.main_window = None
        self.login_window = None
        self.register_window = None
        authorization = self.__try_load_authorization()
        self.client = Client(authorization=authorization)
        self.__try_save_authorization()

    def show_error(self, error_message: str):
        parent = self.login_window or self.main_window or self.register_window

        if parent:
            result = QtWidgets.QMessageBox.critical(
                self.login_window, "Error", str(error_message), QtWidgets.QMessageBox.StandardButton.Close
            )

    def try_register(self, username: str, password: str):
        try:
            self.client.register(username, password)
        except ApiException as e:
            self.show_error(e.message)

        if self.client.is_authorized:
            self.__try_save_authorization()
            self.show_app_window()

    def try_login(self, username: str, password: str):
        try:
            self.client.login(username, password)
        except ApiException as e:
            self.show_error(e.message)

        if self.client.is_authorized:
            self.__try_save_authorization()
            self.show_app_window()

    def show_register_window(self):
        self.register_window = RegisterWindow()
        self.register_window.open_login_window.connect(self.show_login_window)
        self.register_window.try_register.connect(self.try_register)
        if self.main_window:
            self.main_window.close()
            self.main_window = None
        if self.login_window:
            self.login_window.close()
            self.login_window = None
        self.register_window.show()

    def show_login_window(self):
        self.login_window = LoginWindow()
        self.login_window.try_login.connect(self.try_login)
        self.login_window.open_register_window.connect(self.show_register_window)
        if self.main_window:
            self.main_window.close()
            self.main_window = None
        if self.register_window:
            self.register_window.close()
            self.register_window = None
        self.login_window.show()

    def show_app_window(self):
        self.main_window = MainWindow(self.client)
        if self.login_window:
            self.login_window.close()
            self.login_window = None
        if self.register_window:
            self.register_window.close()
            self.register_window = None
        self.main_window.show()

    def start(self):
        if self.client.is_authorized:
            self.show_app_window()
        else:
            self.show_login_window()

    def __del__(self):
        self.__try_save_authorization()
