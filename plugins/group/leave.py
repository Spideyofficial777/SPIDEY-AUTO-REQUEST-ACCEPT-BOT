from pyrogram import filters, enums
from Spidey.bot import SpideyBot as app
from configs import ADMINS


@app.on_message(filters.command('leave') & filters.group)
async def leave_group(client, message):
    if not message.from_user or message.from_user.id not in ADMINS:
        return
    chat_id = message.chat.id
    title = message.chat.title or str(chat_id)
    await message.reply(
        f'<b>ʟᴇᴀᴠɪɴɢ {title}...</b>',
        parse_mode=enums.ParseMode.HTML,
    )
    await client.leave_chat(chat_id)
