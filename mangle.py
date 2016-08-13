from microsofttranslator import Translator
import random
import configparser
from enum import Enum

# get config
config = configparser.ConfigParser()
config.read("babble_bot.cfg")

class MangleMethod(Enum):
	flipflop = 1
	straight = 2
	manual = 3
	def __str__(self):
		if self == MangleMethod.flipflop:
			return "flip flop: flip flop between a primary language and random languages."
		elif self == MangleMethod.straight:
			return "straight: run through a completely random list of languages."
		elif self == MangleMethod.manual:
			return "manual: language path specified by the user manually."
		else:
			raise NotImplementedError("MangleMethod value's __str__ conversion not implemented.")

class Mangle:

	def __init__(self, client_id, client_secret,
								language, low, high, language_blacklist):
		self.language = language
		self.translator = Translator(client_id, client_secret) 
		self.languages = set(self.translator.get_languages()) - language_blacklist
		self.low = low
		self.high = high
			
	def mangle(self, 
							message_text, 
							times = 0, 
							method = None, 
							language_list = None):
							
		if method == MangleMethod.manual and not language_list:
			raise ValueError("No language list given.")
		if method is None:
			method = random.sample(set(MangleMethod) - set([MangleMethod.manual]), 1)[0]
		if times < 0:
			raise ValueError("Parameter times must be greater than 0.")
		if times == 0:
			times = random.randint(self.low, self.high)
			
		if method == MangleMethod.manual:
			language_list.insert(0, self.language)
			language_list.append(self.language)
		elif method == MangleMethod.flipflop:
			language_list = []
			language_list.append(self.language)
			for i in range(int(times/2)):
				language_list.extend([random.sample(self.languages, 1)[0], self.language])
		elif method == MangleMethod.straight:
			language_list = []
			language_list.append(self.language)
			language_list.extend(random.sample(self.languages, times))
			language_list.append(self.language)
		else:
			raise NotImplementedError("MangleMethod {} not implemented.".format(method))
		
		all_messages = [message_text]
		for i in range(len(language_list)):
			if i == 0:
				continue
			try:
				text = self.translator.translate(all_messages[i - 1],
																				from_lang = language_list[i - 1], 
																				to_lang = language_list[i])
				all_messages.append(text)
			except Exception as e:
				all_messages = False
				break
						
		message_info = {
			'method' : str(method),
			'languages' : language_list,
			'all_messages' : all_messages
		}
		
		return message_info