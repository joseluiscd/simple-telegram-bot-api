from setuptools import setup
setup(
    name = "simple-telegram-bot-api",
    version = "0.0.2",
    author = "José Luis C.D.",
    description = ("A simple telegram bot API for telegram"),
    license = "GPL",
    url = "https://github.com/joseluiscd/simple-telegram-bot-api",
    packages=["telegrambot"],
    install_requires=["requests"]
)
