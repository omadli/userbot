API_ID = int(input("Enter your APP_ID: "))
API_HASH = input("Enter yor API_HASH: ")

from pyrogram import Client, filters
from pyrogram.types import ChatPermissions
from pyrogram.errors import FloodWait
# from pyrogram.raw.functions import *

import json
import os
import time
from time import sleep
import random
from datetime import datetime

# from __future__ import unicode_literals
import youtube_dl
import subprocess
from videoprops import get_video_properties

app = Client("userbot", API_ID, API_HASH)
ydl = youtube_dl.YoutubeDL({"outtmpl":'video.mp4'})

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


@app.on_message(filters.command("snow", prefixes=[".", "#", "$", "!"]) & filters.me)
def snow(_, msg):
    cloud = "☁️🌨"*5 + "☁️"
    snow1 = "❄       ❄️      ❄️       ❄️       ❄️       ❄️"
    snow2 = "   ❄️       ❄️       ❄️       ❄️       ❄️       ❄️"
    snowman = "⛄️☃️⛄️☃️⛄️☃️⛄️☃️⛄️☃️⛄️"
    for i in range(6):
        try:
            s = cloud + "\n" 
            for j in range(i):
                s += snow1 if(j%2) else snow2
                s += "\n"
            s += "\n" * (5-i)
            s += snowman
            msg.edit(s)
            sleep(0.3) # 80 ms
        except FloodWait as e:
            sleep(e.x)
    for i in range(4):
        try:
            s = cloud + "\n"*(i+2)
            for j in range(4-i):
                s += snow2 if(j%2) else snow1
                s += "\n"
            s += snowman
            msg.edit(s)
            sleep(0.3) # 80 ms
        except FloodWait as e:
            sleep(e.x)


@app.on_message(filters.command("police", prefixes=[".", "#", "$", "!"]) & filters.me)
def police(_, msg):
    p1 = "🔴🔴🔴🔴⬜️⬜️🔵🔵🔵🔵\n🔴🔴🔴🔴⬜️⬜️🔵🔵🔵🔵\n🔴🔴🔴🔴⬜️⬜️🔵🔵🔵🔵"
    p2 = "🔵🔵🔵🔵⬜️⬜️🔴🔴🔴🔴\n🔵🔵🔵🔵⬜️⬜️🔴🔴🔴🔴\n🔵🔵🔵🔵⬜️⬜️🔴🔴🔴🔴"
    for i in range(50):
        try:
            s = p1 if(i%2) else p2
            msg.edit(s)
            sleep(0.01) # 10 ms
        except FloodWait as e:
            sleep(e.x)

@app.on_message(filters.command("heart", prefixes=[".", "#", "$", "!"]) & filters.me)
def heart(_, msg):
    txt = """🤍🤍🤍🤍🤍🤍🤍🤍🤍
🤍🤍❤️❤️🤍❤️❤️🤍🤍
🤍❤️❤️❤️❤️❤️❤️❤️🤍
🤍❤️❤️❤️❤️❤️❤️❤️🤍
🤍❤️❤️❤️❤️❤️❤️❤️🤍
🤍🤍❤️❤️❤️❤️❤️🤍🤍
🤍🤍🤍❤️❤️❤️🤍🤍🤍
🤍🤍🤍🤍❤️🤍🤍🤍🤍
🤍🤍🤍🤍🤍🤍🤍🤍🤍"""
    for i in ["❤️", "🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "💔", "💗", "💖", "❤️"]:
        try:
            msg.edit(txt.replace("❤️", i))
            sleep(0.1) # 100 ms
        except FloodWait as e:
            sleep(e.x)


@app.on_message(filters.command("ping", ["?", "/", "!", ".", "#", "$"]) & filters.me)
async def ping_me(_, message):
    start = datetime.now()
    await message.edit_text("`Pong!`")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await message.edit_text(f"**Pong!**\n`{ms} ms`")

@app.on_message(filters.command("get", prefixes=[".", "#", "$", "!"]) & filters.me)
def type(_, msg):
    try:
        args = msg.text.split("get ", maxsplit=1)[1]
        chid, mid = args.split()
        mid = int(mid)
        get = app.get_messages(chid, mid)
        data = get.reply_markup.inline_keyboard[0][0]["callback_data"]
        id = json.loads(data)["id"]
        msg.reply_text(f"@like #{id}")
    except Exception as e:
        msg.reply_text(e) 

@app.on_message(filters.command("dl", [".", "!", "$"]) & filters.me)
async def youtube_dl(_, msg):
    try:
        msg2 = msg
        if len(msg.text) < 10:
            if msg.reply_to_message: msg2 = msg.reply_to_message
        entities = msg2.entities
        for entity in entities:
            if entity.type == "url":
                o, l = entity.offset, entity.length
                link = msg2.text[o:o+l]
                global ydl
                await msg.edit_text(f"Yuklab olyapman...")
                try:
                    if os.path.exists("video.mp4"): os.remove("video.mp4")
                    if os.path.exists("thumb.jpg"): os.remove("thumb.jpg")
                    ydl.download([link])
                    await msg.edit_text("Yuklab oldim.")
                    subprocess.call(['ffmpeg', '-i', "video.mp4", '-ss', '00:00:00.000', '-vframes', '1', "thumb.jpg"])
                    # vid = cv2.VideoCapture("video.mp4")
                    # w, h, dur = vid.get(cv2.CAP_PROP_FRAME_HEIGHT), vid.get(cv2.CAP_PROP_FRAME_WIDTH), get_length("video.mp4")
                    props = get_video_properties('video.mp4')
                    w, h, dur = props['width'], props['height'], get_length("video.mp4")
                    await app.send_chat_action(msg.chat.id, "upload_video")
                    await msg2.reply_video(video="video.mp4", thumb="thumb.jpg", duration=dur, width=w, height=h)
                except Exception as e:
                    await msg.edit_text(f"Xatolik yuz berdi\n{e}")
                finally:
                    if os.path.exists("video.mp4"): os.remove("video.mp4")
                    if os.path.exists("thumb.jpg"): os.remove("thumb.jpg")

    except Exception as e:
        await msg.reply_text(e)


app.run()
