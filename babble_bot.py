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

# maps messageid -> message info dict (see mangle)
messages = {}

@bot.message_handler(func=lambda m: (random.random() < freq or "@babble_bot" in m.text))
def echo_all(message):
	message_text=message.text.replace('@babble_bot','')
	message_info = m.mangle(message_text=message_text)
	sent = bot.send_message(message.chat.id, message_info['new_message'])
	messages[sent.message_id] = message_info
	
@bot.message_handler(commands=['info'], func=lambda m: m.reply_to_message is not None and m.reply_to_message.message_id in messages)
def handle_info(message):
	message_info = messages[message.reply_to_message.message_id]
	bot.send_message(message.chat.id,
		"*original:*\n{}\n*language map:*\n{}".format(message_info['old_message'], " → ".join(message_info['languages'])),
		parse_mode = "Markdown")
		
@bot.message_handler(commands=['moreinfo'], func=lambda m: m.reply_to_message is not None and m.reply_to_message.message_id in messages)
def handle_more_info(message):
	message_info = messages[message.reply_to_message.message_id]
	bot.send_message(message.chat.id,
		"*original:*\n{}\n".format(message_info['old_message'])
		+ "*map*:\n"
		+ "\n".join(["_({})_ {}".format(message_info['languages'][i], message_info['all_messages'][i]) for i in range(len(message_info['languages']))]),
		parse_mode = "Markdown")
	
print("Bot started!")
bot.polling()						# Bot waits for events.

