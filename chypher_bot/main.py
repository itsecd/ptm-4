import config
import telebot
from telebot import types
import Encode, Decode
from log_config import configure_logger

import random
    
LOGGER = configure_logger()
bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    """/start comand porcessor

    Args:
        message (_type_): /start message
    """
    LOGGER.info("Handled 'start'")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    btn1 = types.KeyboardButton("Зашифровать")
    btn2 = types.KeyboardButton("Расшифровать")
    
    markup.add(btn1, btn2)
    
    bot.send_message(message.from_user.id, "Добро пожаловать в text_chiper_bot!\nВыберите режим работы", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    """Keyboard catcher

    Args:
        message (_type_): Cathced message from usr
    """
    if message.text == "Зашифровать":
        LOGGER.info("Handled 'Зашифровать'")
        bot.send_message(message.from_user.id, "Введите текст, который нужно зашифровать:")
        bot.register_next_step_handler(message, encrypt_text)
        
    elif message.text == "Расшифровать":
        LOGGER.info("Handled 'Расшифровать'")
        bot.send_message(message.from_user.id, "Введите ключ:")
        bot.register_next_step_handler(message, get_key)
    
    else:
        LOGGER.warn("Handled unexpected message")
        wordlist = "Камень","Ножницы","Бумага"
        word = random.choice(wordlist)
        bot.send_message(message.from_user.id, word)
        
def encrypt_text(message):
    """Encrypts cathced message

    Args:
        message (_type_): Catched message from usr
    """
    LOGGER.info("Encryption started")
    text = message.text
    
    text_result, key = Encode.EncodeText(text)
    
    LOGGER.info("Encryption finished")
    
    bot.send_message(message.from_user.id, f"Зашифрованный текст:")
    bot.send_message(message.from_user.id, text_result)
    bot.send_message(message.from_user.id, f"Ключ:")
    bot.send_message(message.from_user.id, key)
    
KEY = bytes()
    
def get_key(message):
    """Cathces key message from usr

    Args:
        message (_type_): Catched message from user
    """
    global KEY 
    KEY = bytes(message.text, encoding="utf-8")
    
    bot.send_message(message.from_user.id, "Введите текст, который нужно расшифровать:")
    bot.register_next_step_handler(message, decrypt_text)
    LOGGER.info("Secret key handled. Waiting for message.")

def decrypt_text(message):
    """Get text to decrypt and start decryption foo

    Args:
        message (_type_): The message from user
    """
    text = message.text
    LOGGER.info("Decryption started")
    result = Decode.DecodeText(text, KEY)
    LOGGER.info("Decryption finished")
    bot.send_message(message.from_user.id, f"Расшифрованный текст:\n {result}")
    

def main(): 
    """main
    """
    bot.polling(none_stop=True, interval=0)
    
if __name__=="__main__":
    main()