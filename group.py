from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
import traceback
from configs import * # LOG_CHANNEL
from Script import script
from database.database import db
from utils import *
import re


ZERO_WIDTH_PATTERN = re.compile(
    r'[\u200b-\u200f\u202a-\u202e\u2060-\u2064\ufeff\xa0]'
)


def _strip_zero_width(text: str) -> str:
    """Remove invisible/zero-width unicode characters used to bypass filters."""
    if not text:
        return ""
    return ZERO_WIDTH_PATTERN.sub("", text)


MARKDOWN_LINK_PATTERN = re.compile(
    r'\[[^\[\]]*\]\(\s*(https?://[^\s\)]+)\s*\)',
    re.IGNORECASE,
)

HTML_LINK_PATTERN = re.compile(
    r'<a\b[^>]*\bhref\s*=\s*["\']([^"\']+)["\']',
    re.IGNORECASE,
)

LINK_PATTERN = re.compile(
    r'(?:'
        r'https?://\S+'                       # explicit http/https URL
        r'|www\.\S+'                          # www. prefix
        r'|t\.me/\S+'                         # Telegram link
        r'|telegram\.me/\S+'                  # Telegram alt domain
        r'|telegram\.dog/\S+'                 # Telegram alt domain
        r'|discord\.gg/\S+'                   # Discord invite (short)
        r'|discord\.com/invite/\S+'           # Discord invite (long)
        r'|wa\.me/\S+'                        # WhatsApp click-to-chat
        r'|chat\.whatsapp\.com/\S+'           # WhatsApp group invite
        r'|bit\.ly/\S+'                       # shortener
        r'|tinyurl\.com/\S+'                  # shortener
        r'|t\.co/\S+'                         # shortener
        r'|cutt\.ly/\S+'                      # shortener
        r'|is\.gd/\S+'                        # shortener
        r'|(?:[\w-]+\.)+(?:'                  # bare domain: one-or-more labels +
            r'com|net|org|io|co|in|me|tv'
            r'|info|biz|app|dev|xyz|gg'
            r'|online|site|web|tech|store'
            r'|live|stream|link|click|space'
            r'|today|news|shop|pro|top|club'
            r'|dog|gd|ly|us|uk|ca|de|fr|ru|cn|jp'
            r'|edu|gov|mil'
            r'|[a-z]{2,3}'                    # generic ccTLD catch-all
        r')(?:/\S*)?'                          # optional path
    r')',
    re.IGNORECASE,
)

USERNAME_PATTERN = re.compile(r'@(?!admins?\b)\w{4,}', re.IGNORECASE)


def _contains_link(text: str) -> bool:
    """
    Returns True if `text` contains a link in ANY form:
    plain URL, bare domain, markdown link, or HTML <a href> link.
    `text` should already be zero-width-stripped by the caller.
    """
    if not text:
        return False
    if MARKDOWN_LINK_PATTERN.search(text):
        return True
    if HTML_LINK_PATTERN.search(text):
        return True
    if LINK_PATTERN.search(text):
        return True
    return False


from Spidey.bot import SpideyBot as Client

@Client.on_message(filters.new_chat_members & filters.group)
async def save_group(bot, message):
    for u in message.new_chat_members:
        # If bot itself is added
        if u.id == temp.ME:
            if not await db.get_chat(message.chat.id):
                total = await bot.get_chat_members_count(message.chat.id)
                r_j = message.from_user.mention if message.from_user else "Anonymous"
                await bot.send_message(
                    LOG_CHANNEL,
                    script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, r_j)
                )
                await db.add_chat(message.chat.id, message.chat.title)

            if message.chat.id in temp.BANNED_CHATS:
                buttons = [[
                    InlineKeyboardButton('• ᴄᴏɴᴛᴀᴄᴛ ꜱᴜᴘᴘᴏʀᴛ •', url='https://t.me/hacker_x_official_777')
                ]]
                reply_markup = InlineKeyboardMarkup(buttons)
                k = await message.reply(
                    text='<b>ᴄʜᴀᴛ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ 🐞\n\nᴍʏ ᴀᴅᴍɪɴꜱ ʜᴀꜱ ʀᴇꜱᴛʀɪᴄᴛᴇᴅ ᴍᴇ ꜰʀᴏᴍ ᴡᴏʀᴋɪɴɢ ʜᴇʀᴇ ! ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ ᴀʙᴏᴜᴛ ɪᴛ ᴄᴏɴᴛᴀᴄᴛ ꜱᴜᴘᴘᴏʀᴛ.</b>',
                    reply_markup=reply_markup,
                )
                try:
                    await k.pin()
                except:
                    pass
                await bot.leave_chat(message.chat.id)
                return

            buttons = [[
                InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ', url='https://telegram.me/spideyofficial777'),
                InlineKeyboardButton('ᴜᴘᴅᴀᴛᴇꜱ', url='https://telegram.me/spideyofficial_777')
            ]]
            reply_markup = InlineKeyboardMarkup(buttons)
            await message.reply_text(
                text=f"<b>Thankyou For Adding Me In {message.chat.title} ❣️\n\nIf you have any questions & doubts about using me contact support.</b>",
                reply_markup=reply_markup
            )

        # For all users who join (via any method)
        settings = await get_settings(message.chat.id)
        if settings["welcome"]:
            if temp.MELCOW.get('welcome'):
                try:
                    await temp.MELCOW['welcome'].delete()
                except:
                    pass

            temp.MELCOW['welcome'] = await message.reply_photo(
                photo=MELCOW_VID,
                caption=script.MELCOW_ENG.format(u.mention, message.chat.title),
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton('• ᴊᴏɪɴ ᴍʏ ᴜᴘᴅᴀᴛᴇꜱ •', url='https://t.me/+QVmLP_hlHNw3M2I1/')
                ]]),
                parse_mode=enums.ParseMode.HTML
            )

            if settings["auto_delete"]:
                await asyncio.sleep(600)
                await temp.MELCOW['welcome'].delete()


@Client.on_message(filters.left_chat_member & filters.group)
async def user_left(bot, message):
    left_user = message.left_chat_member
    settings = await get_settings(message.chat.id)
    if settings["welcome"]:
        buttons = [[
            InlineKeyboardButton("• ᴊᴏɪɴ ᴍʏ ᴜᴘᴅᴀᴛᴇꜱ •", url="https://t.me/spideyofficial_777")
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=MELCOW_VID,
            caption=f"<b>{left_user.mention} has left the group {message.chat.title}.</b>",
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )



@Client.on_message(filters.command('leave') & filters.user(ADMINS))
async def leave_a_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a chat id')
    chat = message.command[1]
    try:
        chat = int(chat)
    except:
        chat = chat
    try:
        buttons = [[
                  InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ', url='https://telegram.me/spideyofficialupdatez')
                  ]]
        reply_markup=InlineKeyboardMarkup(buttons)
        await bot.send_message(
            chat_id=chat,
            text='<b>ʜᴇʟʟᴏ ꜰʀɪᴇɴᴅꜱ, \nᴍʏ ᴀᴅᴍɪɴ ʜᴀꜱ ᴛᴏʟᴅ ᴍᴇ ᴛᴏ ʟᴇᴀᴠᴇ ꜰʀᴏᴍ ɢʀᴏᴜᴘ, ꜱᴏ ɪ ʜᴀᴠᴇ ᴛᴏ ɢᴏ !/nɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴀᴅᴅ ᴍᴇ ᴀɢᴀɪɴ ᴄᴏɴᴛᴀᴄᴛ ꜱᴜᴘᴘᴏʀᴛ.</b>',
            reply_markup=reply_markup,
        )

        await bot.leave_chat(chat)
        await message.reply(f"left the chat `{chat}`")
    except Exception as e:
        await message.reply(f'Error - {e}')

@Client.on_message(filters.text & filters.group)
async def group_text_handler(client, message):
    try:
        is_admin = await is_check_admin(client, message.chat.id, message.from_user.id)

        clean_text = _strip_zero_width(message.text)

        if _contains_link(clean_text):
            if is_admin:
                return
            await message.delete()
            warn = await message.reply("<b>❌ ʟɪɴᴋꜱ ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ.</b>")
            try:
                await asyncio.sleep(60)
                await warn.delete()
            except:
                pass
            return

        elif USERNAME_PATTERN.search(clean_text):
            if is_admin:
                return
            await message.delete()
            warn = await message.reply("<b>❌ @ᴜꜱᴇʀɴᴀᴍᴇ ᴍᴇɴᴛɪᴏɴꜱ ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ.</b>")
            try:
                await asyncio.sleep(60)
                await warn.delete()
            except:
                pass
            return

        # @admin / @admins REPORT
        elif '@admin' in message.text.lower() or '@admins' in message.text.lower():
            if is_admin:
                return
            admins = []
            async for member in client.get_chat_members(chat_id=message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
                if not member.user.is_bot:
                    admins.append(member.user.id)
                    if member.status == enums.ChatMemberStatus.OWNER:
                        try:
                            if message.reply_to_message:
                                sent_msg = await message.reply_to_message.forward(member.user.id)
                                await sent_msg.reply_text(
                                    f"#Attention\n★ User: {message.from_user.mention}\n★ Group: {message.chat.title}\n\n★ <a href={message.reply_to_message.link}>Go to message</a>",
                                    disable_web_page_preview=True
                                )
                            else:
                                sent_msg = await message.forward(member.user.id)
                                await sent_msg.reply_text(
                                    f"#Attention\n★ User: {message.from_user.mention}\n★ Group: {message.chat.title}\n\n★ <a href={message.link}>Go to message</a>",
                                    disable_web_page_preview=True
                                )
                        except Exception as e:
                            
                            pass
            hidden_mentions = ''.join([f'[\u2064](tg://user?id={user_id})' for user_id in admins])
            await message.reply_text('<code>Report sent</code>' + hidden_mentions)

    except Exception as e:

        pass
           
