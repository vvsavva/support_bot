import sqlite3
import threading
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContext, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import config
TOKEN = config.TOKEN

GROUP_CHAT_ID = config.GROUP_CHAT_ID

conn = sqlite3.connect('userpuser.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS userpuser (
        user_id INTEGER,
        message_id INTEGER,
        reply_message_id INTEGER,
        is_blocked INTEGER DEFAULT 0
    )
''')
conn.commit()

db_lock = threading.Lock()

def start(update, context):
    update.message.reply_text(config.hi)

def forward_to_admins(update, context):
    user_id = update.message.chat_id
    member = update.message.from_user.username
    conn = sqlite3.connect('userpuser.db')
    cursor = conn.cursor()
    cursor.execute("SELECT is_blocked FROM userpuser WHERE user_id=?", (user_id,))
    is_blocked = cursor.fetchone()
    conn.close()

    if is_blocked and is_blocked[0] == 1:
        update.message.reply_text("Вы заблокированы и не можете отправлять сообщения администраторам.")
    else:
        sent_message = None
        keyboard = [[InlineKeyboardButton("Заблокировать пользователя", callback_data=f'block_{user_id}')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.message.text:
            sent_message = context.bot.send_message(GROUP_CHAT_ID, f'Пользователь {user_id},{member} написал:\n{update.message.text}', reply_markup=reply_markup)
        elif update.message.photo:
            photo = update.message.photo[-1] 
            context.bot.send_photo(GROUP_CHAT_ID, photo.file_id, caption=f'Пользователь {user_id}, {member}: Подпись {update.message.caption}')
        elif update.message.audio:
            audio = update.message.audio
            sent_message = context.bot.send_audio(GROUP_CHAT_ID, audio.file_id, caption=f'Пользователь {user_id},{member}: Подпись {update.message.caption}', reply_markup=reply_markup)
        elif update.message.document:
            file = update.message.document
            if file.mime_type == "audio/mpeg":
                sent_message = context.bot.send_audio(GROUP_CHAT_ID, file.file_id, caption=f'Пользователь {user_id},{member}: Подпись {update.message.caption}', reply_markup=reply_markup)
            else:
                sent_message = context.bot.send_document(GROUP_CHAT_ID, file.file_id, caption=f'Пользователь {user_id},{member}: Подпись {update.message.caption}', reply_markup=reply_markup)
        elif update.message.video:
            sent_message = context.bot.send_video(GROUP_CHAT_ID, update.message.video.file_id, caption=f'Пользователь {user_id},{member}: Подпись {update.message.caption}', reply_markup=reply_markup)
        elif update.message.voice:
            sent_message = context.bot.send_voice(GROUP_CHAT_ID, update.message.voice.file_id, caption=f'Пользователь {user_id},{member}: Подпись {update.message.caption}', reply_markup=reply_markup)

        if sent_message:
            conn = sqlite3.connect('userpuser.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO userpuser (user_id, message_id, reply_message_id) VALUES (?, ?, ?)", (user_id, update.message.message_id, sent_message.message_id))
            conn.commit()
            conn.close()



def reply_to_user(update, context):
    admin_message = update.message.text
    reply_message = update.message.reply_to_message
    reply_message_id = reply_message.message_id
    message_id = update.message.message_id
    conn = sqlite3.connect('userpuser.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM userpuser WHERE reply_message_id=?", (reply_message_id,))
    user_id = cursor.fetchone()
    conn.close()

    if user_id:
        user_id = user_id[0]
        context.bot.copy_message(user_id, GROUP_CHAT_ID, message_id, disable_notification=True)
def id(update, context):
    sas = update.message.chat_id
    print(sas)


def button_callback(update, context):
    query = update.callback_query
    data = query.data

    if data.startswith('block_'):
        user_id = int(data.split('_')[1])

        conn = sqlite3.connect('userpuser.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE userpuser SET is_blocked=1 WHERE user_id=?", (user_id,))
        conn.commit()
        conn.close()
        query.answer("Пользователь заблокирован.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('id', id))

    dp.add_handler(MessageHandler(Filters.private & Filters.all, forward_to_admins))

    dp.add_handler(MessageHandler(Filters.chat(chat_id=GROUP_CHAT_ID) & Filters.reply, reply_to_user))

    dp.add_handler(CallbackQueryHandler(button_callback))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()