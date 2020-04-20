import telebot
from mangle import Mangle
import random
import configparser
from datetime import datetime
import re
from time import time
from mangle import MangleMethod

# get config
config = configparser.ConfigParser()
config.read("babble_bot.cfg")

# create bot with key
bot = telebot.TeleBot(config['telegram_bot_api']['telegram_token'])

blacklist = set(["tlh-Qaak"])

m = Mangle(client_key=config['translation_api']['client_key'],
           language="en",
           language_blacklist=blacklist,
           low=2,
           high=50)

freq = 0.1

times_to_mangle_info_messages = 2

# maps messageid -> message info dict (see mangle)
messages = {}

languages = set(m.languages) - blacklist

language = "en"

bracket_matcher = re.compile("^\[.*\]")
language_matcher = re.compile(r"[\w-]+")

# TODO put these in config (and update example!)
#low = 2
#high = 50

since = int(time())


@bot.message_handler(
    func=lambda m: int(m.date) > since and "/info" not in m.text and
    (random.random() < freq or
     (m.text is not None and "@babble_bot" in m.text)))
def mangle_message(message):
    message_text, language_list = parse(message.text)

    method = None
    if language_list:
        method = MangleMethod.manual

    message_info = m.mangle(message_text,
                            method=method,
                            language_list=language_list)

    if message_info['all_messages'] is False:
        bot.send_message(message.chat.id,
                         "_{}_".format(
                             m.mangle("One or more languages not recognized.",
                                      3)),
                         parse_mode="Markdown")
        return

    sent = bot.send_message(message.chat.id, message_info['all_messages'][-1])
    messages[sent.message_id] = message_info


@bot.message_handler(
    commands=['info'],
    func=lambda m: m.reply_to_message is not None and m.reply_to_message.
    message_id in messages and int(m.date) > since)
def handle_info(message):
    message_info = messages[message.reply_to_message.message_id]
    bot.send_message(
        message.chat.id,
        "*{}:*\n{}\n".format(mangle_info("language picking method"),
                             mangle_info(message_info['method'])) +
        "*{}*:\n".format(mangle_info("all translations")) + "\n".join([
            "_({})_ {}".format(message_info['languages'][i],
                               message_info['all_messages'][i])
            for i in range(len(message_info['languages']))
        ]),
        parse_mode="Markdown")


def parse(text):
    '''
	Parses a message's text, performing a few tasks:
	- Remove instances of '@babble_bot ' and '@babble_bot'
	- Parse a language list from the start of the message
	'''

    text = re.sub("@babble_bot *", "", text)

    language_list_result = re.search("^\[.*\]", text)
    found_languages = None
    if language_list_result:
        language_list_string = language_list_result.group(0)[
            1:-1]  # remove brackets on the sides
        found_languages = re.findall("[\w-]+", language_list_string)
        text = re.sub("^\[.*\] *", "", text)

    return (text, None if not found_languages else list(found_languages))


def mangle_info(text):
    return m.mangle(text,
                    method=MangleMethod.straight,
                    times=times_to_mangle_info_messages)['all_messages'][-1]


print("Bot started!")
bot.polling()  # Bot waits for events.
