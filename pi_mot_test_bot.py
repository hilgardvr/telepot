import sys
import time
import datetime
import telepot
import os
import requests
import json

def get_price(chat_id):
    url = "https://blockchain.info/ticker"
    r = requests.get(url)
    data = r.json()
    usd = str(data["USD"]["buy"])
    bot.sendMessage(chat_id, "BTC-USD top bid: " + usd)

def get_pi(chat_id):
    os.system("/sbin/ifconfig > /tmp/addr")
    os.system("chmod 750 /tmp/addr")
    f = open("/tmp/addr", "r")
    addr = f.read()
    bot.sendMessage(chat_id, "Address: " + addr)
    f.close()

def ping(chat_id):
    bot.sendMessage(chat_id, "PiPing")

def telepot_id(chat_id):
    bot.sendMessage(chat_id, "rootId: " + root_id)

def rpc(chat_id, msg):
    user = os.environ['RPC_USER']
    pwd = os.environ['RPC_PWD']
    os.system("/usr/bin/curl --user %s:%s --data-binary '{\"jsonrpc\": \"1.0\", \"id\":\"curltest\", \"method\": \"getblockchaininfo\", \"params\": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8332/ > /tmp/msg" %(user, pwd))
    f = open("/tmp/msg", "r")
    msg = f.read()
    bot.sendMessage(chat_id, "RPC: " + msg)
    f.close()

def handle_msg(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        command = (msg['text']).lower()
        print('Got command: %s' % command)
        if command == 'ping':
            ping(chat_id)
        elif command == 'ip':
            get_pi(chat_id)
        elif command == 'price':
            get_price(chat_id)
        elif command == 'telepotid':
            telepot_id(chat_id)
        elif command == "rpc_gbi":
            rpc(chat_id, command)

root_id = os.environ['TELEPOT']
bot = telepot.Bot(root_id)
bot.message_loop(handle_msg)
print('Listening')

while 1:
    time.sleep(10)
