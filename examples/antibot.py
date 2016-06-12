# This bot is used as a group administrator, and the only thing it does is to kick
# other bots when they are added to the group.

import telegrambot
import traceback

bot = telegrambot.TgCommandBot("Bot_token")
admin = "YourUsernameHere"

@bot.messageHandler(msgtype="new_chat_member")
def newMember(bot, message, res):
	print("Nuevo")
	if message["new_chat_member"]["id"] == bot.me["id"]:
		if not "username" in message["from"] or message["from"]["username"]!=admin:
			bot.leaveChat(chat_id=message["chat"]["id"])
	elif not "from" in message:
		#A bot cannot use invite links
		return
	else:
		#We check if it's a bot
		newuser = message["new_chat_member"]
		user = message["from"]
		user = "@"+user["username"] if "username" in user else user["first_name"]
		if "username" in newuser and newuser["username"].lower().endswith("bot"):
			try:
				#It's a bot!!
				bot.sendMessage(chat_id=message["chat"]["id"],
						text=user+" ha invitado a un bot!! Fuera!!")
				bot.kickChatMember(chat_id=message["chat"]["id"],
						user_id=newuser["id"])
			except:
				traceback.print_exc()

if __name__=="__main__":
	bot.polling()
