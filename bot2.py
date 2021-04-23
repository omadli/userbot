API_ID = 2040149
API_HASH = "cdbcca56176c96ef5fc8b2d2f4b61e43"

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import ChatPermissions
import time
from time import sleep
import random

app = Client("lucky", API_ID, API_HASH)

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
  members = [ x for x in app.iter_chat_members(chat) if x.status not in ("administrator", "creator") ]
  random.shuffle(members)
  app.send_message(chat, "Щелчок Таноса ... *щёлк*")
  for i in range(len(members) // 2):
    try:
      app.restrict_chat_member( chat_id=chat, user_id=members[i].user.id, permissions=ChatPermissions(), until_date=int(time.time() + 86400), )
      app.send_message(chat, "Исчез " + members[i].user.first_name)
    except FloodWait as e:
      print("> waiting", e.x, "seconds.")
      time.sleep(e.x)
      app.send_message(chat, "Но какой ценой?")

@app.on_message(filters.command("get ", prefixes=[".", "#", "$", "!"]) & filters.me)
def type(_, msg):
  args = msg.text.split("get ", maxsplit=1)[1]
  chid, mid = args.split()
  mid = int(mid)
  get = app.get_messages(chid, mid)
  print(get) 
  app.send_message(msg.chat.id, get)

@app.on_message(filters.photo & filters.chat(["me", "@xvestru_channel", "@mr_pythoncik"]))
def get_bonus(_, msg):
  try:
    c = msg.caption bonus = ""
    for entity in msg.caption_entities:
      if entity.type == "code":
        l, o = entity.length, entity.offset
        bonus = c[o:o+l]
    app.send_message("me", bonus)

    import requests
    c = requests.Session()
    url1, url2, url3 = "https://xvest.ru", "https://xvest.ru/auth", "https://xvest.ru/user/promo-code"
    r1 = c.get(url1)
    # print(r1.text)
    SID = r1.cookies["SID"]
    print(SID)
    payload = {"login":"omadli", "pass":"ibmomadli007", "auth":"Войти", "SID":SID}
    r2 = c.post(url2, data=payload, cookies=r1.cookies)
    print(r2.text, r2.cookies)

    r3 = c.get(url3, cookies=r2.cookies)
    print(r3.text, r3.cookies)

    payload = {"code":bonus, "submit":"Tasdiqlash", "SID":SID}
    r4 = c.post(url3, data=payload, cookies=r2.cookies) 
    print(r4.text, r4.cookies)
    f = open("natija.html", "w")
    f.write(r4.text)
    f.close()
    if ("Bunday promo-kodi yo'q!" in r4.text) or ("Promo-kod faoliyati tugadi!" in r4.text):
      app.send_message("me", "Bunday promo-kodi yo'q! yoki Promo-kod faoliyati tugadi!")
    else:
      app.send_message("me", "Nimadir ishladi yoki xatolik")

    app.send_document("me", "natija.html")
  except Exception as e:
    app.send_message("me", e)

app.run()
