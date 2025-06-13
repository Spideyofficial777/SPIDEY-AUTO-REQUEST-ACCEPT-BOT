from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import UserNotParticipant
from datetime import datetime
import random, traceback, os
from configs import CAPTCHA_JOIN_PROTECTION, LOG_CHANNEL
from database.database import *
from Spidey.bot import SpideyBot as app, Client

# Define image URLs
background_image_url = "https://i.ibb.co/RymDMxS/66e7d1b6.jpg"

# --- JOIN REQUEST HANDLER WITH CAPTCHA PROTECTION ---
@app.on_chat_join_request(filters.group | filters.channel)
async def approve_join_request(_, message):
    try:
        user = message.from_user
        chat = await app.get_chat(message.chat.id)
        channel_name = chat.title if chat.title else "our channel"

        if CAPTCHA_JOIN_PROTECTION:
            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🤖 ɪ ᴀᴍ ɴᴏᴛ ᴀ ʀᴏʙᴏᴛ", callback_data=f"captcha_verify:{message.chat.id}:{user.id}")]]
            )
            await app.send_photo(
                user.id,
                CAPTCHA_IMG,
                caption=f"""
<b>🔐🤖 ᴄᴀᴘᴛᴄʜᴀ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ

👋 ʜᴇʟʟᴏ {user.mention},

🚨 ᴛᴏ ᴘʀᴏᴛᴇᴄᴛ <u>{chat.title} ғʀᴏᴍ ʙᴏᴛs ᴀɴᴅ sᴘᴀᴍ, ᴡᴇ ɴᴇᴇᴅ ᴛᴏ ǫᴜɪᴄᴋʟʏ ᴠᴇʀɪғʏ ʏᴏᴜ'ʀᴇ ʜᴜᴍᴀɴ.</u>

🎯 Jᴜsᴛ ᴛᴀᴘ ᴛʜᴇ ✅ I'ᴍ ɴᴏᴛ ᴀ Rᴏʙᴏᴛ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ᴄᴏᴍᴘʟᴇᴛᴇ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ.

🛡️ ᴏɴᴄᴇ ᴄᴏɴғɪʀᴍᴇᴅ, ʏᴏᴜ’ʟʟ ʙᴇ <u>ɪᴍᴍᴇᴅɪᴀᴛᴇʟʏ ᴀᴘᴘʀᴏᴠᴇᴅ ᴀɴᴅ ɢᴀɪɴ ғᴜʟʟ ᴀᴄᴄᴇss ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ.</u>

⏱️ <b>ᴛɪᴍᴇ Lɪᴍɪᴛ: 𝟿𝟶 sᴇᴄᴏɴᴅs  
🚫 <i>ɪғ ʏᴏᴜ ᴅᴏɴ'ᴛ ᴠᴇʀɪғʏ ɪɴ ᴛɪᴍᴇ, ʏᴏᴜ ᴍᴀʏ ʙᴇ ʀᴇᴍᴏᴠᴇᴅ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ.

👇 <b>ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ᴠᴇʀɪғʏ 👇 </b>
                """,
                reply_markup=keyboard,
                message_effect_id=random.choice([
                    5104841245755180586, 5046509860389126442, 5107584321108051014
                ])
            )

            log_text = (
                f"⏳ <b>Captcha verification pending</b>\n\n"
                f"👤 <b>User:</b> {user.mention}\n"
                f"🆔 <code>{user.id}</code>\n"
                f"📢 <b>Group/Channel:</b> {chat.title}"
            )
            await app.send_message(LOG_CHANNEL, log_text)
            return

        await approve_user(chat, user, captcha_bypassed=True)

    except Exception as err:
        with open("logs/errors.log", "a") as f:
            f.write(f"\n---\nError at {datetime.now()}:\n")
            traceback.print_exc(file=f)
        print(f"Error approving join request: {str(err)}")


# --- CAPTCHA BUTTON CALLBACK HANDLER ---
@app.on_callback_query(filters.regex(r"^captcha_verify:(-?\d+):(\d+)$"))
async def approve_after_captcha(_, callback_query: CallbackQuery):
    try:
        chat_id, user_id = map(int, callback_query.data.split(":")[1:])
        if callback_query.from_user.id != user_id:
            return await callback_query.answer("⛔ This verification link isn't for you!", show_alert=True)

        chat = await app.get_chat(chat_id)
        user = callback_query.from_user
        await approve_user(chat, user, captcha_bypassed=False)

        await callback_query.answer("✅ Verification complete! You are approved.", show_alert=True)

    except Exception as e:
        print(f"[ERROR] in approve_after_captcha: {e}")
        await callback_query.answer("❌ Verification failed.", show_alert=True)


# --- COMMON FUNCTION TO APPROVE & WELCOME ---
async def approve_user(chat, user, captcha_bypassed=False):
    await app.approve_chat_join_request(chat.id, user.id)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔔 Sᴜʙsᴄʀɪʙᴇ Tᴏ Oᴜʀ Cʜᴀɴɴᴇʟ", url="https://youtube.com/@spidey_official_777")],
        [InlineKeyboardButton("💬 Cᴏɴᴛᴀᴄᴛ Sᴜᴘᴘᴏʀᴛ", url="https://t.me/hacker_x_official_777")]
    ])

    effect_id = 5159385139981059251 if user.is_premium else random.choice([
        5104841245755180586, 5046509860389126442, 5107584321108051014
    ])

    await app.send_photo(
        user.id,
        background_image_url,
        caption=f"<b>✅ Verified!\nWelcome {user.mention} to \n{chat.title}</b>",
        reply_markup=keyboard,
        message_effect_id=effect_id
    )

    log_text = (
        f"✅ <b>User Approved</b>\n\n"
        f"👤 <b>User:</b> {user.mention}\n"
        f"🆔 <b>ID:</b> <code>{user.id}</code>\n"
        f"📢 <b>Group/Channel:</b> {chat.title}\n"
        f"🆔 <b>Chat ID:</b> <code>{chat.id}</code>\n"
        f"🔐 <b>Captcha:</b> {'Bypassed' if captcha_bypassed else 'Verified'}"
    )
    await app.send_message(LOG_CHANNEL, log_text)
