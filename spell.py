from halmodule import HalModule
from aspell import Speller
import re

class Spell(HalModule):

	def init(self):
		self.active = (self.config.get('active')) or False
		self.lang = (self.config.get('lang')) or 'en'

		self.rgx = re.compile(r"[^a-zA-Z']")
		self.speller = Speller('lang', self.lang)

	def ignore(self, msg, words):
		if len(words) > 1:
			for m in words:
				for w in self.rgx.split(m):
					self.speller.addtoSession(w)
			self.reply(msg, 'These words are now a component of the descriptivist English language: ' + ', '.join(words[1:]))
		else:
			self.reply(msg, 'Ah, good, I see you are a prescriptivist as well.')

	def correct(self, msg, words):
		for m in words:
			for w in self.rgx.split(m):
				if w.isalpha() and not self.speller.check(w):
					if (len(self.speller.suggest(w)) > 0):
						self.reply(msg, "'" + w + "'? Did you mean '" + self.speller.suggest(w)[0] + "'?")

	def receive(self, msg):
		words = msg['body'].split(' ')

		if words[0] == '!spellignore':
			self.ignore(msg, words[1:])
		elif words[0] == '!spellcheck':
			self.correct(msg, words[1:])
		elif self.active:
			self.correct(msg, words)

