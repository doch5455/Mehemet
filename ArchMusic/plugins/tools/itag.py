from pyrogram import filters
from pyrogram.types import Message
from config import BANNED_USERS
from ArchMusic import app
import random

# Emoji listesi
EMOJIS = [
    "🔥", "💥", "🌟", "✨", "🎯", "🧲", "🎉", "🪄",
    "🌀", "🌈", "🫧", "🍀", "🌻", "🦋", "🌙", "⚡",
    "💫", "🧿", "🫶", "🌸", "🎈", "🍁", "☄️", "🌼"
]

# Cancel edilen kullanıcılar
cancel_users = set()

# /cancel komutu
@app.on_message(filters.command("cancel") & filters.group & ~BANNED_USERS)
async def cancel_itag(client, message: Message):
    cancel_users.add(message.from_user.id)
    await message.reply("❌ İşlem iptal edildi. Etiketleme durduruldu.")

# /itag komutu
@app.on_message(filters.command("itag") & filters.group & ~BANNED_USERS)
async def itag_command(client, message: Message):
    user_id = message.from_user.id

    if user_id in cancel_users:
        cancel_users.remove(user_id)
        return await message.reply("⛔ Etiketleme işlemi iptal edilmişti.")

    if not message.reply_to_message or not message.reply_to_message.from_user:
        return await message.reply("❗ Lütfen etiketlemek istediğiniz bir kullanıcıyı yanıtlayın.")

    hedef_kullanici = message.reply_to_message.from_user
    emoji = random.choice(EMOJIS)

    etiketlenen = 0
    etiketlenmeyen = 0

    try:
        await message.reply(
            f"{emoji} [{hedef_kullanici.first_name}](tg://user?id={hedef_kullanici.id})",
            quote=False
        )
        etiketlenen += 1
    except Exception as e:
        etiketlenmeyen += 1
        await message.reply(f"❌ Etiketleme başarısız oldu: {e}")

    await message.reply(
        f"📊 **Etiketleme Sonucu:**\n"
        f"✅ Etiketlenen: {etiketlenen}\n"
        f"❌ Etiketlenemeyen: {etiketlenmeyen}\n"
        f"🏁 İşlem tamamlandı."
    )
