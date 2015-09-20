# simple-telegram-bot-api
Very simple (unofficial) wrapper for the Telegram Bot API (https://core.telegram.org/bots/api)

This is the way you work with it:

    import tgbotapi
    bot = tgbotapi.tgBot("bot1234567:asdfghjklasdfghjklasdfghjkl")
    
    u = bot.getUpdates(offset=1111, limit=10, timeout=20)
    
    if u:
        for x in u:
            chat = x["message"]["chat"]
            bot.sendMessage(chat_id=chat, text="Hello", reply_markup={"keyboard": [["Hello"], ["Hi"]], one_time_keyboard=True})
            
            


Every method of tgBot objects have the same keyword arguments, and return the same things described in [the official API documentation](https://core.telegram.org/bots/api), as a python dict, list or combination of them.

In order to send a file, you have to use the special keyword argument "files". The key is the name of the parameter that the bot API requires (in sendDocument is "document, in sendPhoto is "photo"...).

    bot.sendDocument(chat_id=1234567, files={"document": open("document.txt", "r")})
