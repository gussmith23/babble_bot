from microsofttranslator import Translator
import random

languages = ["af", "sq", "ar","be", "bg", "ca", "zh-CN", "zh-TW", "hr",
          "cs", "da", "nl", "en", "et", "tl", "fi", "fr", "gl", "de",
          "el", "iw", "hi", "hu", "is", "id", "ga", "it", "ja", "ko",
          "lv", "lt", "mk", "ms", "mt", "no", "fa", "pl", "pt", "ro",
          "ru", "sr", "sk", "sl", "es", "sw", "sv", "th", "tr", "uk",
          "vi", "cy", "yi"]

client_id = 'babble_bot'
client_secret = 'YKJH9gMPCuoSV82xqB3ncVWcitu3Ts+pBRIDapkppWU='



low = 2
high = 5

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
