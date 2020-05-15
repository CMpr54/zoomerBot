# coding: utf8

import logging
import telebot
from telebot import types
import sqlite3
import schedule
from multiprocessing import Process
from random import choice
from datetime import datetime
import requests
import time

"""
                                         Подгтовка к запуску
"""

# настройка логов
logging.getLogger('schedule').propagate = False
logging.basicConfig(level=logging.INFO)

# Токен стесняется, не смотрите
bot = telebot.TeleBot('1268099740:AAFm0gKTZTnAy2bHSXlTINIibFfaDzbKtFY')

timetable = {"Friday": {
    "9А": ["Алгебра", "Алгебра", "Русский язык", "Литература", "Физическая культура", "Биология"],
    "10А": ["Математика", "География", "Биология", "Физика", "Астрономия", "Литература"]
                        },

            "Saturday": {
    "9А": ["Физика", "Русский язык", "Литература", "Английский язык", "Химия", "Немецкий язык"],
    "10А": ["Обществознание", "Обществознание", "Математика", "Физическая культура", "Родной язык", "Родная литература"]
                        }
            }

format_date = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

keyboard_main = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_main.add("Изменить данные")


# класс для хранения информации о юзере
class User:
    def __init__(self, fio=None, email=None, num_class=None, letter_class=None, change=False):
        self.fio = fio
        self.email = email
        self.num_class = num_class
        self.letter_class = letter_class
        self.change = change

    def update(self, fio=None, email=None, num_class=None, letter_class=None, change=False):
        self.fio = fio
        self.email = email
        self.num_class = num_class
        self.letter_class = letter_class
        self.change = change

    def __str__(self):
        return "{} {} {}{}".format(self.fio, self.email, self.num_class,  self.letter_class)

    def __repr__(self):
        return "{} {} {}{}".format(self.fio, self.email, self.num_class,  self.letter_class)


"""
                                        Вычислительные функции
"""


def data_day():
    today = datetime.today()
    weekday = format_date[datetime.weekday(today)]

    day = today.day
    month = today.month

    if day < 10:
        day = '0{}'.format(day)
    if month < 10:
        month = '0{}'.format(month)

    return ['{}.{}.{}'.format(day, month, today.year), weekday]


# url = "https://docs.google.com/forms/d/e/1FAIpQLSe9AVNY-Ff0JJvAqX4nEz2-ueiAQwPVNnZRZlToiBAgVanmYA/formResponse"
url = "https://docs.google.com/forms/d/e/1FAIpQLSczAO0SaL-V6YgpPUvCeag-HYdl1IQ9JEViUNAUu5Y8yBfxFw/formResponse"


def get_values(num_class, letter_class, fio, date, subject, email):
    values_list = []
    values = {
        # class
        "entry.1636959309": "{}".format(num_class),
        # class letter
        "entry.1528634530": "{}".format(letter_class),
        # FIO
        "entry.1437687741": "{}".format(fio),
        # data
        "entry.1630759217": "{}".format(date),
        # subject
        "entry.1620919827": "{}".format(subject),
        # email
        "entry.1076833356": "{}".format(email),
            }

    # values = {
    #     "entry.452086364": "{}".format(fio),
    #     # class letter
    #     "entry.1367140281": "{}".format("Физика"),
    #     # FIO
    # }

    values_list.append(values)

    return values_list


def send_attendance(url, data):
    for d in data:
        try:
            requests.post(url, data=d)
            logging.info("Form Submitted.")
            time.sleep(3)
        except Exception as send_error:
            logging.warning("send_error {}".format(send_error))


def job(n):
    global dictionary_of_users
    dictionary_update()
    date, weekday = data_day()
    if weekday == "Sunday":
        return
    for i in dictionary_of_users.keys():
        user = dictionary_of_users[i]
        try:
            subject = timetable[weekday][str(user.num_class) + user.letter_class][n]
            send_attendance(url, get_values(user.num_class, user.letter_class, user.fio, date, subject, user.email))
        except IndexError:
            pass
    logging.info("----------------------------------------------------------------------------------------------------")


# обновление словаря юзеров
def dictionary_update():
    global dictionary_of_users
    con = sqlite3.connect("Zommer_db")
    cur = con.cursor()
    result = cur.execute("SELECT id, FIO, email, num_class, letter_class FROM users").fetchall()
    con.close()
    for info in result:
        dictionary_of_users[info[0]] = User(fio=info[1], email=info[2], num_class=info[3], letter_class=info[4])


# создание и заполнение словаря пользователей
dictionary_of_users = {}
dictionary_update()


# процесс проверки времени
def check_time():
    while True:
        schedule.run_pending()
        # ваш код проверки времени и отправки сообщений по таймеру
        # пауза между проверками, чтобы не загружать процессор
        time.sleep(60)


def check_users():
    logging.info("----------------------------------------------------------------------------------------------------")
    dictionary_update()
    for i in dictionary_of_users.values():
        print(i)
    print(len(dictionary_of_users), "num_of_users")
    logging.info("----------------------------------------------------------------------------------------------------")


# создание процесса
p1 = Process(target=check_time, args=())

# ну тут понятно
schedule.every().hour.do(check_users)
schedule.every().day.at("06:00").do(job, 0)
schedule.every().day.at("06:30").do(job, 1)
schedule.every().day.at("07:00").do(job, 2)
schedule.every().day.at("07:30").do(job, 3)
schedule.every().day.at("08:00").do(job, 4)
schedule.every().day.at("08:30").do(job, 5)
schedule.every().day.at("09:00").do(job, 6)
# schedule.every().minute.do(job, 0)

"""
                                        Хэндлеры
"""


def check(data):
    data = data.split('\n')
    if len(data) != 4:
        return False
    elif len(data[0].split()) != 3:
        return False
    elif data[2] not in ['9', '10']:
        return False
    elif data[3] != 'А':
        return False
    else:
        return True


# самое первое и самое волнительное сообщение
@bot.message_handler(commands=['start'])
def start_message(message):
    try:
        tel_id = message.from_user.id
        if tel_id not in dictionary_of_users.keys():
            bot.send_message(message.chat.id, 'Введи ФИО, email, класс и литеру класса\nПример:')
            bot.send_message(message.chat.id, 'Багрянский Константин Дмитриевич\nnanaviju@mail.ru\n10\nА')

            dictionary_of_users[tel_id] = User(change=True)

            logging.info('New user')
        else:
            if dictionary_of_users[tel_id].fio:
                bot.send_message(message.chat.id, 'Мы встречались, {}'.format(dictionary_of_users[tel_id].fio),
                                 reply_markup=keyboard_main)
    except Exception as start_error:
        logging.error('/start {}'.format(start_error.__class__.__name__))


# все основные сообщения идут сюда
@bot.message_handler(content_types=['text'])
def send_text(message):
    try:
        tel_id = message.from_user.id
        if dictionary_of_users[tel_id].change:
            if check(message.text):
                fio, email, num_class, letter_class = message.text.split("\n")
                dictionary_of_users[tel_id].update(fio=fio, email=email, num_class=num_class,
                                                   letter_class=letter_class, change=False)
                con = sqlite3.connect("Zommer_db")
                cur = con.cursor()
                cur.execute("DELETE from users WHERE id = {}".format(tel_id))
                cur.execute(
                    """INSERT INTO users (id, FIO, email, num_class, letter_class) VALUES ({}, "{}", "{}", {}, "{}")""".format(
                        tel_id, fio, email, num_class, letter_class))
                con.commit()
                con.close()
                bot.send_message(message.chat.id, 'Успешно', reply_markup=keyboard_main)
            else:
                bot.send_message(message.chat.id, 'Некорректное значение')
        elif not dictionary_of_users[tel_id].change:
            if message.text.lower() == 'изменить данные':
                dictionary_of_users[tel_id].change = True
                bot.send_message(message.chat.id, 'Введи ФИО, email, класс и литеру класса\nПример:')
                example = ['Багрянский Константин Дмитриевич\nnanaviju@mail.ru\n10\nА',
                           'Молотов Кирилл Дмитриевич\nrandom@mail.ru\n9\nА',
                           'Маршалов Максим Сергеевич\nnanaviju@mail.ru\n10\nА']
                bot.send_message(message.chat.id, choice(example))
    except Exception as main_error:
        logging.error('Unknown error in main {}'.format(main_error))


"""
                                        Запуск бота
"""
# ну это main, тут всё ясно
if __name__ == '__main__':
    p1.start()  # запускаем проверку в отдельном потоке
    while True:  # цикл что бы при падении серверов телеграма бот жил
        try:
            bot.polling(none_stop=True)
        except Exception as error:
            logging.fatal("{} LAST CHANCE".format(error.__class__.__name__))
        time.sleep(300)  # а это что бы он не нагружал систему запросами в случае падения серверов телеграма
