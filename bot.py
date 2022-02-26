import re
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton)
from lib import SolEnd

API_ID = 16100063
API_HASH = "d49d1061fe9e26956314572ad0586265"
BOT_TOKEN = ""
App = Client("SolgramWalletBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


back = SolEnd()
@App.on_message(filters.command('start'))
def start(client, message):
    message.reply('This is /start command', reply_markup=ReplyKeyboardMarkup(
        [
            ["My collection", "Balance", "C", "D"]
        ],
        resize_keyboard=True  # Make the keyboard smaller
    ))
    print('This is /start command')


@App.on_message(filters.command('my_collection'))
def drop(client, message):
    wallet = back.addr_to_nick[message.from_user.username]
    print(wallet)
    for address in back.get_tokens(wallet):
        try:
            metadata = back.get_nft_metadata(address)
            uri = back.get_uri_token(metadata)
            App.send_photo(message.chat.id, back.request_img(uri), caption=back.request_data(uri))
        except:
            print(address)


@App.on_message(filters.command('reg'))
def reg(client, message):
    rega = back.registration(message.text[5:], message.from_user.username)
    print(rega)
    message.reply("Registration succesful. Now you can use bot functions.\nuse /help for more information")


@App.on_message(filters.command('my_balance'))
def raw(client, message):
    bal = back.balance(back.addr_to_nick[message.from_user.username], back.connect())
    print(bal)
    new_bal = bal["result"]["value"]
    new_bal /= 1000000000
    print(new_bal)
    message.reply(str(new_bal) + ' SOL')


App.run()  # Automatically start() and idle()
