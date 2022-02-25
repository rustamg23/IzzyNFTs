from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent,
                            InlineKeyboardMarkup, InlineKeyboardButton)
from lib import SolEnd

API_ID = 12345
API_HASH = "0123456789abcdef0123456789abcdef"
BOT_TOKEN = ""
App = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@App.on_message(filters.command('start'))
def start(client, message):
    message.reply('This is /start command', reply_markup=ReplyKeyboardMarkup(
        [
            ["My collection", "Balance", "C", "D"]
        ],
        resize_keyboard=True  # Make the keyboard smaller
    ))
    print('This is /start command')


@App.on_message(filters.command('parsing'))
def pars(client, message):
    markup = InlineKeyboardMarkup(
        [
            [  # First row
                InlineKeyboardButton(  # Generates a callback query when pressed
                    "Button",
                    callback_data="airdrop"
                ),
                InlineKeyboardButton(  # Opens a web URL
                    "URL",
                    url="https://docs.pyrogram.org"
                ),
            ],
            [  # Second row
                InlineKeyboardButton(  # Opens the inline interface
                    "Choose chat",
                    switch_inline_query="pyrogram"
                ),
                InlineKeyboardButton(  # Opens the inline interface in the current chat
                    "Inline here",
                    switch_inline_query_current_chat="pyrogram"
                )
            ]
        ]
    )
    message.reply('This is /start command', reply_markup=markup)


@App.on_message(filters.command('airdrop'))
def drop(client, message):
    message.reply('Airdrop finished')
    message.answer(
        results=[
            InlineQueryResultArticle(
                title="Installation",
                input_message_content=InputTextMessageContent(
                    "Here's how to install **Pyrogram**"
                ),
                url="https://docs.pyrogram.org/intro/install",
                description="How to install Pyrogram",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(
                            "Open website",
                            url="https://docs.pyrogram.org/intro/install"
                        )]
                    ]
                )
            ),
            InlineQueryResultArticle(
                title="Usage",
                input_message_content=InputTextMessageContent(
                    "Here's how to use **Pyrogram**"
                ),
                url="https://docs.pyrogram.org/start/invoking",
                description="How to use Pyrogram",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(
                            "Open website",
                            url="https://docs.pyrogram.org/start/invoking"
                        )]
                    ]
                )
            )
        ],
        cache_time=1
    )
    print('Airdrop finished. ')


@App.on_message(filters.command('my_collection'))
def drop(client, message):
    wallet = '2HPJbkWbe4UzfemHp8WvwQXw7C9E34N8eNWaxDSGQGxM'
    for address in SolEnd().get_tokens(wallet):
        try:
            metadata = SolEnd().get_nft_metadata(address)
            uri = SolEnd().get_uri_token(metadata)
            App.send_photo(message.chat.id, SolEnd().request_img(uri))
        except:
            print(address)


@App.on_message(filters.command('/'))
def raw(client, message):
    message.reply('This is message')
    print('This is message')


App.run()  # Automatically start() and idle()
