import requests
from functools import partial

BOT_API_URL="https://api.telegram.org/bot"

class TgException(Exception):
	pass

class TgApiConnection:
	def __init__(self, token):
		self.token = token

	def call_method(self, method, files: dict=None, **data):
		ret = requests.post(BOT_API_URL+self.token+"/"+method, data= data if data else None, files=files if files else None)
		l = ret.json()
		if l["ok"]:
			return l["result"]
		elif "description" in l:
			raise TgException(l["description"])
		else:
			raise TgException("Error. Respuesta recibida: "+str(l))

	def __getattr__(self, name):
		return partial(self.call_method, name)
