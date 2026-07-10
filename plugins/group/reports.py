from pyrogram import filters, enums
from Spidey.bot import SpideyBot as app
from .helpers import is_admin


@app.on_message((filters.command('report') | filters.regex(r'(?i)(?:^|\s)@admins?(?:\s|$)')) & filters.group)
async def report(client, message):
    if not message.from_user or await is_admin(client, message.chat.id, message.from_user.id):
        return
    mentions = []
    async for member in client.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        if not member.user.is_bot:
            mentions.append(f'<a href="tg://user?id={member.user.id}">\u2064</a>')
    if not mentions:
        return
    await message.reply('ʀᴇᴘᴏʀᴛ sᴇɴᴛ ' + ''.join(mentions), parse_mode=enums.ParseMode.HTML)
