from typing import Union, Optional
from pyrogram.types import InlineKeyboardButton
from config import GITHUB_REPO, SUPPORT_CHANNEL, SUPPORT_GROUP
from ArchMusic import app


# Eğer daha iyi bir UX istersen: başlığı klavyeye eklemek yerine
# bot.send_message(chat_id, "📌 Menuden istediğin işlemi seç", reply_markup=InlineKeyboardMarkup(buttons))
# şeklinde mesaj metninde gönder. Bu en temiz görünendir.
#
# Aşağıdaki implementasyon ise "başlık butonu"nu klavyeye koyar (tıklanabilir, callback_data='header').


def start_pannel(_: dict):
    buttons = [
        [
            InlineKeyboardButton(text=f"🟦 {_[ 'S_B_1' ]}", url=f"https://t.me/{app.username}?start=help"),
            InlineKeyboardButton(text=f"🟨 {_[ 'S_B_2' ]}", callback_data="settings_helper"),
        ]
    ]

    support_buttons = _get_support_buttons(_)
    if support_buttons:
        buttons.append(support_buttons)

    return buttons


def private_panel(
    _: dict,
    BOT_USERNAME: str,
    OWNER: Union[bool, int] = None,
    header_text: Optional[str] = "📌 Menuden istediğin işlemi seç"
):
    """
    header_text: Klavyenin en üstüne gelecek başlık metni.
                 Eğer None verirsen başlık eklenmez.
                 Not: Klavyedeki başlık butonu tıklanabilir (callback_data='header').
                 Daha iyi bir görünüm için başlığı mesaj metninde göndermeni öneririm.
    """
    buttons = []

    # Opsiyonel başlık (klavyede buton olarak)
    if header_text:
        # callback_data 'header' olarak bırakıldı; botunda bu callback'i yakalayıp pas geçebilirsin.
        buttons.append([InlineKeyboardButton(text=header_text, callback_data="header")])

    # 1. Satır: Geri butonu (ortada)
    buttons.append([
        InlineKeyboardButton(text=f"🔙 {_[ 'S_B_8' ]}", callback_data="settings_back_helper")
    ])

    # 2. Satır: Destek grubu ve kanal (iki sütun)
    support_buttons = _get_support_buttons(_)
    if support_buttons:
        buttons.append(support_buttons)

    # 3. Satır: Grup ekle (ortada)
    buttons.append([
        InlineKeyboardButton(
            text=f"🟢 {_[ 'S_B_5' ]}",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true"
        )
    ])

    # 4. Satır: GitHub ve Owner (iki sütun)
    final_row = []
    if GITHUB_REPO:
        final_row.append(
            InlineKeyboardButton(text=f"🟣 {_[ 'S_B_6' ]}", url=GITHUB_REPO)
        )
    if OWNER:
        final_row.append(
            InlineKeyboardButton(text=f"🔴 {_[ 'S_B_7' ]}", user_id=OWNER)
        )
    if final_row:
        buttons.append(final_row)

    return buttons


def _get_support_buttons(_):
    """Destek butonlarını iki sütun veya tekli olarak döndürür."""
    buttons = []
    if SUPPORT_GROUP:
        buttons.append(InlineKeyboardButton(text=f"🟩 {_[ 'S_B_3' ]}", url=SUPPORT_GROUP))
    if SUPPORT_CHANNEL:
        buttons.append(InlineKeyboardButton(text=f"🟦 {_[ 'S_B_4' ]}", url=SUPPORT_CHANNEL))

    if buttons:
        # Her zaman bir satır halinde dönüyoruz (tek veya iki buton), böylece hizalama tutarlı olur.
        return [buttons]
    return None
