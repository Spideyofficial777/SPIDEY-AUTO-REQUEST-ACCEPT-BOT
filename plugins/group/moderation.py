from pyrogram import filters, enums
from Spidey.bot import SpideyBot as app
from .helpers import is_admin, target_user, can_target, command_reason


@app.on_message(filters.command('kick') & filters.group)
async def kick(client, message):
    if not message.from_user or not await is_admin(client, message.chat.id, message.from_user.id):
        return
    user = target_user(message)
    if not user:
        return await message.reply('ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ.')
    ok, error = await can_target(client, message.chat.id, message.from_user.id, user.id)
    if not ok:
        return await message.reply(error)
    reason = command_reason(message)
    await client.ban_chat_member(message.chat.id, user.id)
    await client.unban_chat_member(message.chat.id, user.id)
    reason_line = f'\n<b>ʀᴇᴀsᴏɴ:</b> {reason}' if reason else ''
    await message.reply(f'👢 {user.mention} <b>ʜᴀs ʙᴇᴇɴ ᴋɪᴄᴋᴇᴅ.</b>{reason_line}', parse_mode=enums.ParseMode.HTML)
