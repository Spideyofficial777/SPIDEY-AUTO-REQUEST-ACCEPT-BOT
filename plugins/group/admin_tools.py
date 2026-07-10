from pyrogram import filters
from Spidey.bot import SpideyBot as app
from .helpers import is_admin


@app.on_message(filters.command('purge') & filters.group)
async def purge(client, message):
    if not message.from_user or not await is_admin(client, message.chat.id, message.from_user.id):
        return
    if not message.reply_to_message:
        return await message.reply('ʀᴇᴘʟʏ ᴛᴏ ᴛʜᴇ ꜰɪʀsᴛ ᴍᴇssᴀɢᴇ ᴛᴏ ᴘᴜʀɢᴇ.')
    start, end = message.reply_to_message.id, message.id
    deleted = 0
    for chunk_start in range(start, end + 1, 100):
        ids = list(range(chunk_start, min(chunk_start + 100, end + 1)))
        try:
            await client.delete_messages(message.chat.id, ids)
            deleted += len(ids)
        except Exception:
            pass
    try:
        status = await client.send_message(message.chat.id, f'{deleted} ᴍᴇssᴀɢᴇs ᴘᴜʀɢᴇᴅ.')
        await status.delete()
    except Exception:
        pass


@app.on_message(filters.command('del') & filters.group)
async def delete(client, message):
    if not message.from_user or not await is_admin(client, message.chat.id, message.from_user.id):
        return
    if message.reply_to_message:
        try:
            await message.reply_to_message.delete()
            await message.delete()
        except Exception:
            pass
