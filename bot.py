# -*- coding: utf-8 -*-
# Configuration
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import apiai, json
updater = Updater(token="")
dispatcher = updater.dispatcher


# Обработка команд
def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?')


def helpCommand(bot, update):
    bot.send_message(chat_id=update.mesaage.chat_id, text='/say - сказать боту\n/google - заставить бота гуглить\n/help - помощь по командам')


def textMessage(bot, update):
    request = apiai.ApiAI('bcb7567f6c2b415a9ed95496a3ea8b0b').text_request() # Dialogflow api token
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'bulbo4kabot' # ID сессии диалога (нужно чтобы потом учить бота)
    request.query = update.message.text # Посылаем запрос к ИИ с обращением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
    # Если есть ответ от бота - пересылаем юзеру, если нет - бот его не понял
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Я не совсем понял что от меня ты хочешь!')


# Хендлеры
start_command_handler = CommandHandler('start', startCommand)
help_command_handler = CommandHandler('help', helpCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)
# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(help_command_handler)
dispatcher.add_handler(text_message_handler)
# Начинаем поиск обновлений
updater.start_polling(clean=True)
# Останавливаем бота, если нажаты Ctrl + C
updater.idle()
