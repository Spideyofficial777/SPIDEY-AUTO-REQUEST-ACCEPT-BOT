from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Spidey.bot import SpideyBot as app
from database.database import db
from .helpers import is_admin, target_user, can_target

WARN_LIMIT = 3


def warn_keyboard(chat_id, user_id):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("ʀᴇᴍᴏᴠᴇ ᴡᴀʀɴ (ᴀᴅᴍɪɴ ᴏɴʟʏ)", callback_data=f"gwrm:{chat_id}:{user_id}")]
    ])


@app.on_message(filters.command('warn') & filters.group)
async def warn(client, message):
    if not message.from_user or not await is_admin(client, message.chat.id, message.from_user.id):
        return
    user = target_user(message)
    if not user:
        return await message.reply('ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ.')
    ok, error = await can_target(client, message.chat.id, message.from_user.id, user.id)
    if not ok:
        return await message.reply(error)
    reason = ' '.join(message.command[1:]).strip()
    count = await db.group_db.add_warning(message.chat.id, user.id, message.from_user.id, reason)
    if count >= WARN_LIMIT:
        await client.ban_chat_member(message.chat.id, user.id)
        await db.group_db.set_punishment(message.chat.id, user.id, 'ban', admin_id=message.from_user.id, reason='warning limit')
        await db.group_db.reset_warnings(message.chat.id, user.id)
        suffix = f'\n\n<b>ʀᴇᴀsᴏɴ:</b> {reason}' if reason else ''
        return await message.reply(
            f'⚠️ {user.mention} ⚠️ <b>ʀᴇᴀᴄʜᴇᴅ {WARN_LIMIT}/{WARN_LIMIT} ᴡᴀʀɴs ᴀɴᴅ ᴡᴀs ʙᴀɴɴᴇᴅ.</b>{suffix}',
            parse_mode=enums.ParseMode.HTML,
        )
    suffix = f'\n<b>ʀᴇᴀsᴏɴ:</b> {reason}' if reason else ''
    await message.reply(
        f'<b>ᴜsᴇʀ {user.mention} ʜᴀs {count}/{WARN_LIMIT} ᴡᴀʀɴɪɴɢs; ʙᴇ ᴄᴀʀᴇꜰᴜʟ!</b>{suffix}',
        reply_markup=warn_keyboard(message.chat.id, user.id),
        parse_mode=enums.ParseMode.HTML,
    )


@app.on_callback_query(filters.regex(r'^gwrm:'))
async def remove_warn_callback(client, query):
    if not query.from_user:
        return
    parts = query.data.split(':')
    if len(parts) != 3:
        return await query.answer('ɪɴᴠᴀʟɪᴅ ʀᴇǫᴜᴇsᴛ.', show_alert=True)
    chat_id, user_id = int(parts[1]), int(parts[2])
    if not await is_admin(client, chat_id, query.from_user.id):
        return await query.answer('ᴀᴅᴍɪɴs ᴏɴʟʏ.', show_alert=True)
    count = await db.group_db.remove_last_warning(chat_id, user_id)
    await query.answer(f'ᴡᴀʀɴ ʀᴇᴍᴏᴠᴇᴅ. {count}/{WARN_LIMIT} ʀᴇᴍᴀɪɴ.', show_alert=True)
    try:
        member = await client.get_chat_member(chat_id, user_id)
        target = member.user
        admin_name = query.from_user.mention
        target_name = target.mention
        await query.message.reply(
            f'<b>ᴀᴅᴍɪɴ {admin_name} ʜᴀs ʀᴇᴍᴏᴠᴇᴅ {target_name}’s ᴡᴀʀɴɪɴɢ.</b>',
            parse_mode=enums.ParseMode.HTML,
        )
    except Exception:
        await query.message.reply(
            f'<b>ᴀᴅᴍɪɴ {query.from_user.mention} ʜᴀs ʀᴇᴍᴏᴠᴇᴅ ᴜsᴇʀ <code>{user_id}</code>’s ᴡᴀʀɴɪɴɢ.</b>',
            parse_mode=enums.ParseMode.HTML,
        )
    try:
        await query.message.edit_reply_markup(None)
    except Exception:
        pass


@app.on_message(filters.command('unwarn') & filters.group)
async def unwarn(client, message):
    if not message.from_user or not await is_admin(client, message.chat.id, message.from_user.id):
        return
    user = target_user(message)
    if not user:
        return await message.reply('ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ.')
    count = await db.group_db.remove_last_warning(message.chat.id, user.id)
    await message.reply(f'⚠️ {user.mention} <b>ʟᴀsᴛ ᴡᴀʀɴ ʀᴇᴍᴏᴠᴇᴅ. {count}/{WARN_LIMIT} ʀᴇᴍᴀɪɴ.</b>', parse_mode=enums.ParseMode.HTML)


@app.on_message(filters.command('resetwarns') & filters.group)
async def resetwarns(client, message):
    if not message.from_user or not await is_admin(client, message.chat.id, message.from_user.id):
        return
    user = target_user(message)
    if not user:
        return await message.reply('ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ.')
    await db.group_db.reset_warnings(message.chat.id, user.id)
    await message.reply(f'⚠️ {user.mention} <b>ᴡᴀʀɴɪɴɢs ʜᴀᴠᴇ ʙᴇᴇɴ ʀᴇsᴇᴛ.</b>', parse_mode=enums.ParseMode.HTML)


@app.on_message(filters.command('warnings') & filters.group)
async def warnings(client, message):
    user = target_user(message) or message.from_user
    if not user:
        return
    count = await db.group_db.warning_count(message.chat.id, user.id)
    await message.reply(f'⚠️ {user.mention} <b>ʜᴀs {count}/{WARN_LIMIT} ᴡᴀʀɴɪɴɢs.</b>', parse_mode=enums.ParseMode.HTML)
