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
from utils import temp
from aiohttp import web
from datetime import datetime
import traceback
import os
from Spidey.bot import SpideyBot as app, Client


@app.on_callback_query()
async def on_callback_query(_, callback_query: CallbackQuery):
    if callback_query.data == "features":
        await callback_query.message.edit_text(text="▰ ▱ ▱")
        await callback_query.message.edit_text(text="▰ ▰ ▱")
        await callback_query.message.edit_text(text="▰ ▰ ▰")                
        about_keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "sᴜʙsᴄʀɪʙᴇ", callback_data="feedback_feature"
                    ),
                    InlineKeyboardButton(
                        "ʀᴇᴍᴏᴠᴇʙɢ", callback_data="close_data"
                    ),
                    InlineKeyboardButton(
                        "ʟɪᴠᴇ ɪᴘʟ 🏏", url="https://t.me/spideyofficialupdatez"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "Rɪɴɢᴛᴏɴᴇ", url="https://example.com/ringtone"
                    ),
                    InlineKeyboardButton("Cʜᴀᴛɢᴘᴛ", url="https://example.com/chatgpt"),
                    InlineKeyboardButton("Oᴡɴᴇʀ", callback_data="spidey"),
                ],
                [
                    InlineKeyboardButton("Mᴏᴠɪᴇs", url="https://example.com/movies"),
                    InlineKeyboardButton(
                        "Uᴘᴅᴀᴛᴇs", url="https://t.me/live_update_channel"
                    ),
                    InlineKeyboardButton(
                        "Sᴜᴘᴘᴏʀᴛ", url="https://t.me/SPIDEYOFFICIAL777"
                    ),
                ],
                [InlineKeyboardButton("⋞ Back", callback_data="back")],
            ]
        )

        await callback_query.message.edit_text(
            script.FEATURES_TXT, reply_markup=about_keyboard
        )
        await callback_query.answer(MSG_ALRT)
        
    elif callback_query.data == "about":
        await callback_query.message.edit_text(text="▰ ▱ ▱")
        await callback_query.message.edit_text(text="▰ ▰ ▱")
        await callback_query.message.edit_text(text="▰ ▰ ▰")

        features_keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("‼️ ᴅɪꜱᴄʟᴀɪᴍᴇʀ ‼️", callback_data="disclaimer")],
                [
                    InlineKeyboardButton(
                        "• ᴠɪsɪᴛ ᴏᴜʀ ᴄᴏᴍᴍᴜɴɪᴛʏ •", url="t.me/SPIDEYOFFICIAL_777"
                    )
                ],
                [
                    InlineKeyboardButton("• ᴏᴡɴᴇʀ •", user_id=int(7965267063)),
                    InlineKeyboardButton("• sᴏᴜʀᴄᴇ •", callback_data="source"),
                ],
                [InlineKeyboardButton("🛰️ ʀᴇɴᴅᴇʀɪɴɢ ꜱᴛᴀᴛᴜꜱ ☁️", callback_data="rendr")],
                [InlineKeyboardButton("⋞ Back ᴛᴏ ʜᴏᴍᴇ ", callback_data="back")],
            ]
        )

        await callback_query.message.edit_text(
            script.ABOUT_TXT, reply_markup=features_keyboard
        )
        await callback_query.answer(MSG_ALRT)
        
        
    elif callback_query.data == "feedback_feature":
        await callback_query.answer(
            "🛠️ Feedback: Save and display user feedback for admins seamlessly!",
            show_alert=True,
        )

    elif callback_query.data == "disclaimer":
        disclaimer_keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📲 ᴄᴏɴᴛᴀᴄᴛ ᴛᴏ ᴏᴡɴᴇʀ", url="https://t.me/hacker_x_official_777"
                    )
                ],
                [InlineKeyboardButton("⪻ ʙᴀᴄᴋ", callback_data="about")],
            ]
        )

        await callback_query.message.edit_text(text="● ◌ ◌")
        await callback_query.message.edit_text(text="● ● ◌")
        await callback_query.message.edit_text(text="● ● ●")

        await callback_query.message.edit_text(
            script.DISCLAIMER_TXT, reply_markup=disclaimer_keyboard
        )
        await callback_query.answer(MSG_ALRT)     
        
    elif callback_query.data == "back":
        await callback_query.message.edit_text(text="▰ ▱ ▱")
        await callback_query.message.edit_text(text="▰ ▰ ▱")
        await callback_query.message.edit_text(text="▰ ▰ ▰")

        welcome_message = script.START_MSG.format(callback_query.from_user.mention)

        main_keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                    "➕ Aᴅᴅ Mᴇ ᴛᴏ Yᴏᴜʀ Cʜᴀɴɴᴇʟ ➕",
                    url="https://t.me/SPIDER_MAN_GAMING_bot?startchannel=Bots4Sale&admin=invite_users+manage_chat",
                )
                ],
                [
                    InlineKeyboardButton("🚀 Channel", url="https://t.me/SPIDEYOFFICIAL_777"),
                    InlineKeyboardButton("💬 Sᴜᴘᴘᴏʀᴛ", callback_data="group_info"),
            ],
            [
                    InlineKeyboardButton("ℹ️ Aʙᴏᴜᴛ", callback_data="about"),
                InlineKeyboardButton("📃 Features", callback_data="features"),
                ],
                [
                    InlineKeyboardButton(
                    "➕ Aᴅᴅ Mᴇ ᴛᴏ Yᴏᴜʀ Gʀᴏᴜᴘ ➕",
                    url="https://t.me/SPIDER_MAN_GAMING_bot?startgroup=true",
                )
            ],
        ]
    )

    # Final message
        await callback_query.message.edit_text(
        welcome_message,     reply_markup=main_keyboard
    )
        await callback_query.answer(MSG_ALRT)     
        
    elif callback_query.data == "group_info":
        await callback_query.message.edit_text(text="▰ ▱ ▱")
        await callback_query.message.edit_text(text="▰ ▰ ▱")
        await callback_query.message.edit_text(text="▰ ▰ ▰")

        buttons = [
            [
                InlineKeyboardButton(
                    "× ᴀʟʟ ᴏᴜʀ ʟɪɴᴋꜱ ×", url="https://t.me/SPIDEYOFFICIAL777"
                )
            ],
            [
                InlineKeyboardButton("• ᴍᴏᴠɪᴇ ɢʀᴏᴜᴘ •", url="https://t.me/+KTXnXf_YPxJlOGRl"),
                InlineKeyboardButton(
                    "• ᴜᴘᴅᴀᴛᴇs •", url="https://t.me/SpideyOfficialUpdatez"
                ),
            ],
            [
                InlineKeyboardButton("• ʜᴀᴄᴋ •", url="https://t.me/+cMlrPqMjUwtmNTI1"),
                InlineKeyboardButton(
                    "• 𝟷𝟾+ 🚫 •", url="https://t.me/+WCbiy07x2uVjNzVl"
                ),
            ],
            [
                InlineKeyboardButton(
                    "• ᴄɪɴᴇғʟɪx •", url="https://t.me/+QVmLP_hlHNw3M2I1"
                )
            ],
            [
                InlineKeyboardButton("⪻ ʙᴀᴄᴋ •", callback_data="back")
            ],
        ]

        reply_markup = InlineKeyboardMarkup(buttons)

        await callback_query.message.edit_text(
            text=script.CHANNELS.format(callback_query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML,
        )
        await callback_query.answer(MSG_ALRT)     
        
        
    elif callback_query.data == "close_data":
        try:
            user = callback_query.data.message.reply_to_message.from_user.id
        except:
            user = callback_query.from_user.id

        if int(user) != 0 and callback_query.data.from_user.id != int(user):
            return await callback_query.data.answer(script.ALRT_TXT, show_alert=True)

        await callback_query.data.answer("ᴛʜᴀɴᴋs ꜰᴏʀ ᴄʟᴏsᴇ")
        await callback_query.data.message.delete()

        try:
            await callback_query.data.message.reply_to_message.delete()
        except:
            pass
            
    elif callback_query.data == "rendr":
        await callback_query.answer(script.ALERT_MSG, show_alert=True)

    elif callback_query.data == "source":
        await callback_query.message.edit_text(text="● ◌ ◌")
        await callback_query.message.edit_text(text="● ● ◌")
        await callback_query.message.edit_text(text="● ● ●")

        buttons = [
        [
                InlineKeyboardButton("⪻ ʙᴀᴄᴋ", callback_data="about"),
                InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", callback_data="group_info"),
        ]
    ]

        reply_markup = InlineKeyboardMarkup(buttons)


        await callback_query.message.edit_text(
            text=script.SOURCE_TXT.format(
                callback_query.from_user.mention if callback_query.from_user else "User"
            ),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML,
            )
        await callback_query.answer(MSG_ALRT)


    elif callback_query.data == "spidey":
        await callback_query.message.edit_text(text="▰ ▱ ▱")
        await callback_query.message.edit_text(text="▰ ▰ ▱")
        await callback_query.message.edit_text(text="▰ ▰ ▰")

        buttons = [
            [
                InlineKeyboardButton("⪻ ʙᴀᴄᴋ", callback_data="features"),
                InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", callback_data="group_info"),
        ]
    ]

        reply_markup = InlineKeyboardMarkup(buttons)

        await callback_query.message.edit_text(
            text=script.OWNER_TEXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML,
    )
        await callback_query.answer(MSG_ALRT)