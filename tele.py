import os
import time

import telebot
from telebot import types
import win10toast
from mss import mss
from rich import print
from rich.console import Console

import auto
import Internet


console = Console()


def get_keyboard() -> types.ReplyKeyboardMarkup:
    """
    Создает и возвращает клавиатуру для бота.
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton("/shutdown")
    but2 = types.KeyboardButton("/Online")
    but3 = types.KeyboardButton("/hibernation")
    but5 = types.KeyboardButton("/Screen")
    but6 = types.KeyboardButton("/lock🔒")
    but4 = types.KeyboardButton("/cancel")
    markup.add(but1, but2, but3, but5, but6, but4)
    return markup


def execute_and_reply(bot: telebot.TeleBot, message: types.Message, command: str, reply_text: str) -> None:
    """
    Выполняет команду ОС и отправляет ответное сообщение в чат.

    :param bot: Экземпляр бота.
    :param message: Сообщение от пользователя.
    :param command: Команда для выполнения.
    :param reply_text: Текст ответного сообщения.
    """
    os.system(command)
    bot.reply_to(message, reply_text)


def get_shutdown_message(txt: str):
    """
    Возвращает соответствующее сообщение о времени выключения на основе заданной продолжительности.

    :param txt: Продолжительность в секундах.
    :return: Сообщение для пользователя о времени до выключения.
    """
    time_ranges = [
        (18000, "часов 🕑"),
        (7200, "часа 🕑"),
        (3600, "час 🕑"),
        (120, "минуты 🕑"),
        (60, "минуту 🕑"),
        (0, "секунд 🕑")
    ]

    for limit, label in time_ranges:
        if int(txt) > limit:
            if limit == 0:
                return f"Компьютер выключится через {txt} {label}"
            time_value = int(txt) / (3600 if "час" in label else 60)
            return f"Компьютер выключится через {round(time_value)} {label}"

    return None


def main() -> None:
    """
    Главная функция, запускающая бота и обрабатывающая команды пользователя.
    """
    console.clear()

    try:
        with open(os.path.join(os.getenv('APPDATA'), 'TurnOffBot', 'token'), 'r') as ff:
            token = ff.read()
    except (IOError, Exception):
        auto.auto()
        with open(os.path.join(os.getenv('APPDATA'), 'TurnOffBot', 'token'), 'r') as ff:
            token = ff.read()

    turn_on = False

    while not turn_on:
        try:
            Internet.check_internet_connection()
            turn_on = True
        except Exception as ex:
            print(f"Ошибка при проверке интернета: {ex}")
            time.sleep(5)
            console.clear()
            continue

        print('Made by rus152')
        print('')

        bot = telebot.TeleBot(token)
        print('Бот в данный момент ОнЛайн')

        @bot.message_handler(commands=['start'])
        def send_welcome(message):
            bot.send_message(message.chat.id, 'Я НАГИБАТОР3000, только напиши и комп отключится')
            markup = get_keyboard()
            bot.reply_to(message, "Вывод кнопок", parse_mode='html', reply_markup=markup)

        @bot.message_handler(commands=['hibernation'])
        def send(message):
            execute_and_reply(bot, message, 'shutdown /h', "Комп переходит в режим гибернация")

        @bot.message_handler(commands=['lock🔒'])
        def send(message):
            execute_and_reply(bot, message, 'rundll32.exe user32.dll, LockWorkStation', "Блокировка компа 🔒")

        @bot.message_handler(commands=['shutdown'])
        def send(message):
            sec = types.ReplyKeyboardMarkup(resize_keyboard=True)
            but0 = types.KeyboardButton("0")
            but1 = types.KeyboardButton("1800")
            but2 = types.KeyboardButton("3600")
            but3 = types.KeyboardButton("7200")
            but4 = types.KeyboardButton("21600")
            but5 = types.KeyboardButton("Назад")
            sec.add(but0, but1, but2, but3, but4, but5)
            msg: str = bot.send_message(message.chat.id, 'Через сколько отключить компьютер?(В секундах)',
                                        parse_mode='html', reply_markup=sec)
            bot.register_next_step_handler(msg, test)

        def test(message):
            txt = message.text
            print(txt)
            markup = get_keyboard()

            if txt == "Назад":
                bot.reply_to(message, "Возврат", parse_mode='html', reply_markup=markup)
                return

            try:
                shutdown_message = get_shutdown_message(txt)
                if shutdown_message:
                    bot.reply_to(message, shutdown_message, parse_mode='html', reply_markup=markup)
                    os.system(f'shutdown /s /t {txt}')
                else:
                    raise ValueError(f"Недопустимое значение времени: {txt}")

            except Exception as _ex:
                bot.reply_to(message, str(_ex), parse_mode='html', reply_markup=markup)

        @bot.message_handler(commands=['cancel'])
        def send(message):
            execute_and_reply(bot, message, 'shutdown /a', "Отключение отменено")

        @bot.message_handler(commands=['Online'])
        def send(message):
            bot.reply_to(message, "В данный момент комп онлайн", )
            toaster = win10toast.ToastNotifier()
            toaster.show_toast("БОТЯРА 🔔", "Все знают, что комп онлайн", icon_path="icon.ico")

        @bot.message_handler(commands=['Screen'])
        def send(message):
            bot.reply_to(message, "Запрос отправлен", )
            mss().shot(mon=1)
            try:
                mss().shot(mon=2)
            except Exception as _ex:
                print(_ex)
            toaster = win10toast.ToastNotifier()
            toaster.show_toast("БОТЯРА 🔔", "Запрос на скриншот", icon_path="icon.ico")
            bot.send_message(message.chat.id, 'Скриншот сделан')
            bot.send_document(message.chat.id, document=open('monitor-1.png', 'rb'))
            try:
                bot.send_document(message.chat.id, document=open('monitor-2.png', 'rb'))
            except Exception as _ex:
                print(_ex)
            os.remove('monitor-1.png')
            try:
                os.remove('monitor-2.png')
            except Exception as _ex:
                print(_ex)

    try:
        bot.polling(none_stop=True)
    except Exception as ex:
        print(f"Ошибка при работе бота: {ex}")
        time.sleep(5)


if __name__ == '__main__':
    main()
