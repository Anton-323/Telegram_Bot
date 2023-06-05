import telebot
from config import keys,TOKEN
from utils import ConversionException,CryptoConventer 

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n<имя валюты> \
<в какую валюты перевести> \
<кол-во переводимой валюты>\n Увидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands= ['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try: 
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConversionException('Слишком много параметров')
        
        
        quoats, base, amount = values 
        total_base = CryptoConventer.convert(quoats, base, amount)
    except ConversionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Бот не может обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quoats} в {base} будет равна {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()