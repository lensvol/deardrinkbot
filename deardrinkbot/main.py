# -*- coding: utf-8 -*-

from bottle import request, route, run
import os
import re
import random
import telegram
import yaml


# Загружаем ответы из внешнего файла, если такой указан и существует
REPLIES = {}
replies_fn = os.environ.get('REPLIES_YAML', 'replies.yaml')
if os.path.exists(replies_fn):
    with open(replies_fn, 'r') as fp:
        REPLIES = yaml.safe_load(fp.read())

# Инициализируем бота
bot_token = os.environ.get('BOT_TOKEN', None)
if not bot_token:
    raise ValueError("No token found!")
bot = telegram.Bot(token=bot_token)

def replace_emoji_code(m):
    code = m.group(1)
    return getattr(telegram.Emoji, code.upper(), code)


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

        reply = REPLIES.get(
            unicode(message),
            u'Дорогая, выпей вина! :wine_glass:',
        )
        if isinstance(reply, list):
            reply = random.choice(reply)
        reply = re.sub(':([a-z_]+):', replace_emoji_code, reply.encode('utf-8'))

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
