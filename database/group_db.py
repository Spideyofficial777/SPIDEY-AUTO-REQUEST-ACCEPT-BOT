from datetime import datetime, timedelta, timezone


class GroupDB:
    def __init__(self, db):
        self.settings = db['Settings']
        self.warns = db['group_warnings']
        self.punishments = db['group_punishments']
        self.filters = db['group_filters']
        self.notes = db['group_notes']
        self.locks = db['group_locks']
        self.blacklist = db['group_blacklist']
        self.pending_filters = db['group_pending_filters']

    async def ensure_indexes(self):
        await self.warns.create_index([('chat_id', 1), ('user_id', 1)], unique=True)
        await self.punishments.create_index([('chat_id', 1), ('user_id', 1), ('kind', 1)], unique=True)
        await self.filters.create_index([('chat_id', 1), ('key', 1)], unique=True)
        await self.notes.create_index([('chat_id', 1), ('key', 1)], unique=True)
        await self.pending_filters.create_index('expires_at', expireAfterSeconds=0)

    async def add_warning(self, chat_id, user_id, admin_id, reason=''):
        item = {'admin_id': admin_id, 'reason': reason, 'at': datetime.now(timezone.utc)}
        await self.warns.update_one({'chat_id': chat_id, 'user_id': user_id}, {'$push': {'items': item}}, upsert=True)
        return await self.warning_count(chat_id, user_id)

    async def warning_count(self, chat_id, user_id):
        doc = await self.warns.find_one({'chat_id': chat_id, 'user_id': user_id})
        return len(doc.get('items', [])) if doc else 0

    async def remove_last_warning(self, chat_id, user_id):
        doc = await self.warns.find_one({'chat_id': chat_id, 'user_id': user_id})
        items = list(doc.get('items', [])) if doc else []
        if items:
            items.pop()
            if items:
                await self.warns.update_one({'chat_id': chat_id, 'user_id': user_id}, {'$set': {'items': items}})
            else:
                await self.warns.delete_one({'chat_id': chat_id, 'user_id': user_id})
        return len(items)

    async def reset_warnings(self, chat_id, user_id):
        await self.warns.delete_one({'chat_id': chat_id, 'user_id': user_id})

    async def set_punishment(self, chat_id, user_id, kind, seconds=None, admin_id=None, reason=''):
        until = datetime.now(timezone.utc) + timedelta(seconds=seconds) if seconds else None
        await self.punishments.update_one(
            {'chat_id': chat_id, 'user_id': user_id, 'kind': kind},
            {'$set': {'until': until, 'admin_id': admin_id, 'reason': reason, 'updated_at': datetime.now(timezone.utc)}},
            upsert=True,
        )

    async def clear_punishment(self, chat_id, user_id, kind):
        await self.punishments.delete_one({'chat_id': chat_id, 'user_id': user_id, 'kind': kind})


    async def create_pending_filter(self, token, user_id, key, data, expires_at):
        await self.pending_filters.update_one(
            {'token': token},
            {'$set': {'user_id': user_id, 'key': key, 'data': data, 'expires_at': expires_at}},
            upsert=True,
        )

    async def get_pending_filter(self, token, user_id):
        return await self.pending_filters.find_one({'token': token, 'user_id': user_id})

    async def delete_pending_filter(self, token, user_id):
        await self.pending_filters.delete_one({'token': token, 'user_id': user_id})

    async def set_filter(self, chat_id, key, data):
        await self.filters.update_one({'chat_id': chat_id, 'key': key}, {'$set': {'data': data}}, upsert=True)

    async def delete_filter(self, chat_id, key):
        return (await self.filters.delete_one({'chat_id': chat_id, 'key': key})).deleted_count

    async def list_filters(self, chat_id):
        return [d['key'] async for d in self.filters.find({'chat_id': chat_id}, {'key': 1}).sort('key', 1)]

    async def match_filter(self, chat_id, text):
        import re
        docs = [d async for d in self.filters.find({'chat_id': chat_id})]
        docs.sort(key=lambda d: len(d.get('key', '')), reverse=True)
        for doc in docs:
            key = doc.get('key', '')
            if key and re.search(r'(?<!\w)' + re.escape(key) + r'(?!\w)', text, re.I):
                return doc.get('data')
        return None

    async def set_note(self, chat_id, key, data):
        await self.notes.update_one({'chat_id': chat_id, 'key': key}, {'$set': {'data': data}}, upsert=True)

    async def get_note(self, chat_id, key):
        doc = await self.notes.find_one({'chat_id': chat_id, 'key': key})
        return doc.get('data') if doc else None

    async def delete_note(self, chat_id, key):
        return (await self.notes.delete_one({'chat_id': chat_id, 'key': key})).deleted_count

    async def list_notes(self, chat_id):
        return [d['key'] async for d in self.notes.find({'chat_id': chat_id}, {'key': 1}).sort('key', 1)]

    async def set_lock(self, chat_id, key, value):
        await self.locks.update_one({'chat_id': chat_id}, {'$set': {key: value}}, upsert=True)

    async def get_locks(self, chat_id):
        return await self.locks.find_one({'chat_id': chat_id}) or {}

    async def blacklist_word(self, chat_id, word, add=True):
        op = '$addToSet' if add else '$pull'
        await self.blacklist.update_one({'chat_id': chat_id}, {op: {'words': word}}, upsert=True)

    async def get_blacklist(self, chat_id):
        doc = await self.blacklist.find_one({'chat_id': chat_id})
        return doc.get('words', []) if doc else []
