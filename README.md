# simple-telegram-bot-api
Very simple (unofficial) wrapper for the Telegram Bot API (https://core.telegram.org/bots/api)

## Tgbot
Every method of a tgCommandBot object has the same keyword arguments, and return the same things described in [the official API documentation](https://core.telegram.org/bots/api), as a python dict, list or combination of them.

In order to send a file, you have to use the special keyword argument "files". The key is the name of the parameter that the bot API requires (in sendDocument is "document, in sendPhoto is "photo"...).

    bot.sendDocument(chat_id=1234567, files={"document": open("document.txt", "r")})

Additional documentation will come soon.

    import telegrambot

    bot = telegrambot.tgCommandBot("YourTokenHere")

    @bot.messageHandler(command="/help", chat_type="private")
    def helpCommandHandler(bot, message, result):
        bot.sendMessage(text="This is the help message!!", chat_id=message["chat"]["id"])

    bot.polling()
