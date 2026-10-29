import os
import telebot
import json
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
            bot.send_message(message.chat.id,"Я не совсем понял. Пожалуйста, выбери 'да' или 'нет'. ", reply_markup=markup)
    
    bot.register_next_step_handler(message, check_answer) 

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):

    if call.data == "mode_info":
        
        markup = InlineKeyboardMarkup()
        btn_unis = InlineKeyboardButton("Поступление", callback_data="info_unis")
        btn_interview = InlineKeyboardButton("Собеседование", callback_data="info_interview")
        btn_internships = InlineKeyboardButton("Стажировка", callback_data="info_internships")
        markup.add(btn_unis)
        markup.add(btn_interview)
        markup.add(btn_internships)
        bot.send_message(call.message.chat.id, "Отлично! Выбери, что будем искать:", reply_markup=markup)
    
    elif call.data == "mode_train":
        bot.send_message(call.message.chat.id,"Круто! Здесь мы будем тренироваться к поступлению или стажировке, а также попробуем создать твой индивидуальный план по подготовке.")
    
    elif call.data == "dont_wanna":
        bot.send_message(call.message.chat.id,"Понимаю. Если захочешь поболтать, просто напиши /start. Я всегда здесь!")
    
    elif call.data == "answer_no":
        bot.send_message(call.message.chat.id, "Понимаю. Тогда в следующий раз.")

    elif call.data == "answer_yes":
         markup = InlineKeyboardMarkup()
         btn_info = InlineKeyboardButton("Справочник", callback_data="mode_info")
         btn_train = InlineKeyboardButton("Тренажёр", callback_data="mode_train")
         markup.add(btn_info, btn_train)
         bot.send_message(call.message.chat.id,"Отлично! Вот, что я умею (мои два режима):", reply_markup=markup)

    elif call.data == "info_unis":
        markup_spec = InlineKeyboardMarkup()
        btn_ib = InlineKeyboardButton("Информационная безопасность", callback_data="spec_ib")
        btn_other = InlineKeyboardButton("Другая специальность", callback_data="spec_other")
        markup_spec.add(btn_ib)
        markup_spec.add(btn_other)

        bot.send_message(call.message.chat.id,"Отлично! Какая у тебя специальность?", reply_markup=markup_spec)

    elif call.data == "spec_ib": 
        with open('database.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        text = "<b>Вузы по Информационной безопасности:</b>\n\n"

        for vuz in data['admission']:
            if "безопасность" in vuz['program'].lower():
                text += f"<b>{vuz['university']}</b>\n"
                text += f"Направление: {vuz['program']}\n"
                text += f"Баллы: {vuz['score']}\n"
                text += f"<a href='{vuz['source']}'>Сайт вуза</a>\n\n"
        
        text += "<i>Рекомендации носят ознакомительный характер и не заменяют официальные требования вузов и работодателей.</i>"
        
        bot.send_message(call.message.chat.id, text, parse_mode='HTML')

    elif call.data == "spec_other":

        markup_back = InlineKeyboardMarkup()
        btn_back = InlineKeyboardButton("Вернуться к выбору", callback_data="info_unis")
        markup_back.add(btn_back)
        
        bot.send_message(call.message.chat.id, "Ой, Информация по этой специальности пока в разработке. Но я уже учусь её искать! Возращайся чуть позже или выбери ИБ.", reply_markup=markup_back)
    
    elif call.data == "info_internships":

        markup_intern = InlineKeyboardMarkup()
        btn_intern_ib = InlineKeyboardButton("Информационная безопасность", callback_data="intern_ib")
        btn_intern_other = InlineKeyboardButton("Другая специальность", callback_data="intern_other")

        markup_intern.add(btn_intern_ib)
        markup_intern.add(btn_intern_other)

        bot.send_message(call.message.chat.id,"Хорошо, в какой сфере ты ищещь стажировку?")


    elif call.data == "info_interview":
         bot.send_message(call.message.chat.id,"Отлично! Какая у тебя специальность?")


         
    else:
        bot.send_message(call.message.chat.id, "В разработке, скоро появится")

    bot.answer_callback_query(call.id)
print("Бот запущен и работает безопасно")
bot.infinity_polling()