import sys
import time
import datetime
import telepot
import os
import requests
import json

def get_price(chat_id):
    url = "https://api.blockchain.com/v3/exchange/l2/BTC-USD"
    r = requests.get(url)
    data = r.json()
    print(data)
    top_bid = data["bids"]
    head = top_bid[0]
    price = str(head["px"])
    print(price)
    #bot.sendMessage(chat_id, "BTC-USD top bid: " + price)

def get_price_blockchain_info(chat_id):
    url = "https://blockchain.info/ticker"
    r = requests.get(url)
    data = r.json()
    print(data)
    usd = data["USD"]["buy"]
    print(usd)


if __name__ == "__main__":
#    get_price(1)
    get_price_blockchain_info(1)
