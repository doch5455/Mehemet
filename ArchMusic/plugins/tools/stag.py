from pyrogram import filters
from pyrogram.types import Message
from config import BANNED_USERS
from ArchMusic import app

# Global cancel listesi
cancel_users = set()

@app.on_message(filters.command("cancel") & filters.group & ~BANNED_USERS)
async def cancel_command(client, message: Message):
    cancel_users.add(message.from_user.id)
    await message.reply("❌ İşlem iptal edildi. Etiketleme durduruldu.")

@app.on_message(filters.command("stag") & filters.group & ~BANNED_USERS)
async def sticker_or_photo_tag(client, message: Message):
    user_id = message.from_user.id

    # Cancel kontrolü
    if user_id in cancel_users:
        cancel_users.remove(user_id)
        return await message.reply("⛔ Etiketleme işlemi iptal edilmişti.")

    # Yanıt kontrolü
    if not message.reply_to_message or not message.reply_to_message.from_user:
        return await message.reply("❗ Lütfen bir çıkartmayı ya da fotoğrafı yanıtlayın!")

    hedef_kullanici = message.reply_to_message.from_user
    etiketlenen = 0
    etiketlenmeyen = 0

    # Medya tipi kontrolü
    if message.reply_to_message.sticker:
        medya_id = message.reply_to_message.sticker.file_id
        medya_tip = "sticker"
    elif message.reply_to_message.photo:
        medya_id = message.reply_to_message.photo.file_id
        medya_tip = "photo"
    else:
        return await message.reply("❗ Lütfen bir çıkartmayı ya da fotoğrafı yanıtlayın!")

    try:
        if medya_tip == "sticker":
            await client.send_sticker(
                chat_id=message.chat.id,
                sticker=medya_id,
                reply_to_message_id=message.message_id
            )
        else:
            await client.send_photo(
                chat_id=message.chat.id,
                photo=medya_id,
                reply_to_message_id=message.message_id
            )

        etiketlenen += 1
        await message.reply(
            f"😶‍🌫️ [{hedef_kullanici.first_name}](tg://user?id={hedef_kullanici.id}) bu medya ile gizlice etiketlendi.",
            quote=False
        )
    except Exception as e:
        etiketlenmeyen += 1
        await message.reply(f"❌ Etiketleme başarısız oldu: {e}")

    # Rapor
    await message.reply(
        f"📊 **Etiketleme Sonucu:**\n"
        f"✅ Etiketlenen: {etiketlenen}\n"
        f"❌ Etiketlenemeyen: {etiketlenmeyen}\n"
        f"🏁 İşlem tamamlandı."
    )
