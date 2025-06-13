import sys
import glob
import importlib
from pathlib import Path
from pyrogram import idle
import logging
import logging.config

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("cinemagoer").setLevel(logging.ERROR)

logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)


from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from database.database import db
from configs import *
from utils import temp
from typing import Union, Optional, AsyncGenerator
from pyrogram import types
from Script import script 
from datetime import date, datetime 
import pytz
from aiohttp import web
from plugins import web_server
import pyrogram.utils
import asyncio
from pyrogram import idle
from Spidey.bot import SpideyBot
from Spidey.util.keepalive import ping_server
from Spidey.bot.clients import initialize_clients


ppath = "plugins/*.py"
files = glob.glob(ppath)
SpideyBot.start()
loop = asyncio.get_event_loop()

pyrogram.utils.MIN_CHANNEL_ID =  -1002294764885

async def Spidey_start():
    print('\n')
    print('Initalizing Spidey Filter Bot')
    
    bot_info = await SpideyBot.get_me()
    SpideyBot.username = bot_info.username

    await initialize_clients()

    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem.replace(".py", "")
            plugins_dir = Path(f"plugins/{plugin_name}.py")
            import_path = "plugins.{}".format(plugin_name)
            spec = importlib.util.spec_from_file_location(import_path, plugins_dir)
            load = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(load)
            sys.modules["plugins." + plugin_name] = load
            print("Spidey Imported => " + plugin_name)

    b_users, b_chats = await db.get_banned()
    temp.BANNED_USERS = b_users
    temp.BANNED_CHATS = b_chats

    me = await SpideyBot.get_me()
    temp.ME = me.id
    temp.U_NAME = me.username
    temp.B_NAME = me.first_name
    temp.B_LINK = me.mention
    SpideyBot.username = '@' + me.username

    logging.info(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on @{me.username}.")
    logging.info(script.LOGO)

    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    now = datetime.now(tz)
    time_now = now.strftime("%H:%M:%S %p")

    try:
        await SpideyBot.send_message(chat_id=LOG_CHANNEL, text=script.RESTART_TXT.format(me.mention, today, time_now))
        await SpideyBot.send_message(chat_id=SUPPORT_GROUP, text=f"<b>{me.mention} ʀᴇsᴛᴀʀᴛᴇᴅ 🤖</b>")
    except Exception as e:
        print(f"Make Your Bot Admin In Log Channel With Full Rights | {e}")

    app = web.AppRunner(await web_server())
    await app.setup()
    bind_address = "0.0.0.0"
    await web.TCPSite(app, bind_address, PORT).start()

    await idle()

    for admin in ADMINS:
        try:
            await SpideyBot.send_message(chat_id=admin, text=f"<b>{me.mention} ʙᴏᴛ ʀᴇsᴛᴀʀᴛᴇᴅ ✅</b>")
        except:
            pass


if __name__ == '__main__':
    try:
        loop.run_until_complete(Spidey_start())
    except Exception as e:
        logging.error(f"Error occurred: {e}")
