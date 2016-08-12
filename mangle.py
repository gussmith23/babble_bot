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
	
	def translate_through_path(self, message_text, path):
		'''
		Translates a message through a series of languages.
		path: The path of languages the message should be translated through. The
					first language in the list should be the language which the message
					starts in.
		Returns a list of every step of the translation, where the first item is the
		orignal message and the last is the final state.
		'''
		all_stages = [message_text]
		for i in range(len(path)):
			if i == 0:
				continue
			all_stages.append(self.translator.translate(all_stages[i - 1],
																									from_lang = path[i - 1], 
																									to_lang = path[i]))
		return all_stages

	
	def mangle(self, message_text, language='en', times=0):
		'''
		Returns a dict with the following fields:
		- old_message
		- new_message
		- languages: a list of the languages traversed in order
		- all_messages: a list of the message at each stage of translation
		'''

		mangled_message_info = {
			'old_message' : message_text,
			'new_message' : '',
			'languages' : [],
			'all_messages' : []
		}

		# If they didn't specify, pick a random number of 
		#     times to scramble.
		if times == 0: times = random.randint(low, high)

		for i in range(times):

			rand_lang = random.choice(self.langs)

			message_text = self.translator.translate(message_text, 
																		from_lang=language, 
																		to_lang=rand_lang)
																		
			mangled_message_info['languages'].append(rand_lang)
			mangled_message_info['all_messages'].append(message_text)

			message_text = self.translator.translate(message_text,
																		from_lang=rand_lang,
																		to_lang=language)

			mangled_message_info['languages'].append('en')
			mangled_message_info['all_messages'].append(message_text)

		mangled_message_info['new_message'] = message_text
		return mangled_message_info
