from pyrogram import filters, enums
from pyrogram.types import ChatPermissions
from Spidey.bot import SpideyBot as app
from database.database import db
from .helpers import is_admin, target_user, parse_duration, until_date, can_target, command_reason


@app.on_message(filters.command(['mute', 'tmute']) & filters.group)
async def mute(client, message):
    if not message.from_user or not await is_admin(client, message.chat.id, message.from_user.id):
        return
    user = target_user(message)
    if not user:
        return await message.reply('ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ.')
    ok, error = await can_target(client, message.chat.id, message.from_user.id, user.id)
    if not ok:
        return await message.reply(error)
    timed = message.command[0].lower() == 'tmute'
    seconds = parse_duration(message.command[1]) if timed and len(message.command) > 1 else None
    if timed and not seconds:
        return await message.reply('<b>ᴜsᴀɢᴇ:</b> <code>/tmute 30m [reason]</code> ᴀs ᴀ ʀᴇᴘʟʏ.', parse_mode=enums.ParseMode.HTML)
    reason = command_reason(message, duration_command=timed)
    await client.restrict_chat_member(message.chat.id, user.id, ChatPermissions(), until_date=until_date(seconds) if seconds else None)
    await db.group_db.set_punishment(message.chat.id, user.id, 'mute', seconds, message.from_user.id, reason)
    duration = f'\n<b>ᴅᴜʀᴀᴛɪᴏɴ:</b> {message.command[1]}' if seconds else '\n<b>ᴅᴜʀᴀᴛɪᴏɴ:</b> ᴘᴇʀᴍᴀɴᴇɴᴛ'
    reason_line = f'\n<b>ʀᴇᴀsᴏɴ:</b> {reason}' if reason else ''
    await message.reply(f'🔇 {user.mention} <b>ʜᴀs ʙᴇᴇɴ ᴍᴜᴛᴇᴅ.</b>{duration}{reason_line}', parse_mode=enums.ParseMode.HTML)


@app.on_message(filters.command('unmute') & filters.group)
async def unmute(client, message):
    if not message.from_user or not await is_admin(client, message.chat.id, message.from_user.id):
        return
    user = target_user(message)
    if not user:
        return await message.reply('ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ.')
    permissions = ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True,
        can_send_polls=True,
    )
    await client.restrict_chat_member(message.chat.id, user.id, permissions)
    await db.group_db.clear_punishment(message.chat.id, user.id, 'mute')
    await message.reply(f'🔊 {user.mention} <b>ʜᴀs ʙᴇᴇɴ ᴜɴᴍᴜᴛᴇᴅ.</b>', parse_mode=enums.ParseMode.HTML)
