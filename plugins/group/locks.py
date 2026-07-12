import re
import asyncio
from pyrogram import filters
from Spidey.bot import NexGuardBot as app
from database.database import db
from .helpers import is_admin

TYPES = {'links', 'usernames', 'photo', 'video', 'sticker', 'gif', 'voice', 'audio', 'document', 'poll', 'forward', 'contact', 'location'}

DEFAULT_LOCKED_TYPES = {'links', 'usernames'}


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
        r'https?://\S+'
        r'|www\.\S+'
        r'|t\.me/\S+'
        r'|telegram\.me/\S+'
        r'|telegram\.dog/\S+'
        r'|discord\.gg/\S+'
        r'|discord\.com/invite/\S+'
        r'|wa\.me/\S+'
        r'|chat\.whatsapp\.com/\S+'
        r'|bit\.ly/\S+'
        r'|tinyurl\.com/\S+'
        r'|t\.co/\S+'
        r'|cutt\.ly/\S+'
        r'|is\.gd/\S+'
        r'|(?:[\w-]+\.)+(?:'
            r'com|net|org|io|co|in|me|tv'
            r'|info|biz|app|dev|xyz|gg'
            r'|online|site|web|tech|store'
            r'|live|stream|link|click|space'
            r'|today|news|shop|pro|top|club'
            r'|dog|gd|ly|us|uk|ca|de|fr|ru|cn|jp'
            r'|edu|gov|mil'
            r'|[a-z]{2,3}'
        r')(?:/\S*)?'
    r')',
    re.IGNORECASE,
)


USERNAME_PATTERN = re.compile(r'@(?!admins?\b)\w{4,}', re.IGNORECASE)


def _contains_link(text: str) -> bool:
    """True if `text` (already zero-width-stripped) has a link in any form."""
    if not text:
        return False
    if MARKDOWN_LINK_PATTERN.search(text):
        return True
    if HTML_LINK_PATTERN.search(text):
        return True
    if LINK_PATTERN.search(text):
        return True
    return False


@app.on_message(filters.command(['lock', 'unlock']) & filters.group)
async def lock_cmd(client, message):
    if not message.from_user or not await is_admin(client, message.chat.id, message.from_user.id):
        return
    if len(message.command) < 2 or message.command[1].lower() not in TYPES:
        return await message.reply('ᴛʏᴘᴇs: ' + ', '.join(sorted(TYPES)))
    key = message.command[1].lower()
    await db.group_db.set_lock(message.chat.id, key, message.command[0].lower() == 'lock')
    await message.reply(f'{key} sᴇᴛᴛɪɴɢ ᴜᴘᴅᴀᴛᴇᴅ.')


@app.on_message(filters.command('locks') & filters.group)
async def lock_status(client, message):
    locks = await db.group_db.get_locks(message.chat.id)
    lines = [
        f'• {key}: {"ʟᴏᴄᴋᴇᴅ" if locks.get(key, key in DEFAULT_LOCKED_TYPES) else "ᴜɴʟᴏᴄᴋᴇᴅ"}'
        for key in sorted(TYPES)
    ]
    await message.reply('ʟᴏᴄᴋ sᴛᴀᴛᴜs\n' + '\n'.join(lines))


@app.on_message(filters.group, group=5)
async def enforce(client, message):
    if not message.from_user or await is_admin(client, message.chat.id, message.from_user.id):
        return
    locks = await db.group_db.get_locks(message.chat.id)

    raw_text = message.text or message.caption or ''
    text = _strip_zero_width(raw_text)

    kind = None
    if text and _contains_link(text):
        kind = 'links'
    elif text and USERNAME_PATTERN.search(text):
        kind = 'usernames'
    elif message.photo: kind = 'photo'
    elif message.video: kind = 'video'
    elif message.sticker: kind = 'sticker'
    elif message.animation: kind = 'gif'
    elif message.voice: kind = 'voice'
    elif message.audio: kind = 'audio'
    elif message.document: kind = 'document'
    elif message.poll: kind = 'poll'
    elif getattr(message, 'forward_date', None): kind = 'forward'
    elif message.contact: kind = 'contact'
    elif message.location: kind = 'location'

    if not kind:
        return

    if not locks.get(kind, kind in DEFAULT_LOCKED_TYPES):
        return

    try:
        await message.delete()
    except Exception:
        return

    if kind in ('links', 'usernames'):
        warning_text = (
            "<b>❌ ʟɪɴᴋꜱ ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ.</b>"
            if kind == 'links' else
            "<b>❌ @ᴜꜱᴇʀɴᴀᴍᴇ ᴍᴇɴᴛɪᴏɴꜱ ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ.</b>"
        )
        try:
            warn = await message.reply(warning_text)
            await asyncio.sleep(60)
            await warn.delete()
        except Exception:
            pass
