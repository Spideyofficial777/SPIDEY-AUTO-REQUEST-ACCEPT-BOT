# Don't Remove Credit @spideyofficial777
# Subscribe YouTube Channel For Amazing Bot @spidey_official_777
# Ask Doubt on telegram @hacker_x_official_777

import os
import asyncio
from aiofiles import os
import time
import logging
import random
from pyrogram import Client, filters, enums
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from pyrogram.errors import (
    FloodWait,
    InputUserDeactivated,
    UserIsBlocked,
    UserNotParticipant,
    MessageTooLong,
    PeerIdInvalid,
)
from database.database import get_all_users, add_user, already_db
from aiogram import Bot, Dispatcher, types
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Script import script
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pymongo.errors import PyMongoError
from configs import * # Spidey, START_IMG
from pyrogram.enums import ChatMembersFilter
from group import *
from utils import * # temp
from aiohttp import web
from datetime import datetime
import traceback
import os
from Spidey.bot import SpideyBot as app, Client

os.makedirs("logs", exist_ok=True)

# Image URLs
background_image_url = "https://i.ibb.co/RymDMxS/66e7d1b6.jpg"
welcome_image = "https://envs.sh/v3t.jpg"


@app.on_message(filters.command("start"))
async def start(bot, message):
    try:
        import random
        if EMOJI_MODE:
            await message.react(emoji=random.choice(REACTIONS), big=True)

        if temp.U_NAME is None:
            temp.U_NAME = (await bot.get_me()).username
        if temp.B_NAME is None:
            temp.B_NAME = (await bot.get_me()).first_name
    except Exception as e:
        print(f"Error fetching bot details: {e}")

    user_id = message.from_user.id
    user_name = message.from_user.first_name

    is_new = False
    if not already_db(user_id):
        add_user(user_id, user_name)
        is_new = True

    if is_new:
        from datetime import datetime
        Spidey = script.NEW_USER_LOG.format(
            bot_name=temp.B_NAME,
            user_id=user_id,
            user_mention=message.from_user.mention,
            username=f"@{message.from_user.username}" if message.from_user.username else "None",
            chat_title=message.chat.title if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP] else "Private Chat",
            time=datetime.now().strftime("%d-%b-%Y %I:%M %p")
        )
        await bot.send_message(LOG_CHANNEL, Spidey)

    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        buttons = [
            [InlineKeyboardButton('• ᴀᴅᴅ ᴍᴇ ᴛᴏ ᴜʀ ᴄʜᴀᴛ •', url=f'http://t.me/{temp.U_NAME}?startgroup=true')],
            [
                InlineKeyboardButton('• ᴍᴀsᴛᴇʀ •', url="https://t.me/hacker_x_official_777"),
                InlineKeyboardButton('• sᴜᴘᴘᴏʀᴛ •', url='https://t.me/deathchatting_world')
            ],
            [InlineKeyboardButton('• ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ •', url="https://t.me/+9tdbATrOMLNlN2I1")]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply(
            script.GSTART_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup
        )
        return

    # Private chat (force subscription check)
    try:
        for channel in CHANNEL_IDS:
            try:
                await app.get_chat_member(channel, message.from_user.id)
            except UserNotParticipant:
                raise UserNotParticipant

        import random
        welcome_image_url = random.choice(START_IMG)

        m = await message.reply_text("<b>ʜᴇʟʟᴏ ʙᴀʙʏ, ʜᴏᴡ ᴀʀᴇ ʏᴏᴜ \nᴡᴀɪᴛ ᴀ ᴍᴏᴍᴇɴᴛ ʙᴀʙʏ ....</b>")
        await asyncio.sleep(0.43)
        await m.edit_text("🎊")
        await asyncio.sleep(0.3)
        await m.edit_text("⚡")
        await asyncio.sleep(0.3)
        await m.edit_text("<b>ꜱᴛᴀʀᴛɪɴɢ ʙᴀʙʏ...</b>")
        await asyncio.sleep(0.3)
        await m.delete()

        m = await message.reply_sticker("CAACAgUAAxkBAAIdBGd7qZ7kMBTPT2YAAdnPRDtBSw9jwAACqwQAAr7vuFdHULNVi6H4nB4E")
        await asyncio.sleep(3)
        await m.delete()

        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("➕ Aᴅᴅ Mᴇ ᴛᴏ Yᴏᴜʀ Cʜᴀɴɴᴇʟ ➕", url="https://t.me/SPIDER_MAN_GAMING_bot?startchannel=Bots4Sale&admin=invite_users+manage_chat")],
                [
                    InlineKeyboardButton("🚀 Cʜᴀɴɴᴇʟ", url="https://t.me/+cMlrPqMjUwtmNTI1"),
                    InlineKeyboardButton("💬 Sᴜᴘᴘᴏʀᴛ", callback_data="group_info")
                ],
                [
                    InlineKeyboardButton("ℹ️ Aʙᴏᴜᴛ", callback_data="about"),
                    InlineKeyboardButton("📃 Fᴇᴀᴛᴜʀᴇs", callback_data="features")
                ],
                [InlineKeyboardButton("➕  Aᴅᴅ Mᴇ ᴛᴏ Yᴏᴜʀ Gʀᴏᴜᴘ ➕", url="https://t.me/SPIDER_MAN_GAMING_bot?startgroup=true")]
            ]
        )

        await message.reply_photo(
            photo=welcome_image_url,
            caption=(script.START_MSG.format(message.from_user.mention)),
            reply_markup=keyboard
        )

    except UserNotParticipant:
        buttons = []
        for channel in CHANNEL_IDS:
            try:
                chat = await app.get_chat(channel)
                if chat.username:
                    channel_link = f"https://t.me/{chat.username}"
                else:
                    channel_link = await app.export_chat_invite_link(channel)

                buttons.append([InlineKeyboardButton(f"🚀 Join {chat.title}", url=channel_link)])

            except Exception as e:
                print(f"Error fetching channel link: {e}")
                continue

        buttons.append([InlineKeyboardButton("🔄 ᴄʜᴇᴄᴋ ᴀɢᴀɪɴ", callback_data="chk")])
        keyboard = InlineKeyboardMarkup(buttons)

        await message.reply_photo(
            photo=welcome_image,
            caption=f"<b>⚠️ Access Denied! ⚠️\n\n🔥 Hello {message.from_user.mention}!\n\n"
                    "You need to join all required channels before proceeding!\n\n"
                    "👉 [✨ Join Now ✨](https://t.me/SPIDEYOFFICIAL777)</b>",
            reply_markup=keyboard
        )



async def get_channel_link(client: Client, channel_id: int) -> str:
    """Fetches the invite link of a Telegram channel."""
    try:
        chat = await client.get_chat(channel_id)
        if chat.username:
            return f"https://t.me/{chat.username}"
        
        invite_link = chat.invite_link
        if not invite_link:
            invite_link = await client.export_chat_invite_link(channel_id)

        return invite_link  
    except Exception as e:
        print(f"Error fetching channel link: {e}")
        return "https://t.me/SPIDEYOFFICIAL777"  # Default backup link

@app.on_callback_query(filters.regex("^chk$"))
async def check_subscription(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    try:
        # Check if user is subscribed to all required channels
        for channel_id in CHANNEL_IDS:
            try:
                await client.get_chat_member(channel_id, user_id)
            except UserNotParticipant:
                raise UserNotParticipant  # Force jump to except if any one fails

        # If user is subscribed, show main menu
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add Me to Your Channel ➕", url="https://t.me/SPIDER_MAN_GAMING_bot?startchannel=Bots4Sale&admin=invite_users+manage_chat")],
            [InlineKeyboardButton("🚀 Channel", url="https://t.me/+cMlrPqMjUwtmNTI1"),
             InlineKeyboardButton("💬 Support", url="https://t.me/SPIDEYOFFICIAL777")],
            [InlineKeyboardButton("➕ Add Me to Your Group ➕", url="https://t.me/SPIDER_MAN_GAMING_bot?startgroup=true")]
        ])

        await callback_query.message.edit_text(
            script.START_MSG.format(callback_query.from_user.mention),
            reply_markup=keyboard,
            disable_web_page_preview=True
        )

    except UserNotParticipant:
        # If not subscribed, show the join buttons
        buttons = []
        for channel_id in CHANNEL_IDS:
            try:
                chat = await client.get_chat(channel_id)
                channel_name = chat.title or "Channel"
                channel_link = f"https://t.me/{chat.username}" if chat.username else await client.export_chat_invite_link(channel_id)
                buttons.append([InlineKeyboardButton(f"🚀 Join {channel_name}", url=channel_link)])
            except Exception as e:
                print(f"Error getting channel info: {e}")
                continue

        buttons.append([InlineKeyboardButton("🔄 Check Again", callback_data="chk")])
        keyboard = InlineKeyboardMarkup(buttons)

        await callback_query.answer(
            "🙅 Yᴏᴜ ᴀʀᴇ ɴᴏᴛ sᴜʙsᴄʀɪʙᴇᴅ ᴛᴏ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ. Pʟᴇᴀsᴇ ᴊᴏɪɴ ᴀɴᴅ ᴄʟɪᴄᴋ 'Cʜᴇᴄᴋ Aɢᴀɪɴ' ᴛᴏ ᴄᴏɴғɪʀᴍ 🙅'.",
            show_alert=True
        )
        await callback_query.message.edit_reply_markup(reply_markup=keyboard)


@app.on_message(filters.command("users") & filters.user(ADMINS))
async def list_users(client, message: Message):
    Spidey = await message.reply("📌 **Fetching Users List...**")
    
    users_list = get_all_users()
    if not users_list:
        return await Spidey.edit_text("🚫 **No users found in the database.**")

    out = "👥 **Users Saved In DB:**\n\n"
    for user in users_list:
        user_id = user.get("user_id")
        user_name = user.get("name", f"User {user_id}")
        is_banned = user.get("ban_status", {}).get("is_banned", False)

        out += f"➤ <a href='tg://user?id={user_id}'>{user_name}</a>"
        if is_banned:
            out += " ❌ (Banned User)"
        out += "\n"

    await Spidey.edit_text(out)


@app.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.reply)
async def broadcast_users(bot, message):
    users = get_all_users()

    if not users:
        return await message.reply_text("🚫 **No users found in the database.**")

    broadcast_message = message.reply_to_message  
    Spidey = await message.reply_text("📡 **Broadcasting message to all users...**")
    
    total_users = len(list(users))
    success, failed = 0, 0
    start_time = time.time()

    
    for user in users:
        user_id = user.get("user_id")
        try:
            await bot.copy_message(
                chat_id=int(user_id),
                from_chat_id=broadcast_message.chat.id,
                message_id=broadcast_message.id
            )
            success += 1
        except UserIsBlocked:
            failed += 1
        except PeerIdInvalid:
            failed += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception as e:
            print(f"Error broadcasting to {user_id}: {e}")
            failed += 1
        
        
        if (success + failed) % 10 == 0:
            await Spidey.edit_text(
                f"📡 **Broadcast in Progress...**\n\n"
                f"👥 **Total Users:** `{total_users}`\n"
                f"✅ **Successful:** `{success}`\n"
                f"❌ **Failed:** `{failed}`\n\n"
                f"🔥 **Powered by Spidey** 🕷️"
            )
    
    await Spidey.edit_text(
        f"📡 **Broadcast Completed!**\n\n"
        f"👥 **Total Users:** `{total_users}`\n"
        f"✅ **Successful:** `{success}`\n"
        f"❌ **Failed:** `{failed}`\n"
        f"🕒 **Time Taken:** `{round(time.time() - start_time, 2)} sec`\n\n"
        f"🚀 **Broadcast by [Spidey](https://t.me/SPIDEYOFFICIAL777)**\n"
        f"🔹 **Follow [Spidey Network](https://t.me/SPIDEY_CINEMA_X_AI_BOT)**"

    )
@app.on_message(filters.command("send") & filters.user(ADMINS))
async def send_msg(bot, message):
    if message.reply_to_message:
        target_ids = message.text.split(" ")[1:]
        if not target_ids:
            await message.reply_text("<b>ᴘʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴏɴᴇ ᴏʀ ᴍᴏʀᴇ ᴜꜱᴇʀ ɪᴅꜱ...</b>")
            return
        
        success_count = 0
        error_logs = ""

        try:
            for target_id in target_ids:
                try:
                    
                    if not already_db(target_id):
                        error_logs += f"❌ User ID <code>{target_id}</code> is not found in the database.\n"
                        continue
                    
                    user = await bot.get_users(target_id)
                    await message.reply_to_message.copy(int(user.id))
                    success_count += 1

                except Exception as e:
                    error_logs += f"‼️ Error in ID <code>{target_id}</code>: <code>{str(e)}</code>\n"

            # ✅ Ensure proper message formatting to avoid ENTITY_BOUNDS_INVALID error
            await message.reply_text(f"<b>✅ ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ ꜱᴇɴᴛ ᴍᴇꜱꜱᴀɢᴇꜱ ᴛᴏ `{success_count}` ᴜꜱᴇʀꜱ.\n\n{error_logs}</b>")

        except Exception as e:
            await message.reply_text(f"<b>‼️ Error - <code>{e}</code></b>")

    else:
        await message.reply_text("<b>ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴀꜱ ᴀ ʀᴇᴘʟʏ ᴛᴏ ᴀɴʏ ᴍᴇꜱꜱᴀɢᴇ,\n"
                                 "ꜰᴏʀ ᴇɢ - <code>/send user_id1 user_id2</code></b>")

                                 
@app.on_message(filters.command(["info"]))
async def who_is(client, message):
    status_message = await message.reply_text("`Fetching user info...`")
    await status_message.edit("`Processing user info...`")
    from_user_id = message.reply_to_message.from_user.id if message.reply_to_message else message.from_user.id
    
    try:
        from_user = await client.get_users(from_user_id)
    except Exception as error:
        await status_message.edit(f"❌ Error: {error}")
        return

    if not from_user:
        return await status_message.edit("❌ No valid user_id/message specified.")

    message_out_str = f"""
<b>➲ First Name:</b> {from_user.first_name}
<b>➲ Last Name:</b> {from_user.last_name or "None"}
<b>➲ Telegram ID:</b> <code>{from_user.id}</code>
<b>➲ Username:</b> @{from_user.username or "None"}
<b>➲ Data Centre:</b> <code>{getattr(from_user, 'dc_id', 'N/A')}</code>
<b>➲ Profile Link:</b> <a href='tg://user?id={from_user.id}'><b>Click Here</b></a>
"""

    if message.chat.type in (enums.ChatType.SUPERGROUP, enums.ChatType.CHANNEL):
        try:
            chat_member_p = await message.chat.get_member(from_user.id)
            joined_date = (
                chat_member_p.joined_date.strftime("%Y.%m.%d %H:%M:%S") 
                if chat_member_p.joined_date else "Unknown"
            )
            message_out_str += f"\n<b>➲ Joined this chat on:</b> <code>{joined_date}</code>"
        except:
            pass

    # **Buttons**
    buttons = [[InlineKeyboardButton('🔐 Close', callback_data='close_data')]]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    if from_user.photo:
        photo = await client.download_media(from_user.photo.big_file_id)
        await message.reply_photo(
            photo=photo,
            caption=message_out_str,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        os.remove(photo)
    else:
        await message.reply_text(
            text=message_out_str,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    await status_message.delete()

@app.on_message(filters.command("help"))
async def help_command(client, message):
    await message.reply_text(script.HELP_TXT)
 

# Don't Remove Credit @spideyofficial777
# Subscribe YouTube Channel For Amazing Bot @spidey_official_777
# Ask Doubt on telegram @hacker_x_official_777