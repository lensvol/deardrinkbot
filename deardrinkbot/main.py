# -*- coding: utf-8 -*-

from bottle import request, route, run
import os
import random
import telegram


REPLIES = {
    u'привет': [
        u'Привет!',
        u'Здравствуй!',
        u'Рада тебя слышать. :)',
        u'О! Кого я вижу :) Как у тебя дела?',
    ],
    u'пока': [
        u'До встречи. :)',
        u'Ты пиши, если что. :)',
        u'Успехов! :)',
        u'Всегда приятно тебя читать. :)',
    ],
}


bot_token = os.environ.get('BOT_TOKEN', None)
if not bot_token:
    raise ValueError("No token found!")
bot = telegram.Bot(token=bot_token)


@route('/bot', method='POST')
def webhook_handler():
    update = telegram.Update.de_json(request.json)
    chat_id = update.message.chat_id
    message = update.message.text.strip('!., ').lower()

    if message:
        print '(%d) [%s] %s {{ %s }}' % (
            chat_id,
            update.message.from_user.name.encode('utf-8'),
            update.message.text.encode('utf-8'),
            message.encode('utf-8'),
        )

        reply = REPLIES.get(message, 'Дорогая, выпей вина! ' + telegram.Emoji.WINE_GLASS)
        if isinstance(reply, list):
            reply = random.choice(reply)

        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        bot.sendMessage(
            chat_id=chat_id,
            text=reply,
        )

    return 'ok'


@route('/')
def index():
    return '42'


run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
