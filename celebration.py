import requests
from bs4 import BeautifulSoup
import datetime
import telebot

bot = telebot.TeleBot('7139014883:AAFuYlgSTmErdwHPTKJGvWSsa-QYFZ0lfW0')

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет! У меня есть 2 функции - я могу найти любое слово на википедии, просто отправь его мне, или же я могу сказать какой будет сегодня праздник, с помощью команды: /prazdnik")

@bot.message_handler(commands=["prazdnik"])
def praznd(message):
    try:
        current_date = datetime.datetime.now()
        date_years = current_date.strftime('%y')
        date_month = current_date.strftime('%m')
        date_day = current_date.strftime('%d')
        
        response = requests.get(f'https://www.calend.ru/calendar/periodic/20{date_years}/{date_month}/{date_day}/')
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        for h3_tag in soup.find('h3'):
            holiday_name = h3_tag.text.strip()
            bot.send_message(message.chat.id, holiday_name)
        
    except requests.exceptions.RequestException as e:
        bot.send_message(message.chat.id, f"Не удалось выполнить запрос: {e}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")

import wikipedia


    
@bot.message_handler(content_types = ['text'])
def handle_text(message):
    try:
        wikipedia.set_lang('ru')
        bot.send_message(message.from_user.id, wikipedia.summary(str(message.text)))
    except Exception:
        return 'Не удалось найти'

if __name__ == '__main__':
    bot.infinity_polling()
