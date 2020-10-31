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
    top_bid = data["bids"]
    head = top_bid[0]
    price = str(head["px"])
    bot.sendMessage(chat_id, "BTC-USD top bid: " + price)

def get_pi(chat_id):
    f = open("/tmp/addr", "r")
    addr = f.read()
    if not addr:
        bot.sendMessage(chat_id, "No address file - use /refresh to refresh address")
    else:
        bot.sendMessage(chat_id, "Address: " + addr)
    f.close()

def refresh_addr(chat_id):
    os.system("/sbin/ifconfig > /tmp/addr")# | grep 'inet ' | grep -v 127.0.0.1 > /tmp/addr")
    os.system("chmod 750 /tmp/addr")
    bot.sendMessage(chat_id, "Address file refreshed - use /ip to get info")
    
def ping(chat_id):
    bot.sendMessage(chat_id, "PiPing")

def telepot_id(chat_id):
    bot.sendMessage(chat_id, os.environ['TELEPOT'])

def handle_msg(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        command = msg['text']
        print('Got command: %s' % command)
        if command == '/ping':
            ping(chat_id)
        elif command == '/ip':
            get_pi(chat_id)
        elif command == '/refresh':
            refresh_addr(chat_id)
        elif command == '/price':
            get_price(chat_id)
        elif command == '/telepotid':
            telepot_id(chat_id)

bot = telepot.Bot(os.environ['TELEPOT'])
bot.message_loop(handle_msg)
print('Listening')

while 1:
    time.sleep(10)
