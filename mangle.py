from microsofttranslator import Translator
import random
import configparser

# get config
config = configparser.ConfigParser()
config.read("babble_bot.cfg")

# get settings
client_id = config['translation_api']['client_id']
client_secret = config['translation_api']['client_secret']

# TODO put these in config (and update example!)
low = 2
high = 50

class Mangle:
  
  def __init__(self):
    self.translator = Translator(client_id, client_secret) 
    self.langs = self.translator.get_languages()

  def mangle(self, message_text, language='en', times=0):

    # If they didn't specify, pick a random number of 
    #     times to scramble.
    if times == 0: times = random.randint(low, high)

    for i in range(times):

      rand_lang = random.choice(self.langs)

      message_text = self.translator.translate(message_text, 
                                          from_lang=language, 
                                          to_lang=rand_lang)

      message_text = self.translator.translate(message_text,
                                          from_lang=rand_lang,
                                          to_lang=language)

    return message_text
