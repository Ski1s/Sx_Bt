import telebot
import os

bot = telebot.TeleBot(token=os.environ.get('TOKEN'))
bot.remove_webhook()


