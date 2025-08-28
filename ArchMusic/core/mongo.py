
from motor.motor_asyncio import AsyncIOMotorClient as _mongo_client_
from pymongo import MongoClient
from pyrogram import Client, filters
from datetime import datetime

import config

from ..logging import LOGGER

TEMP_MONGODB = "mongodb+srv://userbot:userbot@userbot.nrzfzdf.mongodb.net/?retryWrites=true&w=majority"


if config.MONGO_DB_URI is None:
    LOGGER(__name__).warning(
        "No MONGO DB URL found.. Your Bot will work on ArchMusic's Database"
    )
    temp_client = Client(
        "ArchMusic",
        bot_token=config.BOT_TOKEN,
        api_id=config.API_ID,
        api_hash=config.API_HASH,
    )
    temp_client.start()
    info = temp_client.get_me()
    username = info.username
    temp_client.stop()
    _mongo_async_ = _mongo_client_(TEMP_MONGODB)
    _mongo_sync_ = MongoClient(TEMP_MONGODB)
    mongodb = _mongo_async_[username]
    pymongodb = _mongo_sync_[username]
else:
    _mongo_async_ = _mongo_client_(config.MONGO_DB_URI)
    _mongo_sync_ = MongoClient(config.MONGO_DB_URI)
    mongodb = _mongo_async_["che"]
    pymongodb = _mongo_sync_["ArchMusic"]

# --- Grup koleksiyonu ---
groups_collection_sync = pymongodb["groups"]  # Sync
groups_collection_async = mongodb["groups"]   # Async

# --- Pyrogram bot örneği ---
bot = Client(
    "ArchMusic",
    bot_token=config.BOT_TOKEN,
    api_id=config.API_ID,
    api_hash=config.API_HASH,
)

# Grup mesajlarını yakalayıp MongoDB'ye ekleme
@bot.on_message(filters.group)
async def add_group(client, message):
    group_id = message.chat.id
    group_name = message.chat.title

    existing = await groups_collection_async.count_documents({"group_id": group_id})
    if existing == 0:
        await groups_collection_async.insert_one({
            "group_id": group_id,
            "group_name": group_name,
            "added_at": datetime.utcnow()
        })
        print(f"Yeni grup eklendi: {group_name} ({group_id})")

    total_groups = await groups_collection_async.count_documents({})
    print(f"Botun gerçek bağlı olduğu toplam grup sayısı: {total_groups}")

# Botun bir gruptan çıkarıldığını veya kaldırıldığını kontrol etme
@bot.on_my_chat_member()
async def remove_group(client, chat_member_update):
    status = chat_member_update.new_chat_member.status
    chat_id = chat_member_update.chat.id

    if status in ["kicked", "left"]:
        result = await groups_collection_async.delete_one({"group_id": chat_id})
        if result.deleted_count > 0:
            print(f"Bot bu gruptan çıkarıldı, MongoDB kaydı silindi: {chat_member_update.chat.title}")

    total_groups = await groups_collection_async.count_documents({})
    print(f"Botun gerçek bağlı olduğu toplam grup sayısı: {total_groups}")

# --- Yeni komut: /gruplar ile Telegram mesajında liste ---
@bot.on_message(filters.command("gruplar") & filters.user(config.OWNER_ID))
async def show_groups(client, message):
    groups = await groups_collection_async.find().to_list(length=1000)  # Maksimum 1000 grup
    total = len(groups)
    
    if total == 0:
        await message.reply("Botun bağlı olduğu grup bulunamadı.")
        return

    text = f"📊 Botun Bağlı Olduğu Gruplar ({total}):\n\n"
    for idx, g in enumerate(groups, start=1):
        text += f"{idx}. {g['group_name']} (`{g['group_id']}`)\n"

    await message.reply(text)
    print(f"Toplam grup sayısı: {total}")
