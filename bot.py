from telebot import TeleBot
from decouple import config

TOKEN = config('TOKEN')
bot = TeleBot(token=TOKEN)
