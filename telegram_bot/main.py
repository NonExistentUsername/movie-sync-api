import telebot
import api
from api import Client
import time
import sys
import os

USER_LOGIN = os.getenv("USER_LOGIN")
USER_PASSWORD = os.getenv("USER_PASSWORD")
API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

ADMINS = [472519122, 1028805497]

ANSWER = "Команду відправлено на виконання 👀"

client = Client(username=USER_LOGIN, password=USER_PASSWORD)

if not client.is_authorized:
    try:
        client.login(USER_LOGIN, USER_PASSWORD)
    except api.ApiException as e:
        print(e.message)
        sys.exit(-1)

bot = telebot.TeleBot(API_TOKEN, threaded=False)

bot.remove_webhook()
time.sleep(1)
print("Start done")

def str_from_user(user: api.User) -> str:
    return f'💳 Нікнейм: {user.username}\n🔑 Адмін: {user.is_admin}\n🗝 Має доступ: {user.have_access}'


def str_error(error: str) -> str:
    return f'Error: {error}'


def try_change_user_rights(message: telebot.types.Message, **kwargs):
    if message.from_user.id in ADMINS:
        data = message.text.split(' ')
        if len(data) == 2:
            try:
                message_text = str_from_user(client.update_rights(data[1], **kwargs))
            except api.ApiException as error:
                message_text = str_error(error.message)
            bot.reply_to(message, message_text)


# @bot.message_handler(commands=['add_admin'])
# def add_admin(message: telebot.types.Message):
#     try_change_user_rights(message, is_admin=True)
#
#
# @bot.message_handler(commands=['remove_admin'])
# def remove_admin(message: telebot.types.Message):
#     try_change_user_rights(message, is_admin=False)


# @bot.message_handler(commands=['add_access'])
# def add_command_receiver(message: telebot.types.Message):
#     try_change_user_rights(message, receives_commands=True)


# @bot.message_handler(commands=['remove_access'])
# def remove_command_receiver(message: telebot.types.Message):
#     try_change_user_rights(message, receives_commands=False)


@bot.message_handler(commands=['get_user'])
def get_user(message: telebot.types.Message):
    if message.from_user.id in ADMINS:
        data = message.text.split(' ')
        if len(data) == 2:
            try:
                message_text = str_from_user(client.get_user(data[1]))
            except api.ApiException as e:
                message_text = e.message
            bot.reply_to(message, message_text)


@bot.message_handler(commands=['open_url'])
def open_url(message: telebot.types.Message):
    if message.from_user.id in ADMINS:
        data = message.text.split(' ')
        if len(data) == 2:
            try:
                client.send_command("room_name", "open_url", data[1])
                message_text = ANSWER
            except api.ApiException as error:
                message_text = str_error(error.message)
            bot.reply_to(message, message_text)


class Handler:
    def __init__(self, func_filter, func):
        self.__filter = func_filter
        self.__func = func

    def check(self, message):
        return self.__filter(message)

    def run(self, message):
        return self.__func(message)


handlers = []


def add_handler(filter):
    def decorator(func):
        handlers.append(Handler(filter, func))
        return func

    return decorator


@add_handler(filter=lambda message: message in ['включай', 'Включай', 'включити', 'Включити', 'тикай', 'Тикай'])
def start_playing(message):
    client.send_command("sunshine", "start")


@add_handler(filter=lambda message: message in ['паузу', 'пауза', 'Паузу', 'Пауза'])
def stop_playing(message):
    client.send_command("sunshine", "pause")


def open_url_filter(message):
    data = message.split()
    return len(data) == 2 and data[0] in ['Відкрити', 'відкрити']


@add_handler(filter=open_url_filter)
def open_url(message):
    data = message.split()
    client.send_command("sunshine", "open_url", data[1])


def handle_message(message):
    for handler in handlers:
        if handler.check(message):
            handler.run(message)
            return True
    return False


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if message.from_user.id in ADMINS:
        try:
            handled = handle_message(message.text)
            if handled:
                bot.reply_to(message, ANSWER)
        except api.ApiException as e:
            bot.reply_to(message, e.message)


if __name__ == '__main__':
    bot.infinity_polling()
