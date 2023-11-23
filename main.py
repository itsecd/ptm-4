import telebot
import logging
from telebot import types
from charts import line, hist

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
bot = telebot.TeleBot('А вот токен не дам')


@bot.message_handler(commands=['start'])
def start(message) -> None:
    """
    функция обрабатывает команду /start и нажатие на кнопку "Поздороваться"
    :param message: сообщение
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Поздороваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "Я тебя уже заждался", reply_markup=markup)
    logger.info("User %s started the bot", message.from_user.id)


@bot.message_handler(commands=['whou'])
def who(message) -> None:
    """
    функция обрабатывает команду /who, отвечая пользователю
    :param message: сообщение
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.from_user.id, "Я бот", reply_markup=markup)
    logger.info("User %s asked who the bot is", message.from_user.id)


@bot.message_handler(content_types=['text'])
def get_text_messages(message) -> None:
    """
    Функция обрабатывает нажатие различных кнопок, привязывая к ним определенные действия
    :param message: сообщение
    """
    if message.text == 'Поздороваться':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
        btn1 = types.KeyboardButton('Кто создатель бота?')
        btn2 = types.KeyboardButton('Что ты можешь?')
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, '❓ Задайте интересующий вас вопрос', reply_markup=markup)
    elif message.text == 'Кто создатель бота?':
        bot.send_message(message.from_user.id, 'Создатель бота - это лучший человек в мире, хакер, взломавший одну'
                                               ' розетку, представляю вам:', parse_mode='Markdown')
        bot.send_photo(chat_id=message.from_user.id, photo=open('GFvB3q5Q0P0.jpg', 'rb'))
        logger.info("User %s asked who the bot creator is", message.from_user.id)
    elif message.text == 'Что ты можешь?':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_line = types.KeyboardButton('Линейный график')
        btn_hist = types.KeyboardButton('Гистограмма')
        markup.add(btn_line, btn_hist)
        bot.send_message(message.from_user.id, 'Я могу построить для тебя график! Выбирай, какой хочешь?'
                         , reply_markup=markup)
        logger.info("User %s asked what a bot could do", message.from_user.id)
    elif message.text == 'Линейный график':
        chart = 1
        x = bot.send_message(message.from_user.id, "Задайте координаты х", parse_mode='Markdown')
        bot.register_next_step_handler(x, chart_x, chart)
    elif message.text == 'Гистограмма':
        chart = 2
        x = bot.send_message(message.from_user.id, "Задайте координаты х", parse_mode='Markdown')
        bot.register_next_step_handler(x, chart_x, chart)

    else:
        bot.send_animation(chat_id=message.from_user.id, animation=open('_ty_nesesh_yapfiles.ru_yapfiles.ru.gif', 'rb'))
        logger.warning("User %s sent an invalid message: %s", message.from_user.id, message.text)

    print(message.text)


def chart_x(message, chart) -> None:
    """
    Функция собирает данные для построения графиков
    :param message: сообщение
    :param chart: какой график строить (линейный или гистограмму)
    """
    lst_x = message.text.split()
    y = bot.send_message(message.from_user.id, "Задайте координаты y", parse_mode='Markdown')
    bot.register_next_step_handler(y, chart_y, lst_x, chart)


def chart_y(message, lst_x, chart) -> None:
    """
        Функция собирает данные для построения графиков
        :param message: сообщение
        :param chart: какой график строить (линейный или гистограмму)
    """
    lst_y = message.text.split()
    lst_y = sorted(lst_y)
    lst_x = sorted(lst_x)
    if chart == 1:
        line(lst_x, lst_y)
        bot.send_message(message.from_user.id, "График построен", parse_mode='Markdown')
        bot.send_photo(chat_id=message.from_user.id, photo=open('line.png', 'rb'))
        logger.info("User %s created a line chart", message.from_user.id)
    elif chart == 2:
        hist(lst_x, lst_y)
        bot.send_message(message.from_user.id, "График построен", parse_mode='Markdown')
        bot.send_photo(chat_id=message.from_user.id, photo=open('hist.png', 'rb'))
        logger.info("User %s created a histogram", message.from_user.id)


if __name__ == "__main__":
    logger.info("Bot started")
    bot.polling(none_stop=True, interval=0)
