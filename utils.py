import logging
from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid
#from info import AUTH_CHANNEL, LONG_IMDB_DESCRIPTION, IS_VERIFY , SETTINGS , START_IMG
import asyncio
from pyrogram.types import Message
from pyrogram import enums
import pytz, re, os 
#from shortzy import Shortzy
#from datetime import datetime
from typing import Any
from database.database import db

#BANNED = {}
#imdb = Cinemagoer() 
 
class temp(object):
    ME = None
    CURRENT=int(os.environ.get("SKIP", 2))
    CANCEL = False
    U_NAME = None
    B_NAME = None
    B_LINK = None
    MELCOW = {}
    SETTINGS = {}
    FILES_ID = {}
    USERS_CANCEL = False
    GROUPS_CANCEL = False    
    CHAT = {}
    BANNED_USERS = []
    BANNED_CHATS = []

async def save_group_settings(group_id, key, value):
    current = await get_settings(group_id)
    current.update({key: value})
    temp.SETTINGS.update({group_id: current})
    await db.update_settings(group_id, current)


def get_status():
    tz = pytz.timezone('Asia/Kolkata')
    hour = datetime.now(tz).hour

    if 5 <= hour < 12:
        sts = "𝐺𝑜𝑜𝑑 𝑀𝑜𝑟𝑛𝑖𝑛𝑔 🌞"
    elif 12 <= hour < 18:
        sts = "𝐺𝑜𝑜𝑑 𝐴𝑓𝑡𝑒𝑟𝑛𝑜𝑜𝑛 🌤"
    elif 18 <= hour < 21:
        sts = "𝐺𝑜𝑜𝑑 𝐸𝑣𝑒𝑛𝑖𝑛𝑔 🌇"
    else:
        sts = "𝐺𝑜𝑜𝑑 𝑁𝑖𝑔ℎ𝑡 🌙"

    return sts
    
async def is_check_admin(bot, chat_id, user_id):
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]
    except:
        return False

async def get_seconds(time_string):
    def extract_value_and_unit(ts):
        value = ""
        unit = ""
        index = 0
        while index < len(ts) and ts[index].isdigit():
            value += ts[index]
            index += 1
        unit = ts[index:].lstrip()
        if value:
            value = int(value)
        return value, unit
    value, unit = extract_value_and_unit(time_string)
    if unit == 's':
        return value
    elif unit == 'min':
        return value * 60
    elif unit == 'hour':
        return value * 3600
    elif unit == 'day':
        return value * 86400
    elif unit == 'month':
        return value * 86400 * 30
    elif unit == 'year':
        return value * 86400 * 365
    else:
        return 0
  
async def save_default_settings(id):
    await db.reset_group_settings(id)
    current = await db.get_settings(id)
    temp.SETTINGS.update({id: current})