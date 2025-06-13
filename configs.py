# Don't Remove Credit @spideyofficial777
# Subscribe YouTube Channel For Amazing Bot @spidey_official_777
# Ask Doubt on telegram @hacker_x_official_777

import re
import os
from os import path, getenv, environ
from Script import script
import logging

# Utility functions
id_pattern = re.compile(r'^.\d+$')

def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default
        
#--------------------------------------------        
SESSION = environ.get('SESSION', 'auto_request_acc')
#--------------------------------------------    
API_ID = int(getenv("API_ID", "26967459"))
#--------------------------------------------    
API_HASH = getenv("API_HASH", "b71947dc4f2964519d8abdfb8b4873ac")
#--------------------------------------------    
BOT_TOKEN = getenv("BOT_TOKEN", "")
#--------------------------------------------        
CHANNEL_IDS = list(map(int, getenv("CHANNEL_IDS", "-1001959922658,-1002470391435,-1002433552221").split(",")))
#--------------------------------------------
EMOJI_MODE = bool(environ.get('EMOJI_MODE', True))  # Emoji status On (True) / Off (False)

# ⚠️ Attention: Do not change the reactions, otherwise bot reactions may stop working   
REACTIONS = ["🤝", "😇", "🤗", "😍", "👍", "🎅", "😐", "🥰", "🤩", "😱", "🤣", "😘", "👏", "😛", "😈", "🎉", "⚡️", "🫡", "🤓", "😎", "🏆", "🔥", "🤭", "🌚", "🆒", "👻", "😁"]
#--------------------------------------------        
ADMINS = list(map(int, getenv("ADMINS", "5518489725").split()))
#--------------------------------------------    
DATABASE_URI = getenv("DATABASE_URI", "mongodb+srv://spideyofficial777:6FwYFNcgrAPL8nqq@spidey777.pykfj.mongodb.net/?retryWrites=true&w=majority&appName=SPIDEY777")
DATABASE_NAME = environ.get('DATABASE_NAME', "Spidey")
#--------------------------------------------        
LOG_CHANNEL = int(getenv("LOG_CHANNEL", "-1002294764885"))
#--------------------------------------------  
CAPTCHA_JOIN_PROTECTION = is_enabled(getenv("CAPTCHA_JOIN_PROTECTION", "True"), True)
CAPTCHA_IMG = environ.get("CAPTCHA_IMG", "https://i.ibb.co/WpjrRnvK/photo-2025-05-29-15-31-25-7509890741011742736.jpg")
#--------------------------------------------    
SUPPORT_GROUP = int(environ.get('SUPPORT_GROUP', '-1002294764885'))
#--------------------------------------------    
START_IMG = (environ.get('START_IMG', 'https://graph.org/file/2518d4eb8c88f8f669f4c.jpg https://graph.org/file/d6d9d9b8d2dc779c49572.jpg https://graph.org/file/4b04eaad1e75e13e6dc08.jpg https://graph.org/file/05066f124a4ac500f8d91.jpg https://graph.org/file/2c64ed483c8fcf2bab7dd.jpg https://i.ibb.co/CPxdkHR/IMG-20240818-192201-633.jpg')).split()
#--------------------------------------------    
MELCOW_VID = environ.get("MELCOW_VID", "https://envs.sh/Wdj.jpg")
MELCOW_NEW_USERS = is_enabled((environ.get('MELCOW_NEW_USERS', "True")), True)
#--------------------------------------------
PORT = os.environ.get("PORT", "8080")
#-------------------------------------------- 
MSG_ALRT = environ.get('MSG_ALRT', 'sʜᴀʀᴇ ᴀɴᴅ sᴜᴘᴘᴏʀᴛ ᴜs')
#--------------------------------------------
# Leave message handler
CHAT_IDS = list(map(int, getenv("CHAT_IDS", "-1001959922658,-1002470391435,-1002433552221").split(",")))
MELCOW_LEAVE_MSG = is_enabled(environ.get("MELCOW_LEAVE_MSG", "True"), True)
#--------------------------------------------
# Rejoin & support links
CHANNEL_LINK = os.getenv("CHANNEL_LINK", "https://t.me/spideyofficialupdatez")
SUPPORT_CHAT = os.getenv("SUPPORT_CHAT", "https://t.me/hacker_x_official_777")
#--------------------------------------------

# Don't Remove Credit @spideyofficial777
# Subscribe YouTube Channel For Amazing Bot @spidey_official_777
# Ask Doubt on telegram @hacker_x_official_777
