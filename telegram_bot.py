import telebot
import requests
import json
import tkn


bot = telebot.TeleBot(tkn.my_token)

# Словарь доступных валют
keys = {'биткоин': 'BTC',
        'эфириум': 'ETH',
        'доллар': 'USD',
        'евро': 'EUR',
        'рубль': 'RUB'}



class APIException(Exception):
    pass


# Действие на команду /start
@bot.message_handler(commands=['start', ])
def send_welcome(message: telebot.types.Message):
    text = f'Приветствую тебя, {message.chat.first_name}!\n' \
           f'Я чат-бот Investor.\n' \
           f'Я конвертирую валюты.\n' \
           f'Для дополнительной информации\n' \
           f'отправь команду:  /help'
    bot.reply_to(message, text)


# Действие на команду /value
@bot.message_handler(commands=['value', ])
def send_help(message: telebot.types.Message):
    text = f'Доступные валюты:\n' \
           f' Биткоин\n' \
           f' Эфириум\n' \
           f' Рубль\n' \
           f' Доллар\n' \
           f' Евро'
    bot.reply_to(message, text)

# Действие на команду /help
@bot.message_handler(commands=['help', ])
def send_help(message: telebot.types.Message):
    text = f'Помощь по Telegram-bot:\n' \
           f'отправьте текст типа:\n' \
           f'доллар рубль 1\n' \
           f'\n' \
           f'Информация о доступных валютах\n' \
           f'по ссылке:  /value'
    bot.reply_to(message, text)

# Конвертация валюты
@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        # Проверка все ли значения введены
        if len(values) != 3:
            raise APIException()
    except APIException:
        bot.reply_to(message, f'Некорректные данные\nпопробуйте ещё раз!')
    else:
        quote, base, amount = values
        try:
            # Проверка наличия валюты для конвертации
            if quote not in keys or base not in keys:
                raise APIException()
        except APIException:
            bot.reply_to(message, f'Где-то ошибка!')
        else:
            try:
                if not (amount.isdigit()):
                    raise APIException()
            except APIException:
                bot.reply_to(message, f'Неверное количество конвертируемой валюты!\n'
                                      f'Будьте внимательны!')
            else:

                r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[quote]}&tsyms={keys[base]}')
                total_base = json.loads(r.content)[keys[base]]
                text = f'Цена {amount} {quote}: {round(float(total_base*float(amount)), 2)} {base}.'
                bot.send_message(message.chat.id, text)

print(f'Telegram-bot is started!!!')
bot.polling(none_stop=True)