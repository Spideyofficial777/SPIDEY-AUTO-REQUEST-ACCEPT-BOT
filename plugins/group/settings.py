from pyrogram import filters
from Spidey.bot import SpideyBot as app
from database.database import db
from .helpers import is_admin, media_payload

ON = {'on', 'yes', 'true', '1'}
OFF = {'off', 'no', 'false', '0'}


async def admin_only(client, message):
    return bool(message.from_user and await is_admin(client, message.chat.id, message.from_user.id))


@app.on_message(filters.command(['welcome', 'goodbye', 'antiflood']) & filters.group)
async def setting(client, message):
    if not await admin_only(client, message):
        return
    if len(message.command) < 2:
        return await message.reply('ᴜsᴀɢᴇ: /welcome on|off')
    command, value = message.command[0].lower(), message.command[1].lower()
    if command == 'antiflood':
        try:
            number = int(value)
            if number != 0 and number < 3:
                raise ValueError
        except ValueError:
            return await message.reply('ᴜsᴀɢᴇ: /antiflood 0 ᴏʀ 3-20')
        await db.update_settings(message.chat.id, {'flood_limit': min(number, 20)})
    else:
        if value not in ON | OFF:
            return await message.reply(f'ᴜsᴀɢᴇ: /{command} on|off')
        await db.update_settings(message.chat.id, {command: value in ON})
    await message.reply('sᴇᴛᴛɪɴɢ ᴜᴘᴅᴀᴛᴇᴅ.')


@app.on_message(filters.command(['setwelcome', 'setgoodbye']) & filters.group)
async def set_greeting(client, message):
    if not await admin_only(client, message):
        return
    kind = 'welcome' if message.command[0].lower() == 'setwelcome' else 'goodbye'
    values = {}
    if message.reply_to_message:
        payload = media_payload(message.reply_to_message)
        if payload.get('text'):
            values[f'{kind}_text'] = payload['text']
        if payload.get('file_id') and payload.get('media_type') in ('photo', 'video', 'animation'):
            values[f'{kind}_media'] = payload['file_id']
            values[f'{kind}_media_type'] = payload['media_type']
    elif len(message.command) > 1:
        values[f'{kind}_text'] = message.text.split(None, 1)[1]
    else:
        return await message.reply(f'ʀᴇᴘʟʏ ᴛᴏ ᴛᴇxᴛ/ᴘʜᴏᴛᴏ/ᴠɪᴅᴇᴏ ᴏʀ ᴜsᴇ /set{kind} text')
    await db.update_settings(message.chat.id, values)
    await message.reply(f'{kind} sᴀᴠᴇᴅ.')


@app.on_message(filters.command(['cleanwelcome', 'cleangoodbye']) & filters.group)
async def clean_greeting(client, message):
    if not await admin_only(client, message):
        return
    kind = 'welcome' if message.command[0].lower() == 'cleanwelcome' else 'goodbye'
    await db.col.update_one({'_id': message.chat.id}, {'$unset': {
        f'{kind}_text': '', f'{kind}_media': '', f'{kind}_media_type': ''
    }})
    await message.reply(f'{kind} ʀᴇsᴇᴛ ᴛᴏ ᴅᴇꜰᴀᴜʟᴛ.')


@app.on_message(filters.command('greetingsettings') & filters.group)
async def greeting_settings(client, message):
    settings = await db.get_settings(message.chat.id)
    await message.reply(
        'ɢʀᴇᴇᴛɪɴɢ sᴇᴛᴛɪɴɢs\n'
        f'• ᴡᴇʟᴄᴏᴍᴇ: {"ᴏɴ" if settings.get("welcome", True) else "ᴏꜰꜰ"}\n'
        f'• ɢᴏᴏᴅʙʏᴇ: {"ᴏɴ" if settings.get("goodbye", True) else "ᴏꜰꜰ"}\n'
        f'• ᴀɴᴛɪꜰʟᴏᴏᴅ: {settings.get("flood_limit", 0)}\n'
        f'• ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ: {"ᴏɴ" if settings.get("auto_delete", True) else "ᴏꜰꜰ"}'
    )
