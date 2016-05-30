import telebot
from mangle import Mangle
import random
import configparser
from datetime import datetime

# get config
config = configparser.ConfigParser()
config.read("babble_bot.cfg")

# create bot with key
bot = telebot.TeleBot(config['telegram_bot_api']['telegram_token'])

m = Mangle()

freq = 0.1

@bot.message_handler(func=lambda m: (random.random() < freq or "@babble_bot" in m.text))
def echo_all(message):
    # TODO getting an error here regarding utf characters. commenting it out because it's not needed.
    #print("[{}] Sending message to chat {} ({}).".format(datetime.now().time(), message.chat.title, message.chat.id))
    bot.send_message(message.chat.id, m.mangle(message_text=message.text))
		
print("Bot started!")
bot.polling()						# Bot waits for events.

