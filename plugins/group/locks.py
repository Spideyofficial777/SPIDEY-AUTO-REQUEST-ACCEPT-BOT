import re
from pyrogram import filters
from Spidey.bot import SpideyBot as app
from database.database import db
from .helpers import is_admin

TYPES = {'links', 'photo', 'video', 'sticker', 'gif', 'voice', 'audio', 'document', 'poll', 'forward', 'contact', 'location'}


@app.on_message(filters.command(['lock', 'unlock']) & filters.group)
async def lock_cmd(client, message):
    if not message.from_user or not await is_admin(client, message.chat.id, message.from_user.id):
        return
    if len(message.command) < 2 or message.command[1].lower() not in TYPES:
        return await message.reply('ᴛʏᴘᴇs: ' + ', '.join(sorted(TYPES)))
    key = message.command[1].lower()
    await db.group_db.set_lock(message.chat.id, key, message.command[0].lower() == 'lock')
    await message.reply(f'{key} sᴇᴛᴛɪɴɢ ᴜᴘᴅᴀᴛᴇᴅ.')


@app.on_message(filters.command('locks') & filters.group)
async def lock_status(client, message):
    locks = await db.group_db.get_locks(message.chat.id)
    lines = [f'• {key}: {"ʟᴏᴄᴋᴇᴅ" if locks.get(key) else "ᴜɴʟᴏᴄᴋᴇᴅ"}' for key in sorted(TYPES)]
    await message.reply('ʟᴏᴄᴋ sᴛᴀᴛᴜs\n' + '\n'.join(lines))


@app.on_message(filters.group, group=5)
async def enforce(client, message):
    if not message.from_user or await is_admin(client, message.chat.id, message.from_user.id):
        return
    locks = await db.group_db.get_locks(message.chat.id)
    text = message.text or message.caption or ''
    kind = None
    if text and re.search(r'(?:https?://|www\.|t\.me/|telegram\.me/)', text, re.I): kind = 'links'
    elif message.photo: kind = 'photo'
    elif message.video: kind = 'video'
    elif message.sticker: kind = 'sticker'
    elif message.animation: kind = 'gif'
    elif message.voice: kind = 'voice'
    elif message.audio: kind = 'audio'
    elif message.document: kind = 'document'
    elif message.poll: kind = 'poll'
    elif getattr(message, 'forward_date', None): kind = 'forward'
    elif message.contact: kind = 'contact'
    elif message.location: kind = 'location'
    if kind and locks.get(kind):
        try:
            await message.delete()
        except Exception:
            pass
