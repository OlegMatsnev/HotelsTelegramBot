# db.py
from telebot import TeleBot
from bot.handlers.user import register_user_handlers
from bot.misc import TgKeys

bot = TeleBot(token=TgKeys.TOKEN)

# Регистрируем обработчики для пользователей
register_user_handlers(bot)



