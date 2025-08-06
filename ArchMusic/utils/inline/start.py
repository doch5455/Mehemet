# Copyright (C) 2021-2023 by ArchBots@Github, < https://github.com/ArchBots >.
# This file is part of < https://github.com/ArchBots/ArchMusic > project,
# released under GNU v3.0 License. See LICENSE for details.

from typing import Union
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from config import GITHUB_REPO, SUPPORT_CHANNEL, SUPPORT_GROUP
from ArchMusic import app

# --- Start Panel ---
def start_pannel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text="▶️ " + _["S_B_1"],
                url=f"https://t.me/{app.username}?start=help",
            ),
            InlineKeyboardButton(
                text="⚙️ " + _["S_B_2"],
                callback_data="settings_helper"
            ),
        ],
    ]
    if SUPPORT_CHANNEL and SUPPORT_GROUP:
        buttons.append(
            [
                InlineKeyboardButton(
                    text="📢 " + _["S_B_4"], url=f"{SUPPORT_CHANNEL}"
                ),
                InlineKeyboardButton(
                    text="💬 " + _["S_B_3"], url=f"{SUPPORT_GROUP}"
                ),
            ]
        )
    else:
        if SUPPORT_CHANNEL:
            buttons.append(
                [InlineKeyboardButton(text="📢 " + _["S_B_4"], url=f"{SUPPORT_CHANNEL}")]
            )
        if SUPPORT_GROUP:
            buttons.append(
                [InlineKeyboardButton(text="💬 " + _["S_B_3"], url=f"{SUPPORT_GROUP}")]
            )
    return buttons

# --- Private Panel ---
def private_panel(_, BOT_USERNAME, OWNER: Union[bool, int] = None):
    buttons = [[InlineKeyboardButton(text="🔙 " + _["S_B_8"], callback_data="settings_back_helper")]]
    if SUPPORT_CHANNEL and SUPPORT_GROUP:
        buttons.append(
            [
                InlineKeyboardButton(text="📢 " + _["S_B_4"], url=f"{SUPPORT_CHANNEL}"),
                InlineKeyboardButton(text="💬 " + _["S_B_3"], url=f"{SUPPORT_GROUP}"),
            ]
        )
    else:
        if SUPPORT_CHANNEL:
            buttons.append([InlineKeyboardButton(text="📢 " + _["S_B_4"], url=f"{SUPPORT_CHANNEL}")])
        if SUPPORT_GROUP:
            buttons.append([InlineKeyboardButton(text="💬 " + _["S_B_3"], url=f"{SUPPORT_GROUP}")])
    buttons.append(
        [InlineKeyboardButton(text="➕ " + _["S_B_5"], url=f"https://t.me/{BOT_USERNAME}?startgroup=true")]
    )
    if GITHUB_REPO and OWNER:
        buttons.append([InlineKeyboardButton(text="👤 " + _["S_B_7"], user_id=OWNER)])
    else:
        if GITHUB_REPO:
            buttons.append([InlineKeyboardButton(text="🐙 " + _["S_B_6"], url=f"https://github.com/ArchBots/ArchMusic")])
        if OWNER:
            buttons.append([InlineKeyboardButton(text="👤 " + _["S_B_7"], user_id=OWNER)])
    return buttons

# --- Start Command Handler ---
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message: Message):
    # Önce sticker gönder
    await message.reply_sticker(
        "CAACAgUAAxkBAAEB123Zn6fN0iFQ4FzQ9BESx6jVdZxZ9wACSwEAAkKVaFT4-8bFy0-N0B4E"  # BURAYA kendi sticker file_id'ni koy
    )

    # Sonra panel gönder
    _ = {
        "S_B_1": "Başlat",
        "S_B_2": "Ayarlar",
        "S_B_3": "Destek Grubu",
        "S_B_4": "Duyuru Kanalı",
        "S_B_5": "Gruba Ekle",
        "S_B_6": "GitHub",
        "S_B_7": "Sahip",
        "S_B_8": "Geri"
    }
    buttons = start_pannel(_)
    await message.reply_text(
        "🎵 Merhaba! İşte seçenekleriniz:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
