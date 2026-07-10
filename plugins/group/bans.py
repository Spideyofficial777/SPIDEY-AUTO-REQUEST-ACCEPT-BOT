from pyrogram import filters, enums
from Spidey.bot import SpideyBot as app
from database.database import db
from .helpers import is_admin, target_user, parse_duration, until_date, can_target, command_reason


@app.on_message(filters.command(['ban', 'tban']) & filters.group)
async def ban(client, message):
    if not message.from_user or not await is_admin(client, message.chat.id, message.from_user.id):
        return
    user = target_user(message)
    if not user:
        return await message.reply('ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ.')
    ok, error = await can_target(client, message.chat.id, message.from_user.id, user.id)
    if not ok:
        return await message.reply(error)
    timed = message.command[0].lower() == 'tban'
    seconds = parse_duration(message.command[1]) if timed and len(message.command) > 1 else None
    if timed and not seconds:
        return await message.reply('<b>ᴜsᴀɢᴇ:</b> <code>/tban 30m [reason]</code> ᴀs ᴀ ʀᴇᴘʟʏ.', parse_mode=enums.ParseMode.HTML)
    reason = command_reason(message, duration_command=timed)
    await client.ban_chat_member(message.chat.id, user.id, until_date=until_date(seconds) if seconds else None)
    await db.group_db.set_punishment(message.chat.id, user.id, 'ban', seconds, message.from_user.id, reason)
    duration = f'\n<b>ᴅᴜʀᴀᴛɪᴏɴ:</b> {message.command[1]}' if seconds else '\n<b>ᴅᴜʀᴀᴛɪᴏɴ:</b> ᴘᴇʀᴍᴀɴᴇɴᴛ'
    reason_line = f'\n<b>ʀᴇᴀsᴏɴ:</b> {reason}' if reason else ''
    await message.reply(
        f'🚫 {user.mention} <b>ʜᴀs ʙᴇᴇɴ ʙᴀɴɴᴇᴅ.</b>{duration}{reason_line}',
        parse_mode=enums.ParseMode.HTML,
    )


@app.on_message(filters.command('unban') & filters.group)
async def unban(client, message):
    if not message.from_user or not await is_admin(client, message.chat.id, message.from_user.id):
        return
    user = target_user(message)
    uid = user.id if user else (int(message.command[1]) if len(message.command) > 1 and message.command[1].lstrip('-').isdigit() else None)
    if not uid:
        return await message.reply('ʀᴇᴘʟʏ ᴏʀ ɢɪᴠᴇ ᴜsᴇʀ ɪᴅ.')
    await client.unban_chat_member(message.chat.id, uid)
    await db.group_db.clear_punishment(message.chat.id, uid, 'ban')
    await db.group_db.reset_warnings(message.chat.id, uid)
    name = user.mention if user else f'<code>{uid}</code>'
    await message.reply(f'✅ {name} <b>ʜᴀs ʙᴇᴇɴ ᴜɴʙᴀɴɴᴇᴅ.\nᴡᴀʀɴɪɴɢs ʜᴀᴠᴇ ʙᴇᴇɴ ʀᴇsᴇᴛ.</b>', parse_mode=enums.ParseMode.HTML)
