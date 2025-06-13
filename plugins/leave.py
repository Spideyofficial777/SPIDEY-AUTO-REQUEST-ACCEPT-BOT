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

@app.on_chat_member_updated(filters.group)
async def user_leave_handler(client: Client, event: ChatMemberUpdated):
    if not MELCOW_LEAVE_MSG:
        return  # 🔕 Disabled from config

    try:
        chat_id = event.chat.id
        chat_title = event.chat.title

        if chat_id not in CHAT_IDS:
            return  # 🚫 Not a monitored chat

        if not event.old_chat_member or not event.new_chat_member:
            return  # Incomplete event data

        user = event.old_chat_member.user
        old_status = event.old_chat_member.status
        new_status = event.new_chat_member.status

        # Detect if user left or was kicked
        if old_status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR] and new_status in [ChatMemberStatus.LEFT, ChatMemberStatus.KICKED]:
            logging.info(f"👋 {user.first_name} left {chat_title} ({chat_id})")

            leave_media = random.choice(MEDIA_FILES) if MEDIA_FILES else None

            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Rejoin Channel", url=CHANNEL_LINK)],
                [InlineKeyboardButton("💬 Need Help?", url=SUPPORT_CHAT)]
            ])

            leave_msg = (
                f"🚀 <b>{user.first_name} has left the chat!</b>\n\n"
                "😢 We're sad to see you go. If you left by mistake, click below to rejoin!\n\n"
                "🔹 Stay connected with latest updates.\n"
                "💡 Need help? Contact support."
            )

            if leave_media:
                await client.send_photo(chat_id=chat_id, photo=leave_media, caption=leave_msg, reply_markup=keyboard, parse_mode="html")
            else:
                await client.send_message(chat_id=chat_id, text=leave_msg, reply_markup=keyboard, parse_mode="html")

    except Exception as e:
        logging.error(f"❌ Error in user_leave_handler: {e}")
