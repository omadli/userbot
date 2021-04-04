from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.raw.functions import *
 
from pyrogram.types import ChatPermissions
 
import time
from time import sleep
import random
 
app = Client("mr_pythoncik", 2625259, "0ddd178b7a1e5d3b220f9905b5d8f85a")

# Команда type
@app.on_message(filters.command("type", prefixes=[".", "#", "$", "!"]) & filters.me)
def type(_, msg):
    orig_text = msg.text.split("type ", maxsplit=1)[1]
    text = orig_text
    tbp = "" # to be printed
    typing_symbol = "▒"
 
    while(tbp != orig_text):
        try:
            msg.edit(tbp + typing_symbol)
            sleep(0.04) # 40 ms
 
            tbp = tbp + text[0]
            text = text[1:]
 
            msg.edit(tbp)
            sleep(0.05)
 
        except FloodWait as e:
            sleep(e.x)
 

@app.on_message(filters.command("thanos", prefixes=[".", "!", "#", "$"]) & filters.me)
def thanos(_, msg):
    chat = msg.text.split("thanos ", maxsplit=1)[1]
 
    members = [
        x
        for x in app.iter_chat_members(chat)
        if x.status not in ("administrator", "creator")
    ]
 
    random.shuffle(members)
 
    app.send_message(chat, "Щелчок Таноса ... *щёлк*")
 
    for i in range(len(members) // 2):
        try:
            app.restrict_chat_member(
                chat_id=chat,
                user_id=members[i].user.id,
                permissions=ChatPermissions(),
                until_date=int(time.time() + 86400),
            )
            app.send_message(chat, "Исчез " + members[i].user.first_name)
        except FloodWait as e:
            print("> waiting", e.x, "seconds.")
            time.sleep(e.x)
 
    app.send_message(chat, "Но какой ценой?")
 
@app.on_message(filters.command("get", prefixes=[".", "#", "$", "!"]) & filters.me)
def type(_, msg):
    try:
        args = msg.text.split("get ", maxsplit=1)[1]
        chid, *mid = args.split()
        mid = list(map('int', mid))
        get = channels.GetMessages(chid, mid)
        print(get)
        app.send_message(msg.chat.id, get)
    except Exception as e:
        print(e)
        app.send_message(msg.chat.id, e)
app.run()
