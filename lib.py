from solana.rpc.api import Client
import requests
import json


def connect():
    server = "https://solana-mainnet.phantom.tech"
    client = Client(server)
    return client


def balance(address, client):
    print(client.get_balance(address))


def registration(pub_key, nickname):
    add_to_nick = {}
    add_to_nick[nickname] = pub_key
    return add_to_nick


def tokens(address):
    address_of_tokkens = []
    link = f'https://public-api.solscan.io/account/tokens?account={address}'
    res = requests.get(link).json()

    for t in res:
        address_of_tokkens.append(t['tokenAddress'])

    return address_of_tokkens


if name == "main":
    address = '2HPJbkWbe4UzfemHp8WvwQXw7C9E34N8eNWaxDSGQGxM'
    print(tokens(address))
