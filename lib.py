from solana.rpc.api import Client
from theblockchainapi import TheBlockchainAPIResource, SolanaNetwork
import requests
import json


class SolEnd:
    def __init__(self):
        self.addr_to_nick = {}
        self.BLOCKCHAIN_API_RESOURCE = TheBlockchainAPIResource(
            api_key_id="F82PeTn9k4CM1SW"
            ,
            api_secret_key="3xqbgM0fQaCHaNZ"
        )

    def connect(self):
        server = "https://solana-mainnet.phantom.tech"
        client = Client(server)
        return client

    def balance(self, address, client):
        print(client.get_balance(address))

    def registration(self, pub_key, nickname):
        self.addr_to_nick[nickname] = pub_key
        return self.addr_to_nick

    # def tokens(self, address):
    #     address_of_tokkens = []
    #     link = f'https://public-api.solscan.io/account/tokens?account={address}'
    #     res = requests.get(link).json()
    #
    #     for t in res:
    #         address_of_tokkens.append(t['tokenAddress'])
    #
    #     return address_of_tokkens

    def get_tokens(self, address):
        address_of_tokens = []
        link = f'https://public-api.solscan.io/account/tokens?account={address}'
        res = requests.get(link).json()

        for tokens in res:
            address_of_tokens.append(tokens['tokenAddress'])

        return address_of_tokens

    def get_nft_metadata(self, nft_address):
        nft_metadata = self.BLOCKCHAIN_API_RESOURCE.get_nft_metadata(
            mint_address=nft_address,
            network=SolanaNetwork.MAINNET_BETA
        )
        return nft_metadata

    def get_uri_token(self, nft_metadata):
        uri_token = nft_metadata['data']['uri']
        return uri_token

    def request_img(self, uri_token):
        img = requests.get(uri_token).json()['image']
        return img


if __name__ == "__main__":
    address = '2qfcgEjCZvYZgDrcFY6qEcbhF1nSJuujHNMGpirpWVnB'
    print(SolEnd().req(address))
