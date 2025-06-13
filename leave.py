import logging
import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatMemberUpdated
from Spidey.bot import SpideyBot as app
from configs import *


# Enable logging for debugging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 🔹 Images & GIFs for Random Selection
MEDIA_FILES = [
    "https://i.ibb.co/RymDMxS/66e7d1b6.jpg",
    "https://i.ibb.co/CPxdkHR/IMG-20240818-192201-633.jpg",
    "https://media.giphy.com/media/3o7aD2saalBwwftBIY/giphy.gif",
    "https://media.giphy.com/media/l3q2K5jinAlChoCLS/giphy.gif"
]

# 🔹 Groups & Channels to Track
CHAT_IDS = [-1002453024937, -1001959922658, -1002470391435, -1002481537934]

# 🔹 Support & Rejoin Links
SUPPORT_CHAT = "https://t.me/hacker_x_official_777"
CHANNEL_LINK = "https://t.me/spideyofficial777"

@app.on_chat_member_updated(filters.group)
async def user_leave_handler(client: Client, event: ChatMemberUpdated):
    try:
        logging.info(f"📌 Event detected in chat {event.chat.id} for user {event.from_user.id}")

        if event.chat.id not in CHAT_IDS:
            logging.info(f"🚫 Chat ID {event.chat.id} not in tracked list. Ignoring.")
            return  

        if not event.old_chat_member or not event.new_chat_member:
            logging.warning(f"⚠️ Skipping event: Missing member data in chat {event.chat.id}")
            return  

        user = event.old_chat_member.user if event.old_chat_member else None
        if not user:
            logging.warning(f"⚠️ Skipping event: User data missing in chat {event.chat.id}")
            return  

        old_status = event.old_chat_member.status
        new_status = event.new_chat_member.status

        if old_status in ["member", "administrator"] and new_status == "left":
            logging.info(f"✅ {user.first_name} ({user.id}) left {event.chat.title}")

            leave_media = random.choice(MEDIA_FILES)

            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Rejoin Channel", url=CHANNEL_LINK)],
                [InlineKeyboardButton("💬 Need Help?", url=SUPPORT_CHAT)]
            ])

            leave_msg = (
                f"🚀 **{user.mention} has left!**\n\n"
                "😢 We're sad to see you go! If it was a mistake, click below to rejoin!\n\n"
                "🔹 **Stay updated with exciting news & updates.**\n"
                "💡 Need help? Contact our support team!"
            )

            await client.send_photo(chat_id=event.chat.id, photo=leave_media, caption=leave_msg, reply_markup=keyboard)
            logging.info(f"✅ Leave message sent in {event.chat.title} for {user.first_name}")

    except Exception as e:
        logging.error(f"❌ Error sending leave message: {e}")
