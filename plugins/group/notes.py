from pyrogram import filters
from Spidey.bot import SpideyBot as app
from database.database import db
from .helpers import is_admin, media_payload, send_payload


@app.on_message(filters.command('save') & filters.group)
async def save_note(client, message):
    if not message.from_user or not await is_admin(client, message.chat.id, message.from_user.id):
        return
    if len(message.command) < 2 or not message.reply_to_message:
        return await message.reply('ᴜsᴀɢᴇ: ʀᴇᴘʟʏ ᴡɪᴛʜ /save note_name')
    key = message.command[1].lower()
    await db.group_db.set_note(message.chat.id, key, media_payload(message.reply_to_message))
    await message.reply('ɴᴏᴛᴇ sᴀᴠᴇᴅ.')


@app.on_message(filters.command('get') & filters.group)
async def get_note(client, message):
    if len(message.command) < 2:
        return
    data = await db.group_db.get_note(message.chat.id, message.command[1].lower())
    if data:
        await send_payload(message, data)
    else:
        await message.reply('ɴᴏᴛᴇ ɴᴏᴛ ꜰᴏᴜɴᴅ.')


@app.on_message(filters.command('clear') & filters.group)
async def clear_note(client, message):
    if not message.from_user or not await is_admin(client, message.chat.id, message.from_user.id) or len(message.command) < 2:
        return
    deleted = await db.group_db.delete_note(message.chat.id, message.command[1].lower())
    await message.reply('ɴᴏᴛᴇ ᴅᴇʟᴇᴛᴇᴅ.' if deleted else 'ɴᴏᴛᴇ ɴᴏᴛ ꜰᴏᴜɴᴅ.')


@app.on_message(filters.command('notes') & filters.group)
async def list_notes(client, message):
    names = await db.group_db.list_notes(message.chat.id)
    await message.reply('ɴᴏᴛᴇs:\n• ' + '\n• '.join(names) if names else 'ɴᴏ ɴᴏᴛᴇs sᴀᴠᴇᴅ.')
