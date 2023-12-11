import logging
import os
import time

import telebot
from telebot import types
import win10toast
from mss import mss
from rich.console import Console

import auto
import Internet


logging.basicConfig(filename='tele.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

console = Console()


def get_keyboard() -> types.ReplyKeyboardMarkup:
    """
    Creates and returns a keyboard for the bot.
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton("/shutdown")
    but2 = types.KeyboardButton("/Online")
    but3 = types.KeyboardButton("/hibernation")
    but5 = types.KeyboardButton("/Screen")
    but6 = types.KeyboardButton("/lock🔒")
    but4 = types.KeyboardButton("/cancel")
    markup.add(but1, but2, but3, but5, but6, but4)
    logging.debug('Keyboard created for the bot')
    return markup


def execute_and_reply(bot: telebot.TeleBot, message: types.Message, command: str, reply_text: str) -> None:
    """
    Executes the OS command and sends a reply message to the chat.

    :param bot: An instance of the bot.
    :param message: A message from the user.
    :param command: The command to execute.
    :param reply_text: The text of the reply message.
    """
    os.system(command)
    bot.reply_to(message, reply_text)
    logging.info(f'Command executed: {command} and replied with {reply_text}')


def get_shutdown_message(txt: str):
    """
    Returns the corresponding shutdown time message based on the specified duration.

    :param txt: Duration in seconds.
    :return: A message to the user about the time before shutdown.
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

    logging.debug(f'Shutdown message generated for duration: {txt}')
    return None


def main() -> None:
    """
    The main function that runs the bot and processes the user's commands.
    """
    logging.info('Main function started')

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
            logging.info("Internet connection successfully established")
        except Exception as ex:
            logging.error(f"Error checking internet connection: {ex}")
            time.sleep(5)

        bot = telebot.TeleBot(token)
        logging.info('Bot is now online')

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
            bot.reply_to(message, "Запрос отправлен")
            mss().shot(mon=1)
            try:
                mss().shot(mon=2)
            except Exception as _ex:
                logging.error(f"Error when creating a screenshot for the second screen: {_ex}")

            toaster = win10toast.ToastNotifier()
            toaster.show_toast("БОТЯРА 🔔", "Запрос на скриншот", icon_path="icon.ico")
            bot.send_message(message.chat.id, 'Скриншот сделан')

            try:
                with open('monitor-1.png', 'rb') as file:
                    bot.send_document(message.chat.id, document=file)
                os.remove('monitor-1.png')
            except Exception as _ex:
                logging.error(f"Error when sending or deleting a screenshot of monitor-1.png: {_ex}")

            try:
                with open('monitor-2.png', 'rb') as file:
                    bot.send_document(message.chat.id, document=file)
                os.remove('monitor-2.png')
            except Exception as _ex:
                logging.error(f"Error when sending or deleting a screenshot of monitor-2.png: {_ex}")

    try:
        bot.polling(none_stop=True)
        logging.info('Bot polling started')
    except Exception as ex:
        logging.error(f'Error during bot operation: {ex}')
        time.sleep(5)


if __name__ == '__main__':
    main()
