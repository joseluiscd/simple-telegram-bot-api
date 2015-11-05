import tgbotapi
import re

CANCEL_MSG="/cancel"

class tgCommandBot(api.tgBot):
	def __init__(self, token, bbdd_conn, webhook=True):
		super().__init__(token)
		self.bbdd = bbdd.Bbdd(bbdd_conn)
		self.me = self.getMe()
		self.cmdregex = re.compile("^/(?P<command>[a-zA-Z0-9]+)(|\@(?P<bot>[a-zA-Z0-9]+))($| )")

	handlers = dict()
	hooks_user = dict()
	hooks_group = dict()

	def proccessMessage(self, message):
		#Hooks
		if message["chat"]["type"]=="private" and message["chat"]["id"] in self.hooks_user: # Hook para el usuario
			if "text" in message and message["text"]=="/cancel":
				self.endHook(message)
				return
			self.hooks_user[message["chat"]["id"]](self, message)
			return
		elif "reply_to_message" in message:
			a = "{0}-{1}".format(message["chat"]["id"], message["reply_to_message"]["message_id"])
			if a in self.hooks_group:
				self.hooks_group[a](self, message)
				return

		#Handlers

		for func in self.handlers:
			ret = func(self, message)
			if ret: # Se cumple la condición??
				self.handlers[func](self, message, ret) #Se le pasa el bot y el mensaje

		return

	def setHook(self, message, func):
		if message["chat"]["type"]=="private": #Usuario
			self.hooks_user[message["chat"]["id"]] = func
		else: #Todo un grupo
			self.hooks_group["{0}-{1}".format(message["chat"]["id"], message["message_id"])] = func

	def endHook(self, message):
		if message["chat"]["type"]=="private": #Usuario
			del(self.hooks_user[message["chat"]["id"]])
		else: #Todo un grupo
			del(self.hooks_group["{0}-{1}".format(message["chat"]["id"], message["message_id"])])

	def fMessageHandler(self, fn_condition):
		def decorator(func):
			self.handlers[fn_condition] = func

		return decorator

	def messageHandler(self, msgtype="text", chat_type="group", sudo=False, command=None, custom_fn=None):
		def fn_condition(bot, message):
			if chat_type and message["chat"]["type"] != chat_type:
				return False

			if sudo:
				#You have to implement your superuser system.
				return False

			if msgtype and not msgtype in message:
				return False

			if command and msgtype=="text":
				match = self.cmdregex.match(message["text"])
				if match:
					grouped = match.groupdict()
					if grouped["comando"]==command and (not grouped["bot"] or grouped["bot"]==self.me["username"]):
						return match
					else:
						return False
				else:
					return False

			if custom_fn:
				return custom_fn(bot, message)

			return True

		def decorator(func):
			self.handlers[fn_condition] = func

		return decorator
