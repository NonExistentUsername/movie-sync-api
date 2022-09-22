from pynput.keyboard import Key, Controller
import webbrowser

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


@add_handler(command="stop")
def stop_playing(param):
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
