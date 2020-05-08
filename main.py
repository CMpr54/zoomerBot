# coding: utf8

import logging
import telebot
from telebot import types
import sqlite3
import schedule
import json
import time
import urllib.request
from multiprocessing import Process
from random import choice
from datetime import datetime
from pytz import timezone, utc
# from timezonefinder import TimezoneFinder

"""
                                         Подгтовка к запуску
"""
# # настройка логов
# logging.getLogger('schedule').propagate = False
# logging.basicConfig(level=logging.INFO)
# tf = TimezoneFinder()
#
# # открытие json
# with open('test.json') as f:
#     json_data = json.load(f)
#
# # проверка json
# if not json_data:
#     logging.fatal('Json is empty')

# Токен стесняется, не смотрите
bot = telebot.TeleBot('1054926363:AAFIizR6JDjoe4TJtmmocU0zIbiYtLYPWqA')


# list_of_time_zones = ["-11", "-10", "-9", "-8", "-7", "-6", "-5", "-4", "-3", "-2", "-1", "0", "+1", "+2", "+3", "+4",
#                       "+5", "+6", "+7", "+8", "+9", "+10", "+11", "+12"]
# list_of_phrases = ["Красавчик!", "Молодчина!", "Так держать!", "Огонь!", "Чётко!"]
#
# dict_of_talks = {'greeting': 'разобрались как мне тебя называть',
#                  'exercises': 'определились с твоими упражнениями', 'date_time': 'утвердили твоё расписание',
#                  'training': 'закончили тренировку'}
#
# dict_of_exercises = {"Отжимания": [0, 24], "Приседания": [0, 24], "Подтягивания": [0, 24], "Планка": [0, 24],
#                      "Поднимание ног": [0, 24]}
#
# days = {"понедельник": "Monday", "вторник": "Tuesday", "среда": "Wednesday", "четверг": "Thursday",
#         "пятница": "Friday",
#         "суббота": "Saturday", "воскресенье": "Sunday"}
#
# list_of_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
#
# format_date = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
#
# # огромное колличество клавиатур для удобства
#
# keyboard_ask_timezone = telebot.types.ReplyKeyboardMarkup()
# keyboard_ask_timezone.add(telebot.types.KeyboardButton('Отправить геолокацию', request_location=True))
# keyboard_ask_timezone.add(telebot.types.KeyboardButton('Выбрать самому'))
#
# keyboard_time_zone = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
# keyboard_time_zone.row("+1", "+2", "+3", "+4", "+5", "+6")
# keyboard_time_zone.row("+7", "+8", "+9", "+10", "+11", "+12")
# keyboard_time_zone.row('0', "-1", "-2", "-3", "-4", "-5")
# keyboard_time_zone.row("-6", "-7", "-8", "-9", "-10", "-11")
#
# keyboard_noyes = telebot.types.ReplyKeyboardMarkup()
# keyboard_noyes.add("Да", "Нет")
#
# keyboard_time = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
# keyboard_time.row('4:00', '4:30', '5:00', '5:30', '6:00', '6:30')
# keyboard_time.row('7:00', '7:30', '8:00', '8:30', '9:00', '9:30')
# keyboard_time.row('10:00', '10:30', '11:00', '11:30', '12:00', '12:30')
# keyboard_time.row('13:00', '13:30', '14:00', '14:30', '15:00', '15:30')
# keyboard_time.row('16:00', '16:30', '17:00', '17:30', '18:00', '18:30')
# keyboard_time.row('19:00', '19:30', '20:00', '20:30', '21:00', '21:30')
# keyboard_time.row('22:00', '22:30', '23:00', '23:30', '00:00', '00:30')
# keyboard_time.row('1:00', '1:30', '2:00', '2:30', '3:00', '3:30')
#
# keyboard_days = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
# keyboard_days.add("Понедельник", "Вторник")
# keyboard_days.add("Среда", "Четверг")
# keyboard_days.add("Пятница", "Суббота")
# keyboard_days.add("Воскресенье")
# keyboard_days.add("На этом хватит")
#
# keyboard_first_days = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
# keyboard_first_days.add("Понедельник", "Вторник")
# keyboard_first_days.add("Среда", "Четверг")
# keyboard_first_days.add("Пятница", "Суббота")
# keyboard_first_days.add("Воскресенье")
#
# keyboard_training = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
# keyboard_training.add('Выполнил')
# keyboard_training.add('Увеличить кол-во упражнений')
# keyboard_training.add('Слишком тяжело')
# keyboard_training.add('Очень легко')
# keyboard_training.add('Закончить тренировку')
#
# keyboard_main = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
# keyboard_main.add("Называй меня по другому")
# keyboard_main.add("Сменить упражнения")
# keyboard_main.add("Сменить расписание")
# keyboard_main.add("Показать расписание")
# keyboard_main.add("Хочу заниматься")
# keyboard_main.add("Изменить часовой пояс")
#
# keyboard_answer = types.InlineKeyboardMarkup()
# key_yes = types.InlineKeyboardButton(text='Готов заниматься', callback_data='yes')
# keyboard_answer.add(key_yes)
# key_no = types.InlineKeyboardButton(text='Нет возможности', callback_data='no')
# keyboard_answer.add(key_no)
#
# """
#                                         Классы
# """
#
#
# # ошибка данетки
# class YesNoError(Exception):
#     pass
#
#
# # ошибка при неправильном выборе дня недели
# class WeekdayError(Exception):
#     pass
#
#
# # ошибка неверного формата времени
# class TimeFormatError(Exception):
#     pass
#
#
# # ошибка некоректно введённого времени(например 25:61)
# class TimeError(Exception):
#     pass
#
#
# # ошибка выбора отрицательного кол-ва упражниний
# class ExerciseFormatError(Exception):
#     pass
#
#
# # ошибка выбора нулевого кол-ва упражниний
# class ZeroError(Exception):
#     pass
#
#
# # ошибка возникающая при попытке уменьшения кол-ва упражниний если оно может стать отрицательным или равным 0
# class TooLittle(Exception):
#     pass
#
#
# # ошибка возникающая при попытке ввода времени если минуты не кратны 5 (например 14:41)
# class DivFiveError(Exception):
#     pass
#
#
# # ошибка при попытке ввода пустого имени
# class BlankName(Exception):
#     pass
#
#
# # ошибка регистрации
# class RegError(Exception):
#     pass
#
#
# # класс для хранения информации о юзере
# class User:
#     def __init__(self, user_name, training_type, date_and_time, time_zone):
#         self.user_name = user_name
#         self.zoom_login = ''
#         self.zoom_password = ''
#         self.gh_login = ''
#         self.gh_password = ''
#         if date_and_time:
#             self.date_and_time = eval(date_and_time)
#         else:
#             self.date_and_time = dict()
#         self.change_data = dict()
#         self.timezone = time_zone
#         self.pref_timezone = time_zone
#         self.day = ""
#         self.conversation = ""
#         self.conversation_power = 0
#         self.first = False
#         self.num = []
#         self.training = []
#         self.payed = ""
#
#
# """
#                                         Вычислительные функции
# """
#
#
# # функция геокодера (получает координаты и возращает часовой пояс)
# def get_offset(*, lat, lng):
#     try:
#         today = datetime.now()
#         tz_target = timezone(tf.certain_timezone_at(lng=lng, lat=lat))
#         # ATTENTION: tz_target could be None! handle error case
#         today_target = tz_target.localize(today)
#         today_utc = utc.localize(today)
#         return (today_utc - today_target).total_seconds() / 60
#     except Exception as geo_error:
#         logging.error("geo error {}".format(geo_error.__class__.__name__))
#         return 3
#
#
# # функция возращающая время в понятном программе формате
# def time_format(hour_minute):
#     hour_minute = hour_minute.split(":")
#     if 0 <= int(hour_minute[0]) < 24 and 0 <= int(hour_minute[1]) <= 59:
#         hour_minute = [str(i) for i in hour_minute]
#         if int(hour_minute[1]) % 5 != 0:
#             raise DivFiveError
#         if int(hour_minute[0]) < 10:
#             hour_minute[0] = "0" + str(hour_minute[0])
#         if int(hour_minute[1]) < 10:
#             hour_minute[1] = "0" + str(hour_minute[1])
#         return hour_minute
#     else:
#         raise TimeError
#
#
# # функция проверяющая выбранные упражниния и запиывающая изменения в БД
# def training_update(tel_id):
#     training = dictionary_of_users[tel_id].change_training
#     try:
#         if training.keys():
#             dictionary_of_users[tel_id].training_type = training
#             dictionary_of_users[tel_id].change_training = dict()
#             con = sqlite3.connect("data")
#             cur = con.cursor()
#             cur.execute(
#                 """UPDATE table_name SET training_type = "{}" WHERE user_id = {}""".format(training, tel_id))
#             con.commit()
#             con.close()
#             return True
#         else:
#             return False
#     except Exception as training_update_error:
#         logging.error('training_update_error {}'.format(training_update_error.__class__.__name__))
#         return False
#
#
# # отлов исключений связанных с часовыми поясами в случае смещения дня недели
# def day_exception(hour, day):
#     if int(hour) < 0:
#         if day != 'Monday':
#             day = list_of_days[day.index(day) - 1]
#         else:
#             day = 'Sunday'
#         hour = str(24 + int(hour))
#     elif int(hour) > 23:
#         if day != 'Sunday':
#             day = list_of_days[day.index(day) + 1]
#         else:
#             day = 'Monday'
#         hour = str(int(hour) - 24)
#     return hour, day
#
#
# # обновление часового пояса в БД и json
# def timezone_update(tel_id):
#     user = dictionary_of_users[tel_id]
#     global json_data
#     user_data = user.date_and_time
#     logging.info('timezone refreshing')
#     if user.pref_timezone != user.timezone:
#         try:
#             for data in user_data.keys():
#                 day, hour, minute = days[data], str(int(user_data[data][0]) - user.pref_timezone), user_data[data][1]
#                 hour, day = day_exception(hour, day)
#                 if hour in json_data[day]["Time"]["Hours"]:
#                     if minute in json_data[day]["Time"]["Hours"][hour]["minutes"]:
#                         if tel_id in json_data[day]["Time"]["Hours"][hour]["minutes"][minute]:
#                             json_data[day]["Time"]["Hours"][hour]["minutes"][minute].remove(tel_id)
#                             if not json_data[day]["Time"]["Hours"][hour]["minutes"][minute]:
#                                 del json_data[day]["Time"]["Hours"][hour]["minutes"][minute]
#             logging.info('Delete completed')
#
#             for data in user_data.keys():
#                 day, hour, minute = days[data], str(int(user_data[data][0]) - user.timezone), user_data[data][1]
#                 hour, day = day_exception(hour, day)
#                 if hour in json_data[day]["Time"]["Hours"]:
#                     if minute in json_data[day]["Time"]["Hours"][hour]["minutes"]:
#                         json_data[day]["Time"]["Hours"][hour]["minutes"][minute].append(tel_id)
#                     else:
#                         json_data[day]["Time"]["Hours"][hour]["minutes"][minute] = [tel_id]
#                 else:
#                     json_data[day]["Time"]["Hours"][hour] = {'minutes': {minute: [tel_id]}}
#             logging.info('Refreshing timezone json completed')
#             file = open("test.json", 'w')
#             a = json.dumps(json_data, ensure_ascii=False, sort_keys=True, indent=4)
#             file.write(a)
#             file.close()
#             dictionary_of_users[tel_id].pref_timezone = user.timezone
#             logging.info('Refresh timezone completed')
#         except Exception as time_zone_error:
#             logging.fatal('timezone_update {}'.format(time_zone_error.__class__.__name__))
#
#
# # обновление расписания занятий в БД и json
# def timetable_update(tel_id):
#     global json_data
#     users_data = dictionary_of_users[tel_id].change_data
#     prev_data = dictionary_of_users[tel_id].date_and_time
#     logging.info('timetable refreshing')
#     try:
#         for data in prev_data.keys():
#             day, hour, minute = days[data], str(int(prev_data[data][0]) - dictionary_of_users[tel_id].timezone), \
#                                 prev_data[data][1]
#             hour, day = day_exception(hour, day)
#             if hour in json_data[day]["Time"]["Hours"]:
#                 if minute in json_data[day]["Time"]["Hours"][hour]["minutes"]:
#                     if tel_id in json_data[day]["Time"]["Hours"][hour]["minutes"][minute]:
#                         json_data[day]["Time"]["Hours"][hour]["minutes"][minute].remove(tel_id)
#                         if not json_data[day]["Time"]["Hours"][hour]["minutes"][minute]:
#                             del json_data[day]["Time"]["Hours"][hour]["minutes"][minute]
#         logging.info('Delete completed')
#
#         for data in users_data.keys():
#             day, hour, minute = days[data], str(int(users_data[data][0]) - dictionary_of_users[tel_id].timezone), \
#                                 users_data[data][1]
#             hour, day = day_exception(hour, day)
#
#             if hour in json_data[day]["Time"]["Hours"]:
#                 if minute in json_data[day]["Time"]["Hours"][hour]["minutes"]:
#                     json_data[day]["Time"]["Hours"][hour]["minutes"][minute].append(tel_id)
#                 else:
#                     json_data[day]["Time"]["Hours"][hour]["minutes"][minute] = [tel_id]
#             else:
#                 json_data[day]["Time"]["Hours"][hour] = {'minutes': {minute: [tel_id]}}
#
#         logging.info("Refresh timetable json completed")
#         file = open("test.json", 'w')
#         a = json.dumps(json_data, ensure_ascii=False, sort_keys=True, indent=4)
#         file.write(a)
#         file.close()
#         dictionary_of_users[tel_id].date_and_time = users_data
#         con = sqlite3.connect("data")
#         cur = con.cursor()
#         cur.execute(
#             """UPDATE table_name SET date_and_time = "{}" WHERE user_id = {}""".format(
#                 str(users_data), tel_id))
#         con.commit()
#         con.close()
#         logging.info("Refresh timetable completed")
#     except Exception as timetable_update_error:
#         logging.fatal('timetable_update {}'.format(timetable_update_error.__class__.__name__))
#
#
# # обновление словаря юзеров
# def dictionary_update():
#     global dictionary_of_users
#     con = sqlite3.connect("data")
#     cur = con.cursor()
#     result = cur.execute("SELECT * FROM table_name").fetchall()
#     con.close()
#     for info in result:
#         if info[0] not in dictionary_of_users.keys():
#             dictionary_of_users[info[0]] = User(*info[1:])
#
#
# # создание и заполнение словаря пользователей
# dictionary_of_users = {}
# dictionary_update()
#
# """
#                                         Диалоговые функции
# """
#
#
# # диалог по упражнениям
# def exercise_talking(message, user):
#     try:
#         if user.conversation_power == 0:
#             if message.text.lower() == "да":
#                 user.conversation_power = 1
#             elif message.text.lower() == "нет":
#                 user.conversation_power = 2
#                 bot.send_message(message.chat.id, 'Ты хочешь приседать?', reply_markup=keyboard_noyes)
#             else:
#                 raise YesNoError
#
#         elif user.conversation_power == 1:
#             if int(message.text) == 0:
#                 raise ZeroError
#             if int(message.text) < 0:
#                 raise ExerciseFormatError
#             user.change_training["Отжимания"] = int(message.text)
#             user.conversation_power = 2
#             bot.send_message(message.chat.id, 'Ты хочешь приседать?', reply_markup=keyboard_noyes)
#
#         elif user.conversation_power == 2:
#             if message.text.lower() == "да":
#                 user.conversation_power = 3
#             elif message.text.lower() == "нет":
#                 user.conversation_power = 4
#                 bot.send_message(message.chat.id, 'Ты хочешь подтягиваться?', reply_markup=keyboard_noyes)
#             else:
#                 raise YesNoError
#
#         elif user.conversation_power == 3:
#             if int(message.text) == 0:
#                 raise ZeroError
#             if int(message.text) < 0:
#                 raise ExerciseFormatError
#             user.change_training["Приседания"] = int(message.text)
#             user.conversation_power = 4
#             bot.send_message(message.chat.id, 'Ты хочешь подтягиваться?', reply_markup=keyboard_noyes)
#
#         elif user.conversation_power == 4:
#             if message.text.lower() == "да":
#                 user.conversation_power = 5
#             elif message.text.lower() == "нет":
#                 user.conversation_power = 6
#                 bot.send_message(message.chat.id, 'Ты хочешь делать планку?', reply_markup=keyboard_noyes)
#             else:
#                 raise YesNoError
#
#         elif user.conversation_power == 5:
#             if int(message.text) == 0:
#                 raise ZeroError
#             if int(message.text) < 0:
#                 raise ExerciseFormatError
#             user.change_training["Подтягивания"] = int(message.text)
#             user.conversation_power = 6
#             bot.send_message(message.chat.id, 'Ты хочешь делать планку?', reply_markup=keyboard_noyes)
#
#         elif user.conversation_power == 6:
#             if message.text.lower() == "да":
#                 user.conversation_power = 7
#             elif message.text.lower() == "нет":
#                 user.conversation_power = 8
#                 bot.send_message(message.chat.id, 'Ты хочешь поднимать ноги?', reply_markup=keyboard_noyes)
#             else:
#                 raise YesNoError
#
#         elif user.conversation_power == 7:
#             if int(message.text) == 0:
#                 raise ZeroError
#             if int(message.text) < 0:
#                 raise ExerciseFormatError
#             user.change_training["Планка"] = int(message.text)
#             user.conversation_power = 8
#             bot.send_message(message.chat.id, 'Ты хочешь поднимать ноги?', reply_markup=keyboard_noyes)
#
#         elif user.conversation_power == 8:
#             if message.text.lower() == "да":
#                 user.conversation_power = 9
#             elif message.text.lower() == "нет":
#                 if training_update(message.from_user.id):
#                     if user.first:
#                         user.conversation_power = 0
#                         user.conversation = "date_time"
#                         user.change_data = dict()
#                         bot.send_message(message.chat.id, 'В какой день тебе удобно заниматься?',
#                                          reply_markup=keyboard_first_days)
#                     else:
#                         bot.send_message(message.chat.id, 'Я запомнил', reply_markup=keyboard_main)
#                         user.conversation_power = 0
#                         user.conversation = ""
#                 else:
#                     bot.send_message(message.chat.id, 'Выбери хотя бы одно упражнение')
#                     bot.send_message(message.chat.id, 'Ты хочешь отжиматься?', reply_markup=keyboard_noyes)
#                     user.conversation = 'exercises'
#                     user.conversation_power = 0
#
#             else:
#                 raise YesNoError
#
#         elif user.conversation_power == 9:
#             if int(message.text) == 0:
#                 raise ZeroError
#             if int(message.text) < 0:
#                 raise ExerciseFormatError
#             user.change_training["Поднимание ног"] = int(message.text)
#             user.conversation_power = 0
#
#             if training_update(message.from_user.id):
#                 if user.first:
#                     user.conversation_power = 0
#                     user.conversation = "date_time"
#                     user.change_data = dict()
#                     bot.send_message(message.chat.id, 'Когда хочешь заниматься?',
#                                      reply_markup=keyboard_first_days)
#                 else:
#                     bot.send_message(message.chat.id, 'Я запомнил', reply_markup=keyboard_main)
#                     user.conversation_power = 0
#                     user.conversation = ""
#             else:
#                 bot.send_message(message.chat.id, 'Серьёзно? Выбери хотя бы одно упражнение')
#                 user.conversation = 'exercises'
#                 user.conversation_power = 0
#     except ValueError:
#         bot.send_message(message.chat.id, 'Отвечай внятно')
#
#
# # диалог тренировки
# def exercise(tel_id):
#     user = dictionary_of_users[tel_id]
#     if user.num:
#         if 'Отжимания' in user.num:
#             bot.send_message(tel_id, 'Отожмись {} раз'.format(user.training_type['Отжимания']),
#                              reply_markup=keyboard_training)
#             user.training = 'Отжимания'
#         elif 'Приседания' in user.num:
#             bot.send_message(tel_id, 'Присядь {} раз'.format(user.training_type['Приседания']),
#                              reply_markup=keyboard_training)
#             user.training = 'Приседания'
#         elif 'Подтягивания' in user.num:
#             bot.send_message(tel_id, 'Подтянись {} раз'.format(user.training_type['Подтягивания']),
#                              reply_markup=keyboard_training)
#             user.training = 'Подтягивания'
#         elif 'Планка' in user.num:
#             bot.send_message(tel_id, 'Держи планку {} секунд'.format(user.training_type['Планка']),
#                              reply_markup=keyboard_training)
#             user.training = 'Планка'
#         elif 'Поднимание ног' in user.num:
#             bot.send_message(tel_id, 'Подними ноги {} раз'.format(user.training_type['Поднимание ног']),
#                              reply_markup=keyboard_training)
#             user.training = 'Поднимание ног'
#
#         user.num.remove(user.training)
#     else:
#         con = sqlite3.connect("data")
#         cur = con.cursor()
#         cur.execute(
#             """UPDATE table_name SET training_type = "{}" WHERE user_id = {}""".format(user.training_type, tel_id))
#         con.commit()
#         con.close()
#         logging.info('{} completed training'.format(user.user_name))
#         bot.send_message(tel_id, 'Отличная была тренировка', reply_markup=keyboard_main)
#         user.conversation = ''
#
#
# """
#                                         Функции рассылки
# """
#
#
# # рассылка напоминаний о тренировках
# def mailing(users):
#     for tel_id in users:
#         bot.send_message(tel_id, 'Пора заниматься', reply_markup=keyboard_answer)
#
#
# # проверка времени для рассылки
# def act():
#     if datetime.now().minute % 5 == 0:
#         hour = str(datetime.now().hour % 24)
#         minute = str(datetime.now().minute)
#         day = format_date[datetime.now().weekday()]
#         if int(hour) < 10:
#             hour = "0" + hour
#         if int(minute) < 10:
#             minute = "0" + minute
#         with open('test.json') as file:
#             data = json.load(file)
#         if hour in data[day]["Time"]["Hours"]:
#             if minute in data[day]["Time"]["Hours"][hour]["minutes"]:
#                 mailing(data[day]["Time"]["Hours"][hour]["minutes"][minute])
#
#
# # процесс проверки времени
# def check_time():
#     while True:
#         schedule.run_pending()
#         # ваш код проверки времени и отправки сообщений по таймеру
#         # пауза между проверками, чтобы не загружать процессор
#         time.sleep(60)
#
#
# # создание процесса
# p1 = Process(target=check_time, args=())
#
# # ну тут понятно
# schedule.every().minute.do(act)
#
# """
#                                         Хэндлеры
# """
#
#
# # самое первое и самое волнительное сообщение
# @bot.message_handler(commands=['start'])
# def start_message(message):
#     try:
#         tel_id = message.from_user.id
#         if tel_id not in dictionary_of_users.keys():
#             con = sqlite3.connect("data")
#             cur = con.cursor()
#             cur.execute(
#                 """INSERT INTO table_name (user_id) VALUES ({})""".format(tel_id))
#             con.commit()
#             con.close()
#             bot.send_message(message.chat.id, 'Как тебя звать?')
#             dictionary_update()
#             dictionary_of_users[tel_id].first = True
#             dictionary_of_users[tel_id].conversation = "greeting"
#             dictionary_of_users[tel_id].conversation_power = 1
#             logging.info('New user')
#         else:
#             if dictionary_of_users[tel_id].user_name:
#                 bot.send_message(message.chat.id, 'Мы встречались, {}'.format(dictionary_of_users[tel_id].user_name),
#                                  reply_markup=keyboard_main)
#     except Exception as start_error:
#         logging.error('/start {}'.format(start_error.__class__.__name__))
#
#
# # все основные сообщения идут сюда
# @bot.message_handler(content_types=['text', 'location'])
# def send_text(message):
#     tel_id = message.from_user.id
#     try:
#         if tel_id not in dictionary_of_users.keys():
#             raise RegError
#         user = dictionary_of_users[tel_id]
#         if user.conversation == "greeting":
#             if user.conversation_power == 1:
#                 if not message.text:
#                     raise BlankName
#                 if user.first:
#                     bot.send_message(tel_id,
#                                      'Я буду звать тебя {}'.format(message.text))
#                     user.user_name = message.text
#                     user.conversation = 'time_zone'
#                     user.conversation_power = 0
#                     bot.send_message(tel_id, 'Какой у тебя часовой пояс?', reply_markup=keyboard_ask_timezone)
#                 else:
#                     bot.send_message(tel_id,
#                                      'Я буду звать тебя {}'.format(message.text), reply_markup=keyboard_main)
#                     user.user_name = message.text
#                     user.conversation_power = 0
#                     user.conversation = ""
#                 con = sqlite3.connect("data")
#                 cur = con.cursor()
#                 cur.execute(
#                     """UPDATE table_name SET user_name = "{}" WHERE user_id = {}""".format(message.text, tel_id))
#                 con.commit()
#                 con.close()
#         elif user.conversation == "time_zone":
#             try:
#                 if user.conversation_power == 0:
#                     if message.location:
#                         loc = {'lat': message.location.latitude, 'lng': message.location.longitude}
#                         hour_offset = int(get_offset(**loc) // 60)
#                         if hour_offset <= 0:
#                             bot.send_message(tel_id, 'Ты живёшь в часовом поясе UTC {}?'.format(hour_offset),
#                                              reply_markup=keyboard_noyes)
#                         else:
#                             bot.send_message(tel_id, 'Ты живёшь в часовом поясе UTC +{}?'.format(hour_offset),
#                                              reply_markup=keyboard_noyes)
#                         user.conversation_power = 1
#                         user.timezone = hour_offset
#                     elif message.text.lower() == 'выбрать самому':
#                         bot.send_message(tel_id, 'Ну тогда выбирай', reply_markup=keyboard_time_zone)
#                         user.conversation_power = 2
#                 elif user.conversation_power == 1:
#                     if message.text.lower() == 'нет':
#                         bot.send_message(tel_id, 'Ну тогда выбирай', reply_markup=keyboard_time_zone)
#                         logging.warning('Wrong timezone')
#                         user.conversation_power = 2
#                     elif message.text.lower() == 'да':
#                         if user.first:
#                             user.pref_timezone = user.timezone
#                             user.conversation = 'exercises'
#                             user.conversation_power = 0
#                             bot.send_message(tel_id, 'Отлично, а сейчас тебя ждёт допрос')
#                             bot.send_message(tel_id, 'Ты хочешь отжиматься?', reply_markup=keyboard_noyes)
#                         else:
#                             timezone_update(tel_id)
#                             bot.send_message(tel_id, 'Я запомнил', reply_markup=keyboard_main)
#                             user.conversation = ''
#                             user.conversation_power = 0
#                         con = sqlite3.connect("data")
#                         cur = con.cursor()
#                         cur.execute(
#                             """UPDATE table_name SET time_zone = {} WHERE user_id = {}""".format(user.timezone, tel_id))
#                         con.commit()
#                         con.close()
#
#                 elif user.conversation_power == 2:
#                     if message.text in list_of_time_zones:
#                         user.timezone = int(message.text)
#                         if user.first:
#                             user.pref_timezone = user.timezone
#                             user.conversation = 'exercises'
#                             user.conversation_power = 0
#                             bot.send_message(tel_id, 'Отлично, а сейчас тебя ждёт допрос')
#                             bot.send_message(tel_id, 'Ты хочешь отжиматься?', reply_markup=keyboard_noyes)
#                         else:
#                             timezone_update(tel_id)
#                             bot.send_message(tel_id, 'Я запомнил', reply_markup=keyboard_main)
#                             user.conversation = ''
#                             user.conversation_power = 0
#                         con = sqlite3.connect("data")
#                         cur = con.cursor()
#                         cur.execute(
#                             """UPDATE table_name SET time_zone = {} WHERE user_id = {}""".format(user.timezone, tel_id))
#                         con.commit()
#                         con.close()
#
#                     else:
#                         bot.send_message(tel_id, 'Пиши корректно')
#             except ValueError:
#                 bot.send_message(tel_id, 'Выбери из вариантов')
#
#         elif user.conversation == "exercises":
#             try:
#                 exercise_talking(message, user)
#             except ZeroError:
#                 bot.send_message(tel_id, 'Слабак?')
#             except ExerciseFormatError:
#                 bot.send_message(tel_id, 'Ты думаешь Рэймонд это не предвидел?')
#             except ValueError:
#                 bot.send_message(tel_id, 'Напиши просто число')
#             except YesNoError:
#                 bot.send_message(tel_id, 'Отвечай да или нет')
#             except Exception as exercise_error:
#                 logging.error('Unknown error in exercises choosing {}'.format(exercise_error.__class__.__name__))
#                 bot.send_message(tel_id, 'Отвечай внятно')
#
#         elif user.conversation == 'date_time':
#             try:
#                 if user.conversation_power == 0:
#                     if message.text.lower() in days.keys():
#                         bot.send_message(tel_id,
#                                          'Когда можешь заниматься в {}, скажи во сколько если не можешь выбрать'.format(
#                                              message.text.lower()), reply_markup=keyboard_time)
#                         user.day = message.text.lower()
#                         user.conversation_power = 1
#                     elif message.text.lower() == 'на этом хватит':
#                         if user.change_data:
#                             user.conversation = ""
#                             timetable_update(tel_id)
#                             user.first = False
#                             user.conversation_power = 0
#                             bot.send_message(tel_id, "Ну хватит так хватит", reply_markup=keyboard_main)
#                         else:
#                             bot.send_message(tel_id, "Ты вообще собираешься заниматься?",
#                                              reply_markup=keyboard_days)
#                     else:
#                         raise WeekdayError
#                 elif user.conversation_power == 1:
#                     user.change_data[user.day] = time_format(message.text)
#                     bot.send_message(tel_id, 'Когда ты ещё хочешь заниматься?', reply_markup=keyboard_days)
#                     user.conversation_power = 0
#             except DivFiveError:
#                 bot.send_message(tel_id, 'Число минут должно быть кратно 5')
#             except WeekdayError:
#                 bot.send_message(tel_id, 'Просто напиши день недели')
#             except TimeFormatError:
#                 bot.send_message(tel_id, 'Пиши в формате HH:MM, например 18:00')
#             except TimeError:
#                 bot.send_message(tel_id, 'Ты шутки шутить вздумал?')
#             except Exception as time_error:
#                 logging.error('Unknown date and time error {}'.format(time_error.__class__.__name__))
#         elif user.conversation == 'training':
#             if message.text.lower() == 'выполнил':
#                 bot.send_message(tel_id, choice(list_of_phrases))
#                 exercise(tel_id)
#             elif message.text.lower() == 'увеличить кол-во упражнений':
#                 if user.training == "Отжимания":
#                     user.training_type[user.training] += 2
#                 elif user.training == "Приседания":
#                     user.training_type[user.training] += 2
#                 elif user.training == "Подтягивания":
#                     user.training_type[user.training] += 1
#                 elif user.training == "Планка":
#                     user.training_type[user.training] += 10
#                 elif user.training == "Поднимание ног":
#                     user.training_type[user.training] += 4
#                 bot.send_message(tel_id, 'Я буду давать тебе большую нагрузку')
#                 exercise(tel_id)
#             elif message.text.lower() == 'слишком тяжело':
#                 try:
#                     if user.training == "Отжимания":
#                         if user.training_type[user.training] > 2:
#                             user.training_type[user.training] -= 2
#                         else:
#                             raise TooLittle
#                     elif user.training == "Приседания":
#                         if user.training_type[user.training] > 2:
#                             user.training_type[user.training] -= 2
#                         else:
#                             raise TooLittle
#                     elif user.training == "Подтягивания":
#                         if user.training_type[user.training] > 1:
#                             user.training_type[user.training] -= 1
#                         else:
#                             raise TooLittle
#                     elif user.training == "Планка":
#                         if user.training_type[user.training] > 10:
#                             user.training_type[user.training] -= 10
#                         else:
#                             raise TooLittle
#                     elif user.training == "Поднимание ног":
#                         if user.training_type[user.training] > 2:
#                             user.training_type[user.training] -= 2
#                         else:
#                             raise TooLittle
#                     bot.send_message(tel_id, 'Я запомнил, что тебе нужно давать меньшую нагрузку')
#                     exercise(tel_id)
#                 except TooLittle:
#                     bot.send_message(tel_id, 'Меньше уже некуда, {}'.format(user.user_name))
#                     exercise(tel_id)
#
#             elif message.text.lower() == 'очень легко':
#                 if user.training == "Отжимания":
#                     user.training_type[user.training] += 4
#                 elif user.training == "Приседания":
#                     user.training_type[user.training] += 4
#                 elif user.training == "Подтягивания":
#                     user.training_type[user.training] += 2
#                 elif user.training == "Планка":
#                     user.training_type[user.training] += 20
#                 elif user.training == "Поднимание ног":
#                     user.training_type[user.training] += 8
#                 bot.send_message(tel_id, 'Я буду давать тебе большую нагрузку')
#                 exercise(tel_id)
#             elif message.text.lower() == 'закончить тренировку':
#                 bot.send_message(tel_id, 'Грустно конечно, но что поделать')
#                 user.num = []
#                 exercise(tel_id)
#             else:
#                 bot.send_message(tel_id, 'Я тебя не понял, повтори')
#         else:
#             if message.text.lower() == 'называй меня по другому':
#                 bot.send_message(tel_id, 'Как тебя называть?', reply_markup=types.ReplyKeyboardRemove())
#                 dictionary_of_users[tel_id].conversation = "greeting"
#                 dictionary_of_users[tel_id].conversation_power = 1
#             elif message.text.lower() == 'сменить упражнения':
#                 user.change_training = dict()
#                 bot.send_message(tel_id, 'Ты хочешь отжиматься?', reply_markup=keyboard_noyes)
#                 user.conversation = 'exercises'
#                 user.conversation_power = 0
#             elif message.text.lower() == 'сменить расписание':
#                 user.conversation_power = 0
#                 user.change_data = dict()
#                 user.conversation = "date_time"
#                 bot.send_message(tel_id, 'В какой день можешь заниматься?', reply_markup=keyboard_first_days)
#             elif message.text.lower() == 'показать расписание':
#                 bot.send_message(tel_id, "{}".format('\n'.join(
#                     ["{}\t{}".format(j.capitalize(), ':'.join(user.date_and_time[j])) for j in
#                      user.date_and_time.keys()])),
#                                  reply_markup=keyboard_main)
#             elif message.text.lower() == 'хочу заниматься':
#                 dictionary_of_users[tel_id].conversation = 'training'
#                 dictionary_of_users[tel_id].num = [i for i in dictionary_of_users[tel_id].training_type.keys()]
#                 dictionary_of_users[tel_id].conversation_power = 0
#                 exercise(tel_id)
#             elif message.text.lower() == 'изменить часовой пояс':
#                 user.conversation = 'time_zone'
#                 user.conversation_power = 0
#                 bot.send_message(tel_id, 'Какой у тебя часовой пояс?', reply_markup=keyboard_ask_timezone)
#     except RegError:
#         bot.send_message(tel_id, 'Я тебя не знаю, нажми /start')
#     except BlankName:
#         bot.send_message(tel_id, 'Ты шутки шутишь? Как тебя звать?')
#     except Exception as main_error:
#         logging.error('Unknown error in main {}'.format(main_error.__class__.__name__))
#
#
# # проверка готовности юзера к тренировке
# @bot.callback_query_handler(func=lambda call: True)
# def callback_worker(call):
#     tel_id = call.message.chat.id
#     try:
#         if dictionary_of_users[tel_id].conversation == '':
#             if call.data == "yes":
#                 dictionary_of_users[tel_id].conversation = 'training'
#                 dictionary_of_users[tel_id].num = [i for i in dictionary_of_users[tel_id].training_type.keys()]
#                 dictionary_of_users[tel_id].conversation_power = 0
#                 exercise(tel_id)
#             elif call.data == "no":
#                 bot.delete_message(call.message.chat.id, call.message.message_id)
#         else:
#             bot.send_message(tel_id,
#                              'Подожди, мы не {}'.format(dict_of_talks[dictionary_of_users[tel_id].conversation]))
#     except KeyError:
#         bot.send_message(tel_id, 'Я тебя не знаю, нажми /start')
#     except Exception as callback_error:
#         logging.error('callback error {}'.format(callback_error.__class__.__name__))
#

# отлов стикеров
@bot.message_handler(content_types=['text'])
def sticker_id(message):
    url = "https://zoom.us/captcha-image?type=1"
    img = urllib.request.urlopen(url).read()
    bot.send_photo(message.chat.id, img)

"""
                                        Запуск бота
"""

# ну это main, тут всё ясно
if __name__ == '__main__':
    # p1.start()  # запускаем проверку в отдельном потоке
    while True:  # цикл что бы при падении серверов телеграма бот жил
        try:
            bot.polling(none_stop=True)
        except Exception as error:
            logging.fatal("{} LAST CHANCE".format(error.__class__.__name__))
        time.sleep(300)  # а это что бы он не нагружал систему запросами в случае падения серверов телеграма