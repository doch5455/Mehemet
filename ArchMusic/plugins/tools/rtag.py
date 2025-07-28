import asyncio
import random
from pyrogram import filters
from pyrogram.types import Message
from config import BANNED_USERS
from ArchMusic import app

# Renk emojileri listesi
RENKLER = [
    "🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "🟤",
    "⚫", "⚪", "🟥", "🟧", "🟨", "🟩", "🟦",
    "🟪", "🟫", "⬛", "⬜", "🔶", "🔷", "🔸",
    "🔹", "✨", "🌈"
]

# Etiketleme durumu kontrolü için sözlük
ETIKET_DURUM = {}

@app.on_message(filters.command("rtag") & filters.group & ~BANNED_USERS)
async def rtag(client, message: Message):
    chat_id = message.chat.id
    ETIKET_DURUM[chat_id] = True
    etiketlenen = 0
    atlanilan = 0

    await message.reply("🎨 Renkli etiketleme başlıyor... Durdurmak için /cancel_rtag yazın.")

    async for u in app.get_chat_members(chat_id):
        if not ETIKET_DURUM.get(chat_id):
            break
        try:
            if u.user.is_deleted or u.user.is_bot:
                atlanilan += 1
                continue
            renk = random.choice(RENKLER)
            await message.reply(
                f"{renk} [{u.user.first_name}](tg://user?id={u.user.id})", quote=False
            )
            etiketlenen += 1
            await asyncio.sleep(2)  # Yavaşlatma süresi (spam koruma)
        except Exception:
            atlanilan += 1
            continue

    await message.reply(
        f"🎨 Renkli etiketleme tamamlandı!\n"
        f"✅ Etiketlenen: `{etiketlenen}`\n"
        f"❌ Atlanılan: `{atlanilan}`\n"
        f"🏁 Toplam İşlem: `{etiketlenen + atlanilan}`"
    )
    ETIKET_DURUM[chat_id] = False

@app.on_message(filters.command("cancel_rtag") & filters.group & ~BANNED_USERS)
async def cancel_rtag(client, message: Message):
    chat_id = message.chat.id
    ETIKET_DURUM[chat_id] = False
    await message.reply("❌ Renkli etiketleme işlemi durduruldu.")
