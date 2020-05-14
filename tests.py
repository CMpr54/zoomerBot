# coding: utf8

import logging
import telebot
from telebot import types
import sqlite3
import schedule
import json
import time
import apiai
from multiprocessing import Process
from random import choice
from datetime import datetime
from pytz import timezone, utc
import requests
from timezonefinder import TimezoneFinder

"""
                                         Подгтовка к запуску
"""
# настройка логов
logging.getLogger('schedule').propagate = False
logging.basicConfig(level=logging.INFO)
tf = TimezoneFinder()

# # открытие json
# with open('test.json') as f:
#     json_data = json.load(f)
#
# # проверка json
# if not json_data:
#     logging.fatal('Json is empty')

# Токен стесняется, не смотрите
bot = telebot.TeleBot('1085413551:AAHPzvywT2G8PabnoZNpsLabaRzQtLJtdfw')

# стикеры
sticker_brain = 'CAACAgIAAxkBAAIC3V6S1pvF1p86MLzrh3f5vIoPvX12AAINAAN2oqAv_LtzGV_Ox78YBA'
sticker_car = 'CAACAgIAAxkBAAIC316S1qMELdyaNMuhY5qDf2L42GecAAIOAAN2oqAvNi6qlYsoOd0YBA'
sticker_fingers = 'CAACAgIAAxkBAAIC4V6S1q1uAAHXa6sM_WeXebBTORHLQQACDwADdqKgL7oTqoU-rx61GAQ'
sticker_poster = 'CAACAgIAAxkBAAIC416S1raMHSSFFLK3ZQs-O76WfDHdAAIQAAN2oqAv0UvxdPK0oBEYBA'
sticker_stupid = 'CAACAgIAAxkBAAIC5V6S1sLMwlMpzSV-HzAUyxnANemBAAIRAAN2oqAvmdctZ8AmSBQYBA'
sticker_surprised = 'CAACAgIAAxkBAAIC516S1sqryWe7_N0jV-bHBSZkSrfLAAISAAN2oqAvECeADCokyIgYBA'
sticker_angry = 'CAACAgIAAxkBAAIC6V6S1tJi2JwarUOsCq574Lg0ch9EAAITAAN2oqAvM-23KXQpG6EYBA'
sticker_hey_you = 'CAACAgIAAxkBAAIC616S1tnFHWBhS1V8neTScUX0i4crAAIUAAN2oqAvY3pzo1XrUwkYBA'
sticker_really = 'CAACAgIAAxkBAAIEZF6Uj87bhHJDkTOcp563jtKxPcEWAAIVAAN2oqAv3236KzzF6VEYBA'
sticker_sad = 'CAACAgIAAxkBAAIEZl6UliNaJtcVxjbZWVk1jj075CUQAAIWAAN2oqAvTEMCrxw9_m0YBA'

# разнообразные списки и словари
list_of_stickers = [sticker_brain, sticker_car, sticker_fingers, sticker_poster, sticker_stupid, sticker_surprised,
                    sticker_angry, sticker_hey_you, sticker_really, sticker_sad]

list_of_time_zones = ["-11", "-10", "-9", "-8", "-7", "-6", "-5", "-4", "-3", "-2", "-1", "0", "+1", "+2", "+3", "+4",
                      "+5", "+6", "+7", "+8", "+9", "+10", "+11", "+12"]
list_of_phrases = ["Красавчик!", "Молодчина!", "Так держать!", "Огонь!", "Чётко!"]

dict_of_talks = {'greeting': 'разобрались как мне тебя называть',
                 'exercises': 'определились с твоими упражнениями', 'date_time': 'утвердили твоё расписание',
                 'training': 'закончили тренировку'}

dict_of_exercises = {"Отжимания": [0, 24], "Приседания": [0, 24], "Подтягивания": [0, 24], "Планка": [0, 24],
                     "Поднимание ног": [0, 24]}

days = {"понедельник": "Monday", "вторник": "Tuesday", "среда": "Wednesday", "четверг": "Thursday",
        "пятница": "Friday",
        "суббота": "Saturday", "воскресенье": "Sunday"}


timetable = {"Thursday": {
    "9А": ["Алгебра", "Алгебра", "Русский язык", "Литература", "Физическая культура", "Биология"],
    "10А": ["Математика", "География", "Биология", "Физика", "Астрономия", "Литература"]
                        }
             }



list_of_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

format_date = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

# огромное колличество клавиатур для удобства

keyboard_main = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_main.add("Изменить данные")

"""
                                        Классы
"""


# ошибка данетки
class YesNoError(Exception):
    pass


# ошибка при неправильном выборе дня недели
class WeekdayError(Exception):
    pass


# ошибка неверного формата времени
class TimeFormatError(Exception):
    pass


# ошибка некоректно введённого времени(например 25:61)
class TimeError(Exception):
    pass


# ошибка выбора отрицательного кол-ва упражниний
class ExerciseFormatError(Exception):
    pass


# ошибка выбора нулевого кол-ва упражниний
class ZeroError(Exception):
    pass


# ошибка возникающая при попытке уменьшения кол-ва упражниний если оно может стать отрицательным или равным 0
class TooLittle(Exception):
    pass


# ошибка возникающая при попытке ввода времени если минуты не кратны 5 (например 14:41)
class DivFiveError(Exception):
    pass


# ошибка при попытке ввода пустого имени
class BlankName(Exception):
    pass


# ошибка регистрации
class RegError(Exception):
    pass


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


"""
                                        Вычислительные функции
"""

def data_day():
    import datetime
    format_date = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

    today = datetime.date.today()
    weekday = format_date[datetime.date.weekday(today)]

    day = today.day
    month = today.month

    if day < 10:
        day = '0{}'.format(day)
    if month < 10:
        month = '0{}'.format(month)

    return ['{}.{}.{}'.format(day, month, today.year), weekday]

url = 'https://docs.google.com/forms/d/e/1FAIpQLSc079VlmVT4mfiayMCO14BuPkt8Tx8ZAyDApQ9qtX03Luoudg/formResponse'


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

    values_list.append(values)

    return values_list


def send_attendance(url, data):
    for d in data:
        try:
            print(d)
            # requests.post(url, data=d)
            # print("Form Submitted.")
            # time.sleep(10)
        except:
            print("Error Occured!")
    print('fins')




def job(n):
    global dictionary_of_users
    dictionary_update()
    date, weekday = data_day()
    for i in dictionary_of_users.keys():
        user = dictionary_of_users[i]
        try:
            subject = timetable[weekday][str(user.num_class) + user.letter_class][n]
        except IndexError:
            pass
        send_attendance(url, get_values(user.num_class, user.letter_class, user.fio, date, subject, user.email))

# обновление словаря юзеров
def dictionary_update():
    global dictionary_of_users
    con = sqlite3.connect("Zommer_db")
    cur = con.cursor()
    result = cur.execute("SELECT id, FIO, email, num_class, letter_class FROM users").fetchall()
    con.close()
    for info in result:
        if info[0] not in dictionary_of_users.keys():
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
        time.sleep(5)


# создание процесса
p1 = Process(target=check_time, args=())

# ну тут понятно
schedule.every().day.at("15:35").do(job, 0)
schedule.every().day.at("15:36").do(job, 1)
schedule.every().day.at("15:34").do(job, 2)
schedule.every().day.at("15:07").do(job, 3)
schedule.every().day.at("15:08").do(job, 4)
schedule.every().day.at("15:09").do(job, 5)
schedule.every().day.at("15:09").do(job, 6)

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
            if dictionary_of_users[tel_id].user_name:
                bot.send_message(message.chat.id, 'Мы встречались, {}'.format(dictionary_of_users[tel_id].fio),
                                 reply_markup=keyboard_main)
    except Exception as start_error:
        logging.error('/start {}'.format(start_error.__class__.__name__))


# все основные сообщения идут сюда
@bot.message_handler(content_types=['text', 'location'])
def send_text(message):
    try:
        tel_id = message.from_user.id
        if dictionary_of_users[tel_id].change:
            if check(message.text):
                fio, email, num_class, letter_class = message.text.split("\n")
                dictionary_of_users[tel_id].update(fio=fio, email=email, num_class=num_class,
                                                   letter_class=letter_class)
                con = sqlite3.connect("Zommer_db")
                cur = con.cursor()
                cur.execute(
                    """INSERT INTO users (id, FIO, email, num_class, letter_class) VALUES ({}, "{}", "{}", {}, "{}")""".format(
                        tel_id, fio, email, num_class, letter_class))
                con.commit()
                con.close()
            else:
                bot.send_message(message.chat.id, 'Некорректное значение')
        elif not dictionary_of_users[tel_id].change:
            if message.text.lower() == 'изменить данные':
                dictionary_of_users[tel_id].change = True
                bot.send_message(message.chat.id, 'Введи ФИО, email, класс и литеру класса\nПример:')
                bot.send_message(message.chat.id, 'Багрянский Константин Дмитриевич\nnanaviju@mail.ru\n10\nА')
    except Exception as main_error:
        logging.error('Unknown error in main {}'.format(main_error.__class__.__name__))




# отлов стикеров
@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    print(message.sticker.file_id)
    bot.send_sticker(message.chat.id, choice(list_of_stickers))


"""
                                        Запуск бота
"""
print(datetime.hour)
# ну это main, тут всё ясно
if __name__ == '__main__':
    p1.start()  # запускаем проверку в отдельном потоке
    #while True:  # цикл что бы при падении серверов телеграма бот жил
    #    try:
    #        bot.polling(none_stop=True)
    #    except Exception as error:
    #        logging.fatal("{} LAST CHANCE".format(error.__class__.__name__))
    #    time.sleep(300)  # а это что бы он не нагружал систему запросами в случае падения серверов телеграма
