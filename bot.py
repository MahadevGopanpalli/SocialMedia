from telegram.ext import Updater,CommandHandler,MessageHandler,Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging
import time
import sys


updater = Updater(token='1138454208:AAEwugvq0GOt9KLXL1qilsMFEzSiu2rRG0s', use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

print("VK")

def option1(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,text="This is Option 1")


def option2(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,text="This is Option 2")


def option3(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,text="This is Option 3")




def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to bot ")
    keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
             InlineKeyboardButton("Option 2", callback_data='2')],
          [InlineKeyboardButton("Option 3", callback_data='3')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")



start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

dispatcher.add_handler(CallbackQueryHandler(option1, pattern='1'))
dispatcher.add_handler(CallbackQueryHandler(option2, pattern='2'))
dispatcher.add_handler(CallbackQueryHandler(option3, pattern='3'))


unknown_handler = MessageHandler(Filters.text, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()
updater.idle()

time.sleep(100)
sys.exit()