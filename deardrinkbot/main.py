# -*- coding: utf-8 -*-

from bottle import request, route, run
import os
import telegram


REPLIES = {
    u'привет': u'Привет!',
    u'пока': u'До встречи. :)',
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
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        bot.sendMessage(
            chat_id=chat_id,
            text=REPLIES.get(message, 'Дорогая, выпей вина! ' + telegram.Emoji.WINE_GLASS),
        )

    return 'ok'


@route('/')
def index():
    return '42'


run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
