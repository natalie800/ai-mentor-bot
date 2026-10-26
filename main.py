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
        elif answer in ['no', 'не', 'нет','не хочу']:
            markup = InlineKeyboardMarkup()
            btn_sad = InlineKeyboardButton("Не хочу говорить", callback_data="dont_wanna")
            markup.add(btn_sad)
            bot.send_message(message.chat.id,"Ой, а почему? Что-то случилось?", reply_markup=markup)
        else:
            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton("Да", callback_data="answer_yes"),
                InlineKeyboardButton("Нет", callback_data="answer_no"),
                )
            bot.send_message(message.chat.id,"Я не совсем понял. Пожалуйста, напиши 'да' или 'нет'. ", reply_markup=markup)
    
    bot.register_next_step_handler(message, check_answer) 

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "mode_info":
        bot.send_message(call.message.chat.id,"Отлично! Здесь я буду помогать подбирать вузы и искать стажировки.")
    
    elif call.data == "mode_train":
        bot.send_message(call.message.chat.id,"Круто! Здесь мы будем тренироваться к поступлению или стажировке, а также попробуем создать твой индивидуальный план по подготовке.")
    
    elif call.data == "dont_wanna":
        bot.send_message(call.message.chat.id,"Понимаю. Если захочешь поболтать, просто напиши /start. Я всегда здесь!")
    
    elif call.data == "answer_yes":
        bot.send_message(call.message.chat.id, "Отлично! ")
    elif call.data == "answer_no":
        bot.send_message(call.message.chat.id, "Понимаю.")
    else:
        bot.send_message(call.message.chat.id, "В разработке")

    bot.answer_callback_query(call.id)
print("Бот запущен и работает безопасно")
bot.infinity_polling()