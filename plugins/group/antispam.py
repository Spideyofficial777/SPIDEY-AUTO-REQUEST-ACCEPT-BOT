import re
from pyrogram import filters
from Spidey.bot import SpideyBot as app
from database.database import db
from .helpers import is_admin


@app.on_message(filters.text & filters.group, group=6)
async def blacklist(client, message):
    if not message.from_user or await is_admin(client, message.chat.id, message.from_user.id):
        return
    words = await db.group_db.get_blacklist(message.chat.id)
    text = message.text or ''
    if any(re.search(r'(?<!\w)' + re.escape(word) + r'(?!\w)', text, re.I) for word in words):
        try:
            await message.delete()
        except Exception:
            pass


@app.on_message(filters.command(['blacklist', 'unblacklist']) & filters.group)
async def blackcmd(client, message):
    if not message.from_user or not await is_admin(client, message.chat.id, message.from_user.id):
        return
    if len(message.command) < 2:
        return await message.reply('ᴜsᴀɢᴇ: /blacklist word or phrase')
    word = ' '.join(message.command[1:]).strip().lower()
    await db.group_db.blacklist_word(message.chat.id, word, message.command[0].lower() == 'blacklist')
    await message.reply('ʙʟᴀᴄᴋʟɪsᴛ ᴜᴘᴅᴀᴛᴇᴅ.')


@app.on_message(filters.command('blacklists') & filters.group)
async def blacklists(client, message):
    words = await db.group_db.get_blacklist(message.chat.id)
    await message.reply('ʙʟᴀᴄᴋʟɪsᴛ:\n• ' + '\n• '.join(sorted(words)) if words else 'ʙʟᴀᴄᴋʟɪsᴛ ɪs ᴇᴍᴘᴛʏ.')
