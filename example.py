import sys
import datetime
import telebot
from loguru import logger
from telebot_calendar import Calendar, CallbackData, RUSSIAN_LANGUAGE

from telebot.types import ReplyKeyboardRemove, CallbackQuery

def error_filter(record):
    return record["level"].name == "ERROR"

logger.configure(handlers=[{"sink": sys.stderr, "format": "{time} {level} {message} {function} {line}"}])

API_TOKEN = "6605597490:AAHI49AcT_bSQ0ariJIfrucybV5YR1HwFTE"
logger.add("errors.log", filter=error_filter)

bot = telebot.TeleBot(API_TOKEN)

# Creates a unique calendar
calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_1_callback = CallbackData("calendar_1", "action", "year", "month", "day")


@bot.message_handler(commands=["start"])
def check_other_messages(message):
    """
    Catches a message with the command "start" and sends the calendar

    :param message:
    :return:
    """
    try:
        logger.info(f"Received /start command from user: {message.from_user.id}")
        now = datetime.datetime.now()  # Get the current date
        bot.send_message(
            message.chat.id,
            "Selected date",
            reply_markup=calendar.create_calendar(
                name=calendar_1_callback.prefix,
                year=now.year,
                month=now.month,  # Specify the NAME of your calendar
            ),
        )
        logger.debug(f"Sent calendar to user: {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in /start handler: {e}")


@bot.callback_query_handler(
    func=lambda call: call.data.startswith(calendar_1_callback.prefix)
)
def callback_inline(call: CallbackQuery):
    """
    Обработка inline callback запросов
    :param call:
    :return:
    """
    try:
        # At this point, we are sure that this calendar is ours. So we cut the line by the separator of our calendar
        name, action, year, month, day = call.data.split(calendar_1_callback.sep)
        # Processing the calendar. Get either the date or None if the buttons are of a different type
        date = calendar.calendar_query_handler(
            bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
        )
        # There are additional steps. Let's say if the date DAY is selected, you can execute your code. I sent a message.
        if action == "DAY":
            bot.send_message(
                chat_id=call.from_user.id,
                text=f"You have chosen {date.strftime('%d.%m.%Y')}",
                reply_markup=ReplyKeyboardRemove(),
            )
            logger.info(f"User {call.from_user.id} selected date: {date.strftime('%d.%m.%Y')}")
            print(f"{calendar_1_callback}: Day: {date.strftime('%d.%m.%Y')}")
        elif action == "CANCEL":
            bot.send_message(
                chat_id=call.from_user.id,
                text="Cancellation",
                reply_markup=ReplyKeyboardRemove(),
            )
            logger.info(f"User {call.from_user.id} cancelled the action.")
            print(f"{calendar_1_callback}: Cancellation")
    except Exception as e:
        logger.error(f"Error in callback query handler: {e}")


bot.polling(none_stop=True)