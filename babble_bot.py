import telebot
from mangle import Mangle
import random
import configparser

config = configparser.ConfigParser()
config.read("babble_bot.cfg")

token = "218900293:AAHAt4y4KNYRqC1YPU0Q7YftJby4tvTrcEQ"

bot = telebot.TeleBot(config['telegram_bot_api']['telegram_token'])

m = Mangle()

freq = 0.1

@bot.message_handler(func=lambda m: random.random() < freq)
def echo_all(message):
    print("Sending message...")
    bot.send_message(message.chat.id, m.mangle(message_text=message.text))

bot.polling()
