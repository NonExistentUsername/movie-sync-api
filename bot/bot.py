import telebot
import api
from api import Client
import time
import sys

USER_LOGIN = 'bot_admin'
USER_PASSWORD = 'PD1sY6RSj8%8'
API_TOKEN = '5229850971:AAH_GD0tJEfSY5bvbjIbi89D_uv7C5pRqEw'

ADMINS = [472519122, 1028805497]
SECRET = "IhLZlUssao"

ANSWER = "Команду відправлено на виконання 👀"

bot = telebot.TeleBot(API_TOKEN, threaded=False)
bot.remove_webhook()
time.sleep(20)

client = Client()
client.init()

if not client.is_authorized:
    try:
        client.login(USER_LOGIN, USER_PASSWORD)
    except api.ApiException as e:
        print(e.message)
        sys.exit(-1)

print("Authorized")
bot.send_message(ADMINS[0], "Authorized")


def str_from_user(user: api.User) -> str:
    return f'💳 Нікнейм: {user.nickname}\n🔑 Адмін: {user.is_admin}\n🗝 Отримує команди: {user.receives_commands}'


def try_change_user_rights(message: telebot.types.Message, **kwargs):
    if message.from_user.id in ADMINS:
        data = message.text.split(' ')
        if len(data) == 2:
            try:
                message_text = str_from_user(client.update_rights(data[1], **kwargs))
            except api.ApiException as e:
                message_text = e.message
            bot.reply_to(message, message_text)


@bot.message_handler(commands=['add_admin'])
def add_admin(message: telebot.types.Message):
    try_change_user_rights(message, is_admin=True)


@bot.message_handler(commands=['remove_admin'])
def remove_admin(message: telebot.types.Message):
    try_change_user_rights(message, is_admin=False)


@bot.message_handler(commands=['add_command_receiver'])
def add_command_receiver(message: telebot.types.Message):
    try_change_user_rights(message, receives_commands=True)


@bot.message_handler(commands=['remove_command_receiver'])
def remove_command_receiver(message: telebot.types.Message):
    try_change_user_rights(message, receives_commands=False)


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
                client.send_command("open_url", data[1])
                message_text = ANSWER
            except api.ApiException as e:
                message_text = e.message
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
    client.send_command("start")


@add_handler(filter=lambda message: message in ['паузу', 'пауза', 'Паузу', 'Пауза'])
def stop_playing(message):
    client.send_command("pause")


def open_url_filter(message):
    data = message.split()
    return len(data) == 2 and data[0] in ['Відкрити', 'відкрити']


@add_handler(filter=open_url_filter)
def open_url(message):
    data = message.split()
    client.send_command("open_url", data[1])


def handle_message(message):
    for handler in handlers:
        if handler.check(message):
            handler.run(message)
            return True
    return False


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if message.from_user.id in ADMINS:
        handled = handle_message(message.text)
        if handled:
            bot.reply_to(message, ANSWER)


bot.polling()
