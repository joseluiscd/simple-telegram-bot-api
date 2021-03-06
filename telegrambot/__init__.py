from . import tgbotapi
import re
import time

class TgCommandBot(tgbotapi.TgApiConnection):
	def __init__(self, token, webhook=True):
		super().__init__(token)
		try:
			self.me = self.getMe()
		except:
			time.sleep(5)

		self.cmdregex = re.compile("^/(?P<command>[a-zA-Z0-9]+)(|\@(?P<bot>[a-zA-Z0-9]+))($| )")

	handlers = dict()
	hooks_user = dict()
	hooks_group = dict()
	callbacks = dict()
	middleware = list()

	def runMiddleware(self, message):
		for f in self.middleware:
			print("Run", f)
			ret = f(message)

			if ret is False:
				return
			elif ret is not None:
				message = ret

		return message

	def processUpdate(self, update):
		if "message" in update:
			return self.processMessage(update["message"])
		elif "callback_query" in update:
			return self.processCallbackQuery(update["callback_query"])

	def processCallbackQuery(self, callback_query):
		for regex in self.callbacks:
			match = regex.match(callback_query["data"])
			if match:
				self.callbacks[regex](self, callback_query, match)


	def processMessage(self, message):
		message = self.runMiddleware(message)
		if message is None:
			return

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

	def polling(self, timeout=20):
		current_offset = 0
		while True:
			u = self.getUpdates(offset=current_offset, limit=1, timeout=timeout)
			if u:
				update = u[0]
				current_offset = update["update_id"]+1
				self.processUpdate(update)

	def fMessageHandler(self, fn_condition):
		def decorator(func):
			self.handlers[fn_condition] = func

		return decorator

	def callbackQueryHandler(self, regex):
		def decorator(fn):
			self.callbacks[regex] = fn
			return fn
		return decorator

	def middlewareHandler(self, func):
		print("New middleware")
		self.middleware.append(func)
		return func

	def messageHandler(self, msgtype="text", group=True, private=True, sudo=False, command=None, custom_fn=None):
		def fn_condition(bot, message):
			if (message["chat"]["type"]=="group" or message["chat"]["type"]=="group") and not group:
				return False

			if message["chat"]["type"]=="private" and not private:
				return False

			if sudo and not ("sudo" in message["from"] and message["from"]["sudo"]):
				#Middleware is used as "sudo", you have to change message["from"] and add "sudo" as True
				return False

			if msgtype and not msgtype in message:
				return False

			if command and msgtype=="text":
				match = self.cmdregex.match(message["text"])
				if match:
					grouped = match.groupdict()
					if grouped["command"]==command and (not grouped["bot"] or grouped["bot"]==self.me["username"]):
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
