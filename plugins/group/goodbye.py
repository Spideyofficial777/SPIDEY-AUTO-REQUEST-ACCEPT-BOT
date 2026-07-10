import asyncio
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Spidey.bot import SpideyBot as app
from database.database import db
from configs import MELCOW_VID
from .helpers import render_template, parse_buttons


async def _delete_later(message, delay):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception:
        pass


@app.on_message(filters.left_chat_member & filters.group, group=2)
async def goodbye_member(client, message):
    settings = await db.get_settings(message.chat.id)
    if not settings.get('goodbye', True):
        return
    user = message.left_chat_member
    if not user or user.is_bot:
        return
    template = settings.get('goodbye_text') or '<b>ᴡᴇ’ʀᴇ ᴍɪssɪɴɢ ʏᴏᴜ, {mention} 👋\n\nʜᴏᴘᴇ ᴛᴏ sᴇᴇ ʏᴏᴜ ᴀɢᴀɪɴ ɪɴ {chat}.</b>'
    text = render_template(template, user, message.chat)
    text, markup = parse_buttons(text)
    update_button = InlineKeyboardButton('ᴜᴘᴅᴀᴛᴇs', url='https://t.me/spideyofficial_777')
    if markup and markup.inline_keyboard:
        rows = list(markup.inline_keyboard)
        rows.append([update_button])
        markup = InlineKeyboardMarkup(rows)
    else:
        markup = InlineKeyboardMarkup([[update_button]])
    media = settings.get('goodbye_media') or MELCOW_VID
    media_type = settings.get('goodbye_media_type', 'photo')
    try:
        if media_type == 'video':
            sent = await message.reply_video(media, caption=text, reply_markup=markup, parse_mode=enums.ParseMode.HTML)
        elif media_type == 'animation':
            sent = await message.reply_animation(media, caption=text, reply_markup=markup, parse_mode=enums.ParseMode.HTML)
        else:
            sent = await message.reply_photo(media, caption=text, reply_markup=markup, parse_mode=enums.ParseMode.HTML)
    except Exception:
        sent = await message.reply_text(text, reply_markup=markup, parse_mode=enums.ParseMode.HTML)
    delay = int(settings.get('goodbye_delete_after', 600) or 0)
    if settings.get('auto_delete', True) and delay > 0:
        asyncio.create_task(_delete_later(sent, delay))
