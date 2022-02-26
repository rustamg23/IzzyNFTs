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
    usersProfile[message.from_user.username] = {"reg": false}


@App.on_message(filters.command('reg'))
def reg(client, message):
    rega = back.registration(message.text[5:], message.from_user.username)
    print(rega)
    if(len(message.text) > 10):
        message.reply("Registration succesful. Now you can use '/my_...' bot functions.\nuse /help for more information")
    else:
        message.reply("Call /reg command again with your publicKey")


@App.on_message(filters.command('my_balance'))
def raw(client, message):
    bal = back.balance(back.addr_to_nick[message.from_user.username], back.connect())
    print(bal)
    new_bal = bal["result"]["value"]
    new_bal /= 1000000000
    print(new_bal)
    message.reply(str(new_bal) + ' SOL')


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


@App.on_message(filters.command('show_balance'))
def raw(client, message):
    bal = back.balance((message.text)[14:], back.connect())
    print(bal)
    new_bal = bal["result"]["value"]
    new_bal /= 1000000000
    print(new_bal)
    message.reply(str(new_bal) + ' SOL')


@App.on_message(filters.command('show_collection'))
def drop(client, message):
    wallet = (message.text)[17:]
    print(wallet)
    for address in back.get_tokens(wallet):
        try:
            metadata = back.get_nft_metadata(address)
            uri = back.get_uri_token(metadata)
            App.send_photo(message.chat.id, back.request_img(uri), caption=back.request_data(uri))
        except:
            print(address)

@App.on_message(filters.command('help'))
def helper(client, message):
    message.reply(
        "This bot helps you to surf and trade Solana NFTs:\n"\
        "/reg + publicKey - registrate your public address, so you dont need to paste it later\n"\
        "/my_collection - shows your NFTs with names and descriptions\n"\
        "/my_balance - shows your SOL balance\n"\
        "/show_collection + user_publicKey - shows user NFTs with names and descriptions\n"\
        "/show_balance + user_publicKey - shows user SOL balance"
    )

App.run()  # Automatically start() and idle()
