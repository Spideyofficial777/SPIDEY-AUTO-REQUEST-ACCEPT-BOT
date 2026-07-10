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


@app.on_message(filters.new_chat_members & filters.group, group=2)
async def welcome_members(client, message):
    settings = await db.get_settings(message.chat.id)
    if not settings.get('welcome', True):
        return
    me = await client.get_me()
    for user in message.new_chat_members:
        if user.id == me.id:
            continue
        await db.group_db.reset_warnings(message.chat.id, user.id)
        template = settings.get('welcome_text') or '<b>👋 ʜᴇʏ {mention},\n\nᴡᴇʟᴄᴏᴍᴇ ᴛᴏ {chat} ❣️</b>'
        text = render_template(template, user, message.chat)
        text, inline_markup = parse_buttons(text)
        update_button = InlineKeyboardButton('ᴜᴘᴅᴀᴛᴇs', url='https://t.me/spideyofficial_777')
        if inline_markup and inline_markup.inline_keyboard:
            rows = list(inline_markup.inline_keyboard)
            rows.append([update_button])
            inline_markup = InlineKeyboardMarkup(rows)
        else:
            inline_markup = InlineKeyboardMarkup([[update_button]])
        media = settings.get('welcome_media') or MELCOW_VID
        media_type = settings.get('welcome_media_type', 'photo')
        try:
            if media_type == 'video':
                sent = await message.reply_video(media, caption=text, reply_markup=inline_markup, parse_mode=enums.ParseMode.HTML)
            elif media_type == 'animation':
                sent = await message.reply_animation(media, caption=text, reply_markup=inline_markup, parse_mode=enums.ParseMode.HTML)
            else:
                sent = await message.reply_photo(media, caption=text, reply_markup=inline_markup, parse_mode=enums.ParseMode.HTML)
        except Exception:
            sent = await message.reply_text(text, reply_markup=inline_markup, parse_mode=enums.ParseMode.HTML)
        delay = int(settings.get('welcome_delete_after', 600) or 0)
        if settings.get('auto_delete', True) and delay > 0:
            asyncio.create_task(_delete_later(sent, delay))
