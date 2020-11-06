import sys
import time
import datetime
import telepot
import os
import requests
import json

class Commands:
    ping = "ping"
    ip = "ip"
    price = "price"
    rpc_gbi = "rpc_gbi"
    telepot_id = "telepot_id"
    rpc_var = "rpc"

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

def rpc(chat_id, rpc):
    user = os.environ['RPC_USER']
    pwd = os.environ['RPC_PWD']
    os.system("/usr/bin/curl --user %s:%s --data-binary '{\"jsonrpc\": \"1.0\", \"id\":\"telepot_rpc_curl\", \"method\": \"%s\", \"params\": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8332/ > /tmp/rpc" %(user, pwd, rpc))
    f = open("/tmp/rpc", "r")
    msg = f.read()
    bot.sendMessage(chat_id, "RPC: " + msg)
    f.close()

def get_help(chat_id):
    options = vars(Commands)
    options_list = ""
    for option in options:
        if option != "__module__" and option != "__doc__":
            options_list += "    " + option + "\n"
    bot.sendMessage(chat_id, "Options:\n" + options_list)

def handle_msg(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        commands = (msg['text']).lower().split("_")
        command = commands[0]
        print('Got command: %s' % command)
        if command == Commands.ping:
            ping(chat_id)
        elif command == Commands.ip:
            get_pi(chat_id)
        elif command == Commands.price:
            get_price(chat_id)
        elif command == Commands.telepot_id:
            telepot_id(chat_id)
        elif command == Commands.rpc_var and len(commands) == 2:
            rpc(chat_id, commands[1].replace('_', ''))
        else:
            bot.sendMessage(chat_id, "I don't understand: " + command)
            get_help(chat_id)

root_id = os.environ['TELEPOT']
bot = telepot.Bot(root_id)
bot.message_loop(handle_msg)
print('Listening')

while 1:
    time.sleep(5)
