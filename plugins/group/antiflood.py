import time
from collections import defaultdict, deque
from pyrogram import filters
from pyrogram.types import ChatPermissions
from Spidey.bot import SpideyBot as app
from database.database import db
from .helpers import is_admin, until_date

_hits = defaultdict(lambda: deque(maxlen=25))


@app.on_message(filters.group, group=4)
async def antiflood(client, message):
    if not message.from_user or await is_admin(client, message.chat.id, message.from_user.id):
        return
    settings = await db.get_settings(message.chat.id)
    limit = int(settings.get('flood_limit', 0) or 0)
    if limit < 3:
        return
    key = (message.chat.id, message.from_user.id)
    now = time.monotonic()
    queue = _hits[key]
    queue.append(now)
    while queue and now - queue[0] > 10:
        queue.popleft()
    if len(queue) >= limit:
        seconds = int(settings.get('flood_mute_seconds', 300) or 300)
        try:
            await client.restrict_chat_member(message.chat.id, message.from_user.id, ChatPermissions(), until_date=until_date(seconds))
            await db.group_db.set_punishment(message.chat.id, message.from_user.id, 'mute', seconds, reason='antiflood')
            queue.clear()
            await message.reply(f'{message.from_user.mention} ᴍᴜᴛᴇᴅ ꜰᴏʀ ꜰʟᴏᴏᴅɪɴɢ.')
        except Exception:
            queue.clear()
