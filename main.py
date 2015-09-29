# -*- coding: utf-8 -*-

import telegram
import sys

REPLIES = {
    u'привет': u'Привет!',
    u'пока': u'До встречи. :)',
}

if __name__ == '__main__':
    bot = telegram.Bot(token=sys.argv[1])

    last_update_id = 1

    while True:
        for update in bot.getUpdates(offset=last_update_id, timeout=5):
            chat_id = update.message.chat_id
            message = update.message.text.strip('!., ').lower()

            if message:
                print u'(%d) [%s] %s {{ %s }}' % (
                    chat_id,
                    update.message.from_user.name,
                    update.message.text,
                    message,
                )
                bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
                bot.sendMessage(
                    chat_id=chat_id,
                    text=REPLIES.get(message, 'Дорогая, выпей вина! ' + telegram.Emoji.WINE_GLASS),
                )
                last_update_id = update.update_id + 1
