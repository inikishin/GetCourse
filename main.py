import telebot

from extensions import APIException, ExRatesAPI
from config import cur_list, telbot_token


bot = telebot.TeleBot(telbot_token)

@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id,
                     f"Привет, {message.chat.username}! \nДля того чтобы воспользоваться ботом необходимо отправить "
                     f"сообщение в виде <имя валюты, цену которой нужно узнать> <имя валюты, в которой надо узнать "
                     f"цену первой валюты> <количество первой валюты>. Для получения списка доступных валют введите команду /values")

@bot.message_handler(commands=['values'])
def values(message):
    bot.send_message(message.chat.id, 'Доступные валюты:\n' + '\n'.join(cur_list.keys()))

@bot.message_handler(content_types=['text'])
def convert(message):
    mgs_base = message.text.split(' ')[0]
    mgs_quote = message.text.split(' ')[1]
    try:
        mgs_amount = float(message.text.split(' ')[2])
    except ValueError:
        bot.send_message(message.chat.id, 'Количество введено некорректно')
        raise APIException(f'Количество введено некорректно')
        return

    if mgs_base not in cur_list.keys():
        bot.send_message(message.chat.id, 'Базовая валюта не входит в список доступных элементов')
        raise APIException(f'Базовая валюта не входит в список доступных элементов')
        return

    if mgs_quote not in cur_list.keys():
        bot.send_message(message.chat.id, 'Проверяемая валюта не входит в список доступных элементов')
        raise APIException(f'Проверяемая валюта не входит в список доступных элементов')
        return

    bot.reply_to(message, ExRatesAPI.get_price(cur_list[mgs_base], cur_list[mgs_quote], mgs_amount))

bot.polling(none_stop=True)