import re
from datetime import datetime, timedelta, timezone
from html import escape
from pyrogram import enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

DURATION_RE = re.compile(r'^([1-9]\d*)(s|m|h|d|w)$', re.I)
BUTTON_RE = re.compile(r'\[([^\]]+)\]\(buttonurl\s*:\s*(https?://[^)\s]+)\s*\)', re.I)


def parse_duration(value):
    if not value:
        return None
    match = DURATION_RE.fullmatch(value.strip())
    if not match:
        return None
    number = int(match.group(1))
    return number * {'s': 1, 'm': 60, 'h': 3600, 'd': 86400, 'w': 604800}[match.group(2).lower()]


def until_date(seconds):
    return datetime.now(timezone.utc) + timedelta(seconds=seconds)


async def is_admin(client, chat_id, user_id):
    if not user_id:
        return False
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER)
    except Exception:
        return False


async def is_owner(client, chat_id, user_id):
    if not user_id:
        return False
    try:
        return (await client.get_chat_member(chat_id, user_id)).status == enums.ChatMemberStatus.OWNER
    except Exception:
        return False


async def can_target(client, chat_id, actor_id, target_id):
    if actor_id == target_id:
        return False, 'ʏᴏᴜ ᴄᴀɴɴᴏᴛ ᴜsᴇ ᴛʜɪs ᴀᴄᴛɪᴏɴ ᴏɴ ʏᴏᴜʀsᴇʟꜰ.'
    if await is_owner(client, chat_id, target_id):
        return False, 'ɢʀᴏᴜᴘ ᴏᴡɴᴇʀ ᴄᴀɴɴᴏᴛ ʙᴇ ᴛᴀʀɢᴇᴛᴇᴅ.'
    if await is_admin(client, chat_id, target_id) and not await is_owner(client, chat_id, actor_id):
        return False, 'ᴏɴʟʏ ᴛʜᴇ ᴏᴡɴᴇʀ ᴄᴀɴ ᴛᴀʀɢᴇᴛ ᴀɴ ᴀᴅᴍɪɴ.'
    return True, None


def target_user(message):
    if message.reply_to_message and message.reply_to_message.from_user:
        return message.reply_to_message.from_user
    return None


def command_reason(message, duration_command=False):
    start = 2 if duration_command else 1
    return ' '.join(message.command[start:]).strip()


def render_template(template, user, chat):
    values = {
        'mention': user.mention,
        'first': escape(user.first_name or ''),
        'username': '@' + user.username if user.username else '',
        'id': user.id,
        'chat': escape(chat.title or ''),
        'members': getattr(chat, 'members_count', '') or '',
    }
    try:
        return template.format(**values)
    except (KeyError, ValueError):
        return template


def parse_buttons(text):
    if not text:
        return text, None
    rows = []
    for label, url in BUTTON_RE.findall(text):
        rows.append([InlineKeyboardButton(label.strip(), url=url.strip())])
    clean = BUTTON_RE.sub('', text)
    clean = re.sub(r'\n{3,}', '\n\n', clean).strip()
    return clean, InlineKeyboardMarkup(rows) if rows else None


def media_payload(message):
    data = {'text': message.text or message.caption or ''}
    for attr in ('sticker', 'photo', 'video', 'animation', 'document', 'audio', 'voice'):
        media = getattr(message, attr, None)
        if media:
            data['media_type'] = attr
            data['file_id'] = media.file_id
            break
    return data


async def send_payload(message, data):
    text, markup = parse_buttons(data.get('text') or '')
    media_type, file_id = data.get('media_type'), data.get('file_id')
    if media_type == 'sticker':
        return await message.reply_sticker(file_id)
    if media_type and file_id:
        method = getattr(message, f'reply_{media_type}', None)
        if method:
            kwargs = {'reply_markup': markup}
            if media_type not in ('voice',):
                kwargs['caption'] = text or None
            return await method(file_id, **kwargs)
    if text:
        return await message.reply_text(text, reply_markup=markup)
