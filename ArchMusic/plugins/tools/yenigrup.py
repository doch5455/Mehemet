import datetime
from pyrogram import Client, filters
from pyrogram.types import Message, ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from pyrogram.enums import ChatMemberStatus
from config import LOG_GROUP_ID
from ArchMusic import app


def get_timestamp():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


async def send_log(text: str, user_id=None, has_photo=True, reply_markup=None):
    try:
        # Logu dosyaya yaz
        with open("logs.txt", "a", encoding="utf-8") as f:
            f.write(f"[{get_timestamp()}]\n{text}\n\n")

        # Profil fotoğrafını ekle (varsa)
        if user_id and has_photo:
            try:
                photos = await app.get_profile_photos(user_id)
                if photos.total_count > 0:
                    await app.send_photo(
                        chat_id=LOG_GROUP_ID,
                        photo=photos[0].file_id,
                        caption=f"{text}\n\n🕒 `{get_timestamp()}`",
                        reply_markup=reply_markup
                    )
                    return
            except Exception as e:
                print(f"[HATA] Profil fotoğrafı alınamadı: {e}")

        # Fotoğraf yoksa düz mesaj
        await app.send_message(
            chat_id=LOG_GROUP_ID,
            text=f"{text}\n\n🕒 `{get_timestamp()}`",
            reply_markup=reply_markup
        )
    except Exception as e:
        print(f"[HATA] Log mesajı gönderilemedi:\n{e}")


@app.on_message(filters.new_chat_members)
async def on_new_member(client: Client, message: Message):
    bot_id = (await client.get_me()).id
    for user in message.new_chat_members:
        ad = message.from_user.first_name if message.from_user else "Bilinmiyor"
        chat = message.chat
        chat_link = f"@{chat.username}" if chat.username else "Yok"

        if user.id == bot_id:
            text = (
                f"<u>#✅ <b>Bot Gruba Eklendi</b></u>\n\n"
                f"👥 <b>Grup:</b> {chat.title}\n"
                f"🆔 <b>Grup ID:</b> `{chat.id}`\n"
                f"🔗 <b>Link:</b> {chat_link}\n"
                f"➕ <b>Ekleyen:</b> {ad}"
            )
            await send_log(text, user_id=message.from_user.id)
        else:
            text = (
                f"<u>#👤 <b>Kullanıcı Eklendi</b></u>\n\n"
                f"🙋 <b>Adı:</b> {user.mention}\n"
                f"🆔 <b>ID:</b> `{user.id}`\n"
                f"👥 <b>Grup:</b> {chat.title}\n"
                f"➕ <b>Ekleyen:</b> {ad}"
            )
            markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton(ad, user_id=message.from_user.id)]] if message.from_user else []
            )
            await send_log(text, user_id=user.id, reply_markup=markup)


@app.on_message(filters.left_chat_member)
async def on_left_member(client: Client, message: Message):
    bot_id = (await client.get_me()).id
    user = message.left_chat_member
    ad = message.from_user.first_name if message.from_user else "Bilinmiyor"
    chat = message.chat

    if user.id == bot_id:
        text = (
            f"<u>#🚫 <b>Bot Gruptan Atıldı</b></u>\n\n"
            f"👥 <b>Grup:</b> {chat.title}\n"
            f"🆔 <b>Grup ID:</b> `{chat.id}`\n"
            f"❌ <b>Atan:</b> {ad}"
        )
        await send_log(text, user_id=message.from_user.id)
    else:
        text = (
            f"<u>#🚷 <b>Kullanıcı Ayrıldı/Atıldı</b></u>\n\n"
            f"🙋 <b>Adı:</b> {user.mention}\n"
            f"🆔 <b>ID:</b> `{user.id}`\n"
            f"👥 <b>Grup:</b> {chat.title}\n"
            f"❌ <b>Çıkaran:</b> {ad}"
        )
        markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(ad, user_id=message.from_user.id)]] if message.from_user else []
        )
        await send_log(text, user_id=user.id, reply_markup=markup)


@app.on_chat_member_updated
async def on_chat_member_update(client: Client, update: ChatMemberUpdated):
    old = update.old_chat_member
    new = update.new_chat_member
    user = new.user
    chat = update.chat

    if not user:
        return

    user_name = user.mention or f"{user.first_name} (`{user.id}`)"

    if old.status != new.status:
        if new.status == ChatMemberStatus.ADMINISTRATOR:
            text = (
                f"<u>#🛡️ <b>Yönetici Yapıldı</b></u>\n\n"
                f"🙋 <b>Kullanıcı:</b> {user_name}\n"
                f"🆔 <b>ID:</b> `{user.id}`\n"
                f"👥 <b>Grup:</b> {chat.title}\n"
                f"🆔 <b>Grup ID:</b> `{chat.id}`"
            )
        elif old.status == ChatMemberStatus.ADMINISTRATOR and new.status == ChatMemberStatus.MEMBER:
            text = (
                f"<u>#⚠️ <b>Yetkiler Alındı</b></u>\n\n"
                f"🙋 <b>Kullanıcı:</b> {user_name}\n"
                f"🆔 <b>ID:</b> `{user.id}`\n"
                f"👥 <b>Grup:</b> {chat.title}\n"
                f"🆔 <b>Grup ID:</b> `{chat.id}`"
            )
        elif new.status == ChatMemberStatus.BANNED:
            text = (
                f"<u>#⛔️ <b>Kullanıcı Banlandı</b></u>\n\n"
                f"🙋 <b>Kullanıcı:</b> {user_name}\n"
                f"🆔 <b>ID:</b> `{user.id}`\n"
                f"👥 <b>Grup:</b> {chat.title}\n"
                f"🆔 <b>Grup ID:</b> `{chat.id}`"
            )
        elif old.status == ChatMemberStatus.BANNED and new.status == ChatMemberStatus.MEMBER:
            text = (
                f"<u>#🔓 <b>Ban Kaldırıldı</b></u>\n\n"
                f"🙋 <b>Kullanıcı:</b> {user_name}\n"
                f"🆔 <b>ID:</b> `{user.id}`\n"
                f"👥 <b>Grup:</b> {chat.title}\n"
                f"🆔 <b>Grup ID:</b> `{chat.id}`"
            )
        elif new.status == ChatMemberStatus.LEFT:
            text = (
                f"<u>#🚪 <b>Kullanıcı Ayrıldı</b></u>\n\n"
                f"🙋 <b>Kullanıcı:</b> {user_name}\n"
                f"🆔 <b>ID:</b> `{user.id}`\n"
                f"👥 <b>Grup:</b> {chat.title}\n"
                f"🆔 <b>Grup ID:</b> `{chat.id}`"
            )
        else:
            return

        await send_log(text, user_id=user.id)
