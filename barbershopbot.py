import telebot
from telebot import types
import json

bot = telebot.TeleBot('7174512848:AAEHOk8B9Jk5Xh_Lh5ZbhF9nVbIqY7gmv3U')

SUPPORT_CHAT_ID = "123456789"  # Замените на chat_id чата с техподдержкой


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Привет, я бот для парикмахерской. Это сообщение можно изменить /registr')



# Функция для сохранения данных
def save_data(chat_id, fio):
    data = {
        "chat_id": chat_id,
        "fio": fio
    }
    
    with open("data.json", "a", encoding='utf-8') as file:
        json_str = json.dumps(data, ensure_ascii=False) 
        file.write(json_str + "\n")



services = {
    'haircut': 'Парикмахерские услуги',
    'manicure': 'Маникюр/педикюр',
    'solarium': 'Солярий',
    'eyelash': 'Наращивание ресниц'
} # добавляем сервисы

master = {
    'haircut': 'Наталия',
    'manicure': 'Аня',
    'solarium': 'Яна',
    'eyelash': 'Ольга'
} # добавляем мастеров

@bot.message_handler(commands=['menu'])
def show_menu(message):
    markup = types.InlineKeyboardMarkup()

    for key, value in services.items():
        button = types.InlineKeyboardButton(value, callback_data=key)
        markup.add(button)
    
    support_button = types.InlineKeyboardButton("Техподдержка", callback_data='support')
    markup.add(support_button)


    bot.send_message(message.chat.id, 'Меню услуг:', reply_markup=markup)



@bot.callback_query_handler(func=lambda call: call.data == 'support')
def support_handler(call):
    bot.send_message(call.message.chat.id, 'Свяжитесь с нами в личные сообщения для получения помощи.')
    markup = types.InlineKeyboardMarkup()

    # Отправка ссылки на ЛС техподдержки ОБЯЗАТЕЛЬНО ВВЕСТИ chat id техподдрежки
    support_link = f"tg://user?id={SUPPORT_CHAT_ID}"

    return_button = types.InlineKeyboardButton("Назад в меню", callback_data='back_to_menu')
    markup.add(return_button)
               
    bot.send_message(call.message.chat.id, f"Нажмите на [эту ссылку]({support_link}) для связи с техподдержкой.", parse_mode='Markdown', reply_markup=markup)

times = ['10:00', '14:00', '16:00', '18:00']


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data in services:
        chosen_service = services[call.data]
        chosen_master = master[call.data]

        keyboard = types.InlineKeyboardMarkup()

        for time in times:
            button = types.InlineKeyboardButton(time, callback_data=f'select_time_{time}')
            keyboard.add(button)

        return_button = types.InlineKeyboardButton("Назад в меню", callback_data='back_to_menu')
        keyboard.add(return_button)

        bot.send_message(call.message.chat.id, "Выберите удобное время:", reply_markup=keyboard)

    elif call.data in [f'select_time_{t}' for t in times]:
        chosen_time = call.data.split('_')[2] 

        return_button = types.InlineKeyboardButton("Назад в меню", callback_data='back_to_menu')
        markup = types.InlineKeyboardMarkup()
        markup.add(return_button)

        bot.send_message(call.message.chat.id, f'Вы успешно выбрали время: {chosen_time}', reply_markup=markup)

    elif call.data == 'choose_master':
        chosen_master = master[call.data]
        chosen_master = f'Мастер: {chosen_master}'

        return_button = types.InlineKeyboardButton("Назад в меню", callback_data='back_to_menu')
        markup = types.InlineKeyboardMarkup()
        markup.add(return_button)

        bot.send_message(call.message.chat.id, f'Вы выбрали {chosen_master}', reply_markup=markup)
    elif call.data == 'back_to_menu':
        show_menu(call.message)
    else:
        return_button = types.InlineKeyboardButton("Назад в меню", callback_data='back_to_menu')
        markup = types.InlineKeyboardMarkup()
        markup.add(return_button)

        bot.send_message(call.message.chat.id, 'Пожалуйста, выберите услугу из списка.', reply_markup=markup)





@bot.callback_query_handler(func=lambda call: call.data == 'choose_master')
def choose_master_handler(call):
    bot.send_message(call.message.chat.id, 'Вы сделали выбор мастера.')



@bot.message_handler(commands=['registr'])
def registr(message):
    global waiting_for_fio
    chat_id = message.chat.id
    
    waiting_for_fio = True
    bot.send_message(chat_id, "Для регистрации введите ваше ФИО одним сообщением")

waiting_for_fio = False

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global waiting_for_fio
    
    if waiting_for_fio:
        chat_id = message.chat.id
        fio = message.text 
        save_data(chat_id, fio) # сохраняем в локальном файле на компьютере
        waiting_for_fio = False
        bot.send_message(chat_id, "Спасибо за регистрацию!")


bot.polling()
