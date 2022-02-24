from pyrogram import Client, filters


API_ID = 12345
API_HASH = ""
BOT_TOKEN = ""
App = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@App.on_message(filters.command('start'))
def raw(client, message):
    message.reply('This is /start command')
    print('This is /start command')


@App.on_message(filters.command('parsing'))
def raw(client, message):
    print(f'Parsing completed. The number of TrustLines:')


@App.on_message(filters.command('airdrop'))
def raw(client, message):

    print('Airdrop finished. ')


@App.on_message(filters.command('/'))
def raw(client, message):
    message.reply('This is message')
    print('This is message')


App.run()  # Automatically start() and idle()
