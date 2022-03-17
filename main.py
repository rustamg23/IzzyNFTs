from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup,
                            InlineKeyboardButton)
from lib import SolEnd

# devnet1 CBXTEvYqLZtBGSWwJcD7w7oCPGdR38TGmv8yAM3gQ1qL
# devnet2 9Rfo6MyLtpka9SzxqbQEWYEyaRvXRMJzt9Npo1mg9skX
# mainnet1 H2hFezqB6JNVUixUMttJogFr3KvhTDX4bLvT8Rq4eJwW
# mainnet2 AddjSTX6VdJCgp2B36ioVnyHw57sSjqfewiBXYywwEoc

API_ID = 10187665
API_HASH = "f8113bc0748601e3989acd415971b259"
BOT_TOKEN = " " #token of bot
App = Client("SolgramWalletBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
back = SolEnd(network='main')    # for mainnet: network='main', for devnet: network='dev' or nothing


@App.on_message(filters.command('start'))
def start(client, message):
    back.users_profile[message.from_user.username] = {'input_flag': False}
    text = f'Hey! Welcome to IZZY NFTS bot. ' \
           f'We allow you to view and buy NFTs conveniently and quickly right on Telegram.' \
           f'You need to connect your wallet to make the most use out of our application.' \
           f' Please, share your public key and we’ll connect it to your Telegram ID.'

    message.reply(text, reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    'Registration',
                    callback_data='registration'
                ),
                InlineKeyboardButton(
                    'Skip',
                    callback_data='menu'
                )
            ]
        ]
    ))


@App.on_callback_query()
def start(client, query):
    if query['data'] == 'menu':
        App.send_message(query.from_user.username, 'Selection function', reply_markup=ReplyKeyboardMarkup(
            [
                ["/my_collection", "/my_balance", "/my_bids"],
                ["/show_collection", "/show_balance"]
            ],
            resize_keyboard=True  # Make the keyboard smaller
        ))
    elif query['data'] == 'registration':
        back.users_profile[query.from_user.username]['input_flag'] = True
        back.users_profile[query.from_user.username]['func_data'] = 'registration'
        App.send_message(query.from_user.username, 'Please input your public key:')
    elif query['data'] == 'bid':
        # must colling function bid from object of SolEnd() from lib
        App.send_message(query.from_user.username, 'Go on, name your price 😏.')



@App.on_message(filters.command('my_balance'))
def my_balance(client, message):
    bal = back.balance(back.addr_to_nick[message.from_user.username])["result"]["value"]
    norm_bal = round(bal / 1000000000, 2)
    sol_bal = round((norm_bal * back.price_in_usdt()), 2)
    message.reply(f'{norm_bal} SOL = {sol_bal} USD')
    print(f'{norm_bal} SOL / {sol_bal} USDT')


@App.on_message(filters.command('my_collection'))
def my_collection(client, message):
    wallet = back.addr_to_nick[message.from_user.username]
    print(f'{message.from_user.username}: {wallet}')

    addresses = back.get_tokens(wallet)
    if len(addresses) <= 0:
        message.reply("You don't have NFTs.")
    else:
        for address in back.get_tokens(wallet):
            metadata = back.get_nft_metadata(address)
            try:
                uri = back.get_uri_token(metadata)
                App.send_photo(message.from_user.username,
                               back.request_img(uri),
                               caption=back.request_data(uri))
            except:
                print(address)


@App.on_message(filters.command('show_balance'))
def show_balance(client, message):
    back.users_profile[message.from_user.username]['input_flag'] = True
    back.users_profile[message.from_user.username]['func_data'] = {
        'func_name': "show_balance",
        'chat_id': str(message.chat.id)
    }
    print(message.chat.id)
    message.reply("Please input their public key or username:")


@App.on_message(filters.command('show_collection'))
def show_collection(client, message):
    back.users_profile[message.from_user.username]['input_flag'] = True
    back.users_profile[message.from_user.username]['func_data'] = {
        'func_name': "show_collection",
        'chat_id': str(message.chat.id)
    }
    print(message.chat.id)
    message.reply("Please input their public key or username:")


@App.on_message(filters.command('help'))
def helper(client, message):
    message.reply(
        "This bot helps you to surf and trade Solana NFTs:\n"
        "/reg + publicKey - registrate your public address, so you don't need to paste it later\n"
        "/my_collection - shows your NFTs with names and descriptions\n"
        "/my_balance - shows your SOL balance\n"
        "/show_collection + user_publicKey - shows user NFTs with names and descriptions\n"
        "/show_balance + user_publicKey - shows user SOL balance"
    )


@App.on_callback_query()
def bind(client, query):
    data = query["data"]
    back.bind(query.from_user.username, data[1]["holder"], data[1]["nft_address"])
    App.send_message("Offer your price (bid). It will be shared with the owner. "
                     "If approved, you will be charged and become the owner immediately.")


@App.on_message()
def other(client, message):
    user = message.from_user.username
    # chat_id = back.users_profile[user]['func_data']['chat_id']
    chat_id = user

    if back.users_profile[user]['input_flag'] and \
            back.users_profile[user]['func_data'] == "registration":

        back.users_profile[user]['input_flag'] = False
        back.addr_to_nick[user] = message.text
        print(back.addr_to_nick)

        App.send_message(
            chat_id,
            "Registration succesful. Now you can use IzzyNFTs bot."
            "Use /help for more information",
            reply_markup=ReplyKeyboardMarkup(
                [
                    ["/my_collection", "/my_balance", "/my_bids"],
                    ["/show_collection", "/show_balance"]
                ],
                resize_keyboard=True
            )
        )

    elif back.users_profile[user]['input_flag'] and \
            back.users_profile[user]['func_data']['func_name'] == "show_collection":

        back.users_profile[user]['input_flag'] = False
        mess = message.text
        if mess[0] == '@':
            wallet = back.addr_to_nick[mess[1:]]
        else:
            wallet = message.text

        token_addresses = back.get_tokens(wallet)

        if len(token_addresses) <= 0:
            App.send_message(chat_id, "This user does not have any NFTs.")
        else:

            if len(token_addresses) == 1:
                App.send_message(user, f'There is {len(token_addresses)} NFT in this wallet :)')
            elif len(token_addresses) > 1:
                App.send_message(user, f'There are {len(token_addresses)} NFTs in this wallet :)')

            for address in token_addresses:
                keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                'Buy',
                                callback_data='buy'
                            ),
                            InlineKeyboardButton(
                                'Bid',
                                callback_data='bid'
                            )
                        ]
                    ]
                )


                try:
                    metadata = back.get_nft_metadata(address)
                    uri = back.get_uri_token(metadata)
                    App.send_photo(
                        chat_id=user,
                        photo=back.request_img(uri),
                        caption=back.request_data(uri),
                        reply_markup=keyboard)
                except:
                    print(address)

            App.send_message(user, 'That\'s it. The entire collection^^.')

    elif back.users_profile[user]['input_flag'] and \
            back.users_profile[user]['func_data']['func_name'] == "show_balance":

        back.users_profile[user]['input_flag'] = False
        mess = message.text
        if mess[0] == '@':
            wallet = back.addr_to_nick[mess[1:]]
        else:
            wallet = message.text
        print(wallet)

        bal = back.balance(wallet)
        new_bal = bal["result"]["value"]
        new_bal = round(new_bal / 1000000000, 2)
        sol_bal = round((new_bal * back.price_in_usdt()), 2)
        print(f'{new_bal} SOL / {sol_bal} USDT')
        message.reply(f'{new_bal} SOL = {sol_bal} USD')  #

    else:
        App.send_message(chat_id, "Sorry, but I don`t know this command. ")


App.run()
