import random
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import BANNED_USERS
from ArchMusic import app

@app.on_message(filters.command("coin") & filters.group & ~BANNED_USERS)
async def coin_toss(client, message: Message):
    sonuc = random.choice(["🪙 Yazı", "🪙 Tura"])

    await message.reply_text(
        f"🎲 Para havaya atıldı...\n\n📍 Sonuç: **{sonuc}**",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("↻ Tekrar At", callback_data="coin_again")]]
        ),
        quote=True
    )

@app.on_callback_query(filters.regex("coin_again"))
async def coin_again_callback(client, callback_query):
    sonuc = random.choice(["🪙 Yazı", "🪙 Tura"])
    await callback_query.message.edit_text(
        f"🎲 Para tekrar atıldı...\n\n📍 Yeni Sonuç: **{sonuc}**",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("↻ Tekrar At", callback_data="coin_again")]]
        )
    )
    await callback_query.answer("🎯 Yeni sonuç geldi!", show_alert=False)
