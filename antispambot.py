import telegram
from telegram.ext import Updater, MessageHandler, Filters

# Set up Telegram bot
bot_token = 'YOUR_BOT_TOKEN_HERE'
bot_chatID = 'YOUR_CHAT_ID_HERE'
bot = telegram.Bot(token=bot_token)

# Set up Updater and dispatcher
updater = Updater(bot_token, use_context=True)
dispatcher = updater.dispatcher

# Define spam detection function
def spam_detector(update, context):
    message = update.message
    chat_id = message.chat_id
    user_id = message.from_user.id
    text = message.text

    # Check if message is from a chat or channel
    if message.chat.type == 'group' or message.chat.type == 'supergroup' or message.chat.type == 'channel':
        # Check if message contains a URL
        if 'http' in text:
            bot.kick_chat_member(chat_id=chat_id, user_id=user_id)
            bot.send_message(chat_id=chat_id, text=f'User {user_id} has been kicked for sending a URL.')
        # Check if message is too long
        elif len(text) > 1000:
            bot.delete_message(chat_id=chat_id, message_id=message.message_id)
            bot.kick_chat_member(chat_id=chat_id, user_id=user_id)
            bot.send_message(chat_id=chat_id, text=f'User {user_id} has been kicked for sending a message that is too long.')

# Add spam detector handler to dispatcher
dispatcher.add_handler(MessageHandler(Filters.text, spam_detector))

# Start polling for updates
updater.start_polling()
updater.idle()
