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
        markup_train = InlineKeyboardMarkup()
        btn_train_ib = InlineKeyboardButton("Информационная безопасность", callback_data="train_ib")
        btn_train_other = InlineKeyboardButton("Другая специальность", callback_data="train_other")
        markup_train.add(btn_train_ib)
        markup_train.add(btn_train_other)

        bot.send_message(call.message.chat.id, "Круто! Здесь мы будем тренироваться к поступлению или стажировке, а также попробуем создать твой индивидуальный план по подготовке.\nКакая специальность тебя интересует?", reply_markup=markup_train) # <--- добавили reply_markup

    elif call.data == "train_ib":
        with open('database.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        question_data = data['interview'][0]
        msg = bot.send_message(call.message.chat.id, f"<b>Вопрос на собеседовании:</b>\n\n{question_data['question']}\n\nНапиши свой ответ сообщением:", parse_mode='HTML')
        
        # Ждем ответа пользователя
        bot.register_next_step_handler(msg, check_interview)

    elif call.data == "train_other":
        markup_back_train = InlineKeyboardMarkup()
        btn_back_train = InlineKeyboardButton("Вернуться к выбору", callback_data="mode_train")
        markup_back_train.add(btn_back_train)
        bot.send_message(call.message.chat.id, "Ой, Информация по этой специальности пока в разработке. Попробуй выбрать ИБ или приходи позже.", reply_markup=markup_back_train)

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
        
        text += "<i>⚠️ Рекомендации носят ознакомительный характер и не заменяют официальные требования вузов и работодателей.</i>"
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
        bot.send_message(call.message.chat.id,"Хорошо, в какой сфере ты ищещь стажировку?",reply_markup=markup_intern)

    elif call.data == "intern_ib":
        with open('database.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        text = " <b>Доступные стажировки в сфере ИБ:</b>\n\n"
        found = False
        for job in data['internship']:
            found = True
            company = job.get('company', 'Компания не указана')
            role = job.get('role', 'Стажер')
            reqs = job.get('requirements', 'Требования не указаны')
            link = job.get('source', '#')
       
            text += f"<b>{company}</b>\n"
            text += f"Роль: {role}\n"
            text += f"Требования: {reqs}\n"
            text += f"🔗 <a href='{link}'>Узнать подробнее</a>\n\n"
       
        if not found:
            text += "Пока в базе нет активных стажировок в этой сфере.\n\n"
            
        text += "<i>⚠️ Рекомендации носят ознакомительный характер и не заменяют официальные требования работодателей.</i>"
        bot.send_message(call.message.chat.id, text, parse_mode='HTML')
        
    elif call.data == "intern_other":
        markup_back_intern = InlineKeyboardMarkup()
        btn_back_intern = InlineKeyboardButton(" Вернуться к выбору", callback_data="info_internships")
        markup_back_intern.add(btn_back_intern)
        bot.send_message(call.message.chat.id, "Ой! Стажировки по этой специальности пока в разработке. Попробуй выбрать ИБ.", reply_markup=markup_back_intern)

    elif call.data == "info_interview":
        with open('database.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            tip_data = data['interview'][0]
        
            text = f"<b>💡 Шпаргалка: Как проходить собеседование</b>\n\n"
            text += f"<b>Пример вопроса:</b> {tip_data['question']}\n\n"
            text += f"❌ <b>Плохой ответ:</b> {tip_data['bad_answer']}\n\n"
            text += f"✅ <b>Хороший ответ:</b> {tip_data['good_answer']}\n\n"
            text += f"<b>Совет:</b> {tip_data['tip']}"
        
            markup_back = InlineKeyboardMarkup()
            btn_train_ib = InlineKeyboardButton("Потренироваться", callback_data="train_ib")
            btn_back = InlineKeyboardButton("В меню", callback_data="answer_yes")
            markup_back.add(btn_train_ib, btn_back)
        
            bot.send_message(call.message.chat.id, text, parse_mode='HTML', reply_markup=markup_back)
         
    else:
        bot.send_message(call.message.chat.id, "В разработке, скоро появится")

    

    bot.answer_callback_query(call.id)
    
def check_interview(message):
    if not message.text:
        bot.send_message(message.chat.id, "Пожалуйста, напиши свой ответ текстом ")
        return

    user_text = message.text.lower()

    with open('database.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    q_data = data['interview'][0]

    markup_after = InlineKeyboardMarkup()
    btn_try_again = InlineKeyboardButton("Пройти ещё раз", callback_data="train_ib")
    btn_to_menu = InlineKeyboardButton("В меню", callback_data="answer_yes")
    markup_after.add(btn_try_again, btn_to_menu)

   
    bad_words = ["не знаю", "не умею", "деньг", "зарплат", "бабк", "бабл", "просто"]
    is_bad = len(user_text) < 30 or any(word in user_text for word in bad_words)

    if is_bad:
        bot.send_message(message.chat.id, f"❌<b>Ошибка!</b> Так отвечать не стоит.\n\nПример плохого ответа: {q_data['bad_answer']}\n\n<b>Совет:</b> {q_data['tip']}", parse_mode='HTML', reply_markup=markup_after)
    else:
        bot.send_message(message.chat.id, f"✅<b>Отличный ответ!</b>\n\nВот как можно было ответить ещё лучше: {q_data['good_answer']}\n\n<b>Совет:</b> {q_data['tip']}", parse_mode='HTML', reply_markup=markup_after)
    
print("Бот запущен и работает безопасно")
bot.infinity_polling()