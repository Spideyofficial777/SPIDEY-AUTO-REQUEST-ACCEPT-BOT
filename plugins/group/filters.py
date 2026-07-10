import secrets
from datetime import datetime, timedelta, timezone
from pyrogram import filters, enums
from Spidey.bot import SpideyBot as app
from database.database import db
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .helpers import is_admin, media_payload, send_payload
from .group_registry import register_group
from .group_selector import resolve_groups

_seen_groups = set()


@app.on_message(filters.command('filter') & filters.group)
async def add_filter(client, message):
    if not message.from_user or not await is_admin(client, message.chat.id, message.from_user.id):
        return
    if len(message.command) < 2 or not message.reply_to_message:
        return await message.reply('ᴜsᴀɢᴇ: ʀᴇᴘʟʏ ᴛᴏ ᴛᴇxᴛ/ᴍᴇᴅɪᴀ ᴡɪᴛʜ /filter word')
    key = ' '.join(message.command[1:]).strip().lower()
    payload = media_payload(message.reply_to_message)
    if not payload.get('text') and not payload.get('file_id'):
        return await message.reply('ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ ʜᴀs ɴᴏ sᴜᴘᴘᴏʀᴛᴇᴅ ᴄᴏɴᴛᴇɴᴛ.')
    await db.group_db.set_filter(message.chat.id, key, payload)
    await message.reply(f'ꜰɪʟᴛᴇʀ `{key}` sᴀᴠᴇᴅ.')


@app.on_message(filters.group, group=-100)
async def remember_group(client, message):
    chat_id = message.chat.id
    if chat_id in _seen_groups:
        return
    try:
        await register_group(client, message.chat)
        _seen_groups.add(chat_id)
    except Exception:
        pass


async def _manageable_groups(client, user_id):
    return await resolve_groups(client, user_id)


@app.on_message(filters.command('filter') & filters.private)
async def add_private_filter(client, message):
    if not message.from_user:
        return
    if len(message.command) < 2 or not message.reply_to_message:
        return await message.reply('ᴜsᴀɢᴇ: ʀᴇᴘʟʏ ᴛᴏ ᴛᴇxᴛ/ᴍᴇᴅɪᴀ ᴡɪᴛʜ /filter word')
    key = ' '.join(message.command[1:]).strip().lower()
    payload = media_payload(message.reply_to_message)
    if not payload.get('text') and not payload.get('file_id'):
        return await message.reply('ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ ʜᴀs ɴᴏ sᴜᴘᴘᴏʀᴛᴇᴅ ᴄᴏɴᴛᴇɴᴛ.')
    groups = await _manageable_groups(client, message.from_user.id)
    if not groups:
        return await message.reply('ɴᴏ ᴍᴀɴᴀɢᴇᴀʙʟᴇ ɢʀᴏᴜᴘ ꜰᴏᴜɴᴅ. ᴀᴅᴅ ᴍᴇ ᴛᴏ ᴀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴍᴀᴋᴇ ᴍᴇ ᴀᴅᴍɪɴ.')
    if len(groups) == 1:
        chat_id, title = groups[0]
        await db.group_db.set_filter(chat_id, key, payload)
        return await message.reply(f'ꜰɪʟᴛᴇʀ <code>{key}</code> sᴀᴠᴇᴅ ɪɴ <b>{title}</b>.', parse_mode=enums.ParseMode.HTML)
    token = secrets.token_urlsafe(6)
    await db.group_db.create_pending_filter(
        token,
        message.from_user.id,
        key,
        payload,
        datetime.now(timezone.utc) + timedelta(minutes=10),
    )
    rows = [[InlineKeyboardButton(title[:50], callback_data=f'pf:{token}:{chat_id}')] for chat_id, title in groups[:50]]
    await message.reply(
        'sᴇʟᴇᴄᴛ ᴛʜᴇ ɢʀᴏᴜᴘ ᴡʜᴇʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ sᴀᴠᴇ ᴛʜɪs ꜰɪʟᴛᴇʀ.',
        reply_markup=InlineKeyboardMarkup(rows),
    )


@app.on_callback_query(filters.regex(r'^pf:'))
async def private_filter_group_callback(client, query):
    if not query.from_user:
        return
    parts = query.data.split(':', 2)
    if len(parts) != 3:
        return await query.answer('ɪɴᴠᴀʟɪᴅ ʀᴇǫᴜᴇsᴛ.', show_alert=True)
    token, chat_id_raw = parts[1], parts[2]
    try:
        chat_id = int(chat_id_raw)
    except ValueError:
        return await query.answer('ɪɴᴠᴀʟɪᴅ ɢʀᴏᴜᴘ.', show_alert=True)
    pending = await db.group_db.get_pending_filter(token, query.from_user.id)
    if not pending:
        return await query.answer('ᴛʜɪs ʀᴇǫᴜᴇsᴛ ʜᴀs ᴇxᴘɪʀᴇᴅ.', show_alert=True)
    if not await is_admin(client, chat_id, query.from_user.id):
        return await query.answer('ʏᴏᴜ ᴀʀᴇ ɴᴏ ʟᴏɴɢᴇʀ ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ.', show_alert=True)
    await db.group_db.set_filter(chat_id, pending['key'], pending['data'])
    await db.group_db.delete_pending_filter(token, query.from_user.id)
    try:
        chat = await client.get_chat(chat_id)
        title = chat.title or str(chat_id)
    except Exception:
        title = str(chat_id)
    await query.answer('ꜰɪʟᴛᴇʀ sᴀᴠᴇᴅ.', show_alert=True)
    await query.message.edit_text(
        f'ꜰɪʟᴛᴇʀ <code>{pending["key"]}</code> sᴀᴠᴇᴅ ɪɴ <b>{title}</b>.',
        parse_mode=enums.ParseMode.HTML,
    )


@app.on_message(filters.command('stop') & filters.group)
async def stop_filter(client, message):
    if not message.from_user or not await is_admin(client, message.chat.id, message.from_user.id):
        return
    if len(message.command) < 2:
        return await message.reply('ᴜsᴀɢᴇ: /stop filter name')
    key = ' '.join(message.command[1:]).strip().lower()
    deleted = await db.group_db.delete_filter(message.chat.id, key)
    await message.reply('ꜰɪʟᴛᴇʀ ᴅᴇʟᴇᴛᴇᴅ.' if deleted else 'ꜰɪʟᴛᴇʀ ɴᴏᴛ ꜰᴏᴜɴᴅ.')


@app.on_message(filters.command('filters') & filters.group)
async def list_filters(client, message):
    names = await db.group_db.list_filters(message.chat.id)
    await message.reply('ꜰɪʟᴛᴇʀs:\n• ' + '\n• '.join(names) if names else 'ɴᴏ ꜰɪʟᴛᴇʀs sᴀᴠᴇᴅ.')


@app.on_message((filters.text | filters.caption) & filters.group, group=20)
async def run_filters(client, message):
    text = message.text or message.caption or ''
    if text.startswith('/'):
        return
    data = await db.group_db.match_filter(message.chat.id, text)
    if data:
        await send_payload(message, data)
