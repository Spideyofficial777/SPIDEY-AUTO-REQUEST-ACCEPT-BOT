import secrets
import time

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .group_registry import manageable_groups

_PENDING = {}
_TTL = 600


def create_selection(user_id, payload):
    token = secrets.token_urlsafe(6)
    _PENDING[token] = {
        "user_id": user_id,
        "payload": payload,
        "expires": time.monotonic() + _TTL,
    }
    return token


def get_selection(token, user_id, consume=False):
    item = _PENDING.get(token)
    if not item:
        return None
    if item["user_id"] != user_id or item["expires"] < time.monotonic():
        _PENDING.pop(token, None)
        return None
    if consume:
        _PENDING.pop(token, None)
    return item["payload"]


async def resolve_groups(client, user_id):
    return await manageable_groups(client, user_id)


def group_keyboard(prefix, token, groups):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(title[:50], callback_data=f"{prefix}:{token}:{chat_id}")]
        for chat_id, title in groups[:50]
    ])
