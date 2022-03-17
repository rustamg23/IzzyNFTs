from solana.rpc.api import Client
from theblockchainapi import TheBlockchainAPIResource, SolanaNetwork
import requests


class SolEnd:
    def __init__(self, network='dev'):

        if network == 'dev':
            self.client = Client("https://api.devnet.solana.com/")
            self.network = 'devnet'
        elif network == 'main':
            self.client = Client("https://solana-mainnet.phantom.tech")
            self.network = 'mainnet'
        else:
            self.client = Client("https://api.devnet.solana.com/")
            self.network = 'devnet'
            print('This network mode does not exist!')

        print(f'You work in {self.network}')

        self.addr_to_nick = {}
        self.BLOCKCHAIN_API_RESOURCE = TheBlockchainAPIResource(
            # you need to create on this site https://dashboard.blockchainapi.com/#contact
            api_key_id="9spRKqC0GgLYLpL",
            api_secret_key="f573q7V4fMi3abC"
        )
        self.users_profile = {}

    def balance(self, address):
        return self.client.get_balance(address)

    def price_in_usdt(self):
        link_sol = 'https://public-api.solscan.io/market/token/So11111111111111111111111111111111111111112'
        res = requests.get(link_sol).json()
        return res["priceUsdt"]

    def registration(self, pub_key, nickname):
        self.addr_to_nick[nickname] = pub_key
        return self.addr_to_nick

    def get_tokens(self, wallet_address):
        if self.network == 'devnet':
            link = f'https://api-devnet.solscan.io/account/tokens?address={wallet_address}'
            res = requests.get(link).json()['data']
        elif self.network == 'mainnet':
            link = f'https://public-api.solscan.io/account/tokens?account={wallet_address}'
            res = requests.get(link).json()

        addr_of_tokens = [tokens['tokenAddress'] for tokens in res]

        # for tokens in res:
        #     addr_of_tokens.append(tokens['tokenAddress'])
        return addr_of_tokens

    def get_nft_metadata(self, nft_address):
        if self.network == 'devnet':
            network = SolanaNetwork.DEVNET
        elif self.network == 'mainnet':
            network = SolanaNetwork.MAINNET_BETA

        nft_metadata = self.BLOCKCHAIN_API_RESOURCE.get_nft_metadata(
            mint_address=nft_address,
            network=network
        )
        return nft_metadata

    def get_uri_token(self, nft_metadata):
        uri_token = nft_metadata['data']['uri']
        return uri_token

    def request_img(self, uri_token):
        img = requests.get(uri_token).json()['image']
        return img

    def request_data(seld, uri_token):
        name = requests.get(uri_token).json()["name"]
        info = requests.get(uri_token).json()["description"]
        res = f'{name} \n{info}' \
              f'\n- - - - - - - - - - - - - - - -' \
              f' - - - - - - - - - - - - - - - - \n' \
              f'price is not set, people can offer bids, or you can set the price now.'

        return res

    def bid(self, binder: str, holder: str, nft_address: str):
        self.users_profile[holder] = {"token": nft_address,
                                      "binder": binder}


if __name__ == "__main__":
    address = 'H2hFezqB6JNVUixUMttJogFr3KvhTDX4bLvT8Rq4eJwW'
    print(SolEnd().req(address))
