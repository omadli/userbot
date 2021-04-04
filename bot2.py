from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.raw.functions import *
 
from pyrogram.types import ChatPermissions
 
import time
from time import sleep
import random
 
app = Client("mr_pythoncik", 2625259, "0ddd178b7a1e5d3b220f9905b5d8f85a")

get = channels.GetMessages(channel="@O_romitan", id=[3])
msgs = get.messages
rm = msgs[0].reply_markup
print(rm)

app.run()
