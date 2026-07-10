from pymongo import MongoClient
from configs import * #Spidey
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone

client = MongoClient(DATABASE_URI)
mydb = client[DATABASE_NAME]

users = client['main']['users']
groups = client['main']['groups']


class DataBase:
    def __init__(self, uri):
        client = AsyncIOMotorClient(uri)
        self.col = client['BotDB']['Settings']
        self.grp = client['BotDB']['groups']
        from database.group_db import GroupDB
        self.group_db = GroupDB(client['BotDB'])
        
    async def get_settings(self, id):
        default = {
            'welcome': True,
            'auto_delete': True
        }

        try:
            settings = await self.col.find_one({"_id": id})
            if not settings:
                return default
            default.update(settings)
            return default
        except Exception as e:
            print(f"[get_settings error]: {e}")
            return default


    async def get_chat(self, chat_id):
        return await self.grp.find_one({"id": chat_id})

    async def add_chat(self, chat_id, title, chat_type=None, bot_status=None):
        now = datetime.now(timezone.utc)
        values = {
            "title": title,
            "last_seen": now,
            "updated_at": now,
        }
        if chat_type is not None:
            values["chat_type"] = str(chat_type)
        if bot_status is not None:
            values["bot_status"] = str(bot_status)

        await self.grp.update_one(
            {"id": chat_id},
            {
                "$set": values,
                "$setOnInsert": {
                    "created_at": now,
                    "chat_status": {"is_disabled": False, "reason": ""},
                },
            },
            upsert=True,
        )

    async def list_registered_groups(self):
        cursor = self.grp.find(
            {"chat_status.is_disabled": {"$ne": True}},
            {"id": 1, "title": 1, "chat_type": 1, "bot_status": 1, "last_seen": 1},
        )
        return [doc async for doc in cursor]

    async def update_chat_validation(self, chat_id, bot_status=None, title=None, error=None):
        values = {
            "validated_at": datetime.now(timezone.utc),
            "validation_error": error,
        }
        if bot_status is not None:
            values["bot_status"] = str(bot_status)
        if title is not None:
            values["title"] = title
        await self.grp.update_one({"id": chat_id}, {"$set": values})

    async def update_settings(self, chat_id, values):
        await self.col.update_one({"_id": chat_id}, {"$set": values}, upsert=True)

    async def reset_group_settings(self, chat_id):
        await self.col.delete_one({"_id": chat_id})

    async def get_banned(self):
        users = self.col.find({'ban_status.is_banned': True})
        chats = self.grp.find({'chat_status.is_disabled': True})
        b_chats = [chat['id'] async for chat in chats]
        b_users = [user['id'] async for user in users]
        return b_users, b_chats                   
def already_db(user_id):
    user = users.find_one({"user_id": str(user_id)})
    return bool(user)

def already_dbg(chat_id):
    group = groups.find_one({"chat_id": str(chat_id)})
    return bool(group)

def add_user(user_id, name):
    if already_db(user_id):
        return
    users.insert_one({"user_id": str(user_id), "name": name, "ban_status": {"is_banned": False}})

def remove_user(user_id):
    if not already_db(user_id):
        return
    users.delete_one({"user_id": str(user_id)})

def add_group(chat_id):
    if already_dbg(chat_id):
        return
    groups.insert_one({"chat_id": str(chat_id)})

def all_users():
    return users.count_documents({})

def all_groups():
    return groups.count_documents({})

def get_all_users():
    return list(users.find({}, {"user_id": 1, "name": 1, "_id": 0}))
    
def add_user(user_id, name):
    if already_db(user_id):
        users.update_one({"user_id": str(user_id)}, {"$set": {"name": name}})
        return
    users.insert_one({"user_id": str(user_id), "name": name, "ban_status": {"is_banned": False}})
    
def already_db(user_id):
    """Checks if the user is already in the MongoDB database"""
    return users.find_one({"user_id": str(user_id)}) is not None
    
"""    def new_group(self, id, title):
        return dict(
            id = id,
            title = title,
            chat_status=dict(
                is_disabled=False,
                reason=""
            )
        )"""
        
db = DataBase(DATABASE_URI)            