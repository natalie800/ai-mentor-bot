import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

load_dotenv()

TOKEN= os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Я бот ~Treasure Map~\n Хочешь узнать, что я умею?")

    
    def check_answer(message):
        answer = message.text.lower()

        if answer in ['yes', 'sure', 'да', 'конечно', 'угу', 'мгм']:
        
            markup = InlineKeyboardMarkup()
            btn_info = InlineKeyboardButton("Справочник", callback_data="mode_info")
            btn_train = InlineKeyboardButton("Тренажёр", callback_data="mode_train")
            markup.add(btn_info, btn_train)
            bot.send_message(message.chat.id,"Отлично! Вот, что я умею (мои два режима):", reply_markup=markup)
    bot.register_next_step_handler(message, check_answer) 

print("Бот запущен и работает безопасно")
bot.infinity_polling()