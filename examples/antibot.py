# This bot is used as a group administrator, and the only thing it does is to kick
# other bots when they are added to the group.

import tgbot
import traceback

bot = tgbot.tgCommandBot("Token")

@bot.messageHandler(msgtype="new_chat_member")
def newMember(bot, message, res):
	if message["new_chat_member"]["id"] == bot.me["id"]:
		#It's me!!
		return
	elif not "from" in message:
		#A bot cannot use invite links
		return
	else:
		#We check if it's a bot
		newuser = message["new_chat_member"]
		if "username" in newuser and newuser["username"].lower().endswith("bot"):
			try:
				#It's a bot!!
				bot.kickChatMember(chat_id=message["chat"]["id"], user_id=newuser["id"])
			except:
				traceback.print_exc()

c = 0
while True:
    u = bot.getUpdates(offset=c+1, limit=1)
    if u:
        update = u[0]
        c = update["update_id"]
        bot.proccessMessage(update["message"])

