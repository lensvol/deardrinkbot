# -*- coding: utf-8 -*-

from bottle import request, route, run
import os
import re
import random
import readline
import sys
import telegram
import yaml


# Загружаем ответы из внешнего файла, если такой указан и существует
RESPONSES = {}
replies_fn = os.environ.get('REPLIES_YAML', 'replies.yaml')
if os.path.exists(replies_fn):
    with open(replies_fn, 'r') as fp:
        RESPONSES = yaml.safe_load(fp.read())

# Инициализируем бота
bot_token = os.environ.get('BOT_TOKEN', None)
if not bot_token:
    raise ValueError("No token found!")
bot = telegram.Bot(token=bot_token)


def replace_emoji_code(m):
    code = m.group(1)
    return getattr(telegram.Emoji, code.upper(), code)


def find_reply(message_text, replies_dict):
    message = message_text.strip('!., ').lower()
    reply = replies_dict.get(
        unicode(message_text),
        u'Дорогая, выпей вина! :wine_glass:',
    )
    if isinstance(reply, list):
        reply = random.choice(reply)
    return re.sub(':([a-z_]+):', replace_emoji_code, reply.encode('utf-8'))


def test_replies(replies_dict):
    while True:
        line = raw_input('> ')
        if line == '':
            break
        print find_reply(line.decode('utf-8'), replies_dict)


@route('/bot', method='POST')
def webhook_handler():
    update = telegram.Update.de_json(request.json)
    chat_id = update.message.chat_id

    if message:
        print '(%d) [%s] %s {{ %s }}' % (
            chat_id,
            update.message.from_user.name.encode('utf-8'),
            update.message.text.encode('utf-8'),
            message.encode('utf-8'),
        )

        reply = find_reply(update.message.text, RESPONSES)
        bot.sendChatAction(
            chat_id=chat_id,
            action=telegram.ChatAction.TYPING,
        )
        bot.sendMessage(
            chat_id=chat_id,
            text=reply,
        )
    return 'ok'


@route('/')
def index():
    return '42'


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        test_replies(RESPONSES)
    else:
        run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
