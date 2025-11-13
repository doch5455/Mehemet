from typing import Union
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ArchMusic import app


def help_pannel(_, START: Union[bool, int] = None):

    # ALT – GERİ & KAPAT BUTONLARI
    control_btns = [
        InlineKeyboardButton(
            text=_["BACK_BUTTON"], callback_data="settingsback_helper"
        ),
        InlineKeyboardButton(
            text=_["CLOSEMENU_BUTTON"], callback_data="close"
        ),
    ]

    upl = InlineKeyboardMarkup(
        [
            # 1. SIRA
            [
                InlineKeyboardButton(text=_["H_B_1"], callback_data="help_callback hb1"),
                InlineKeyboardButton(text=_["H_B_2"], callback_data="help_callback hb2"),
            ],

            # 2. SIRA
            [
                InlineKeyboardButton(text=_["H_B_3"], callback_data="help_callback hb3"),
                InlineKeyboardButton(text=_["H_B_4"], callback_data="help_callback hb4"),
            ],

            # 3. SIRA → SON ÜÇ BUTTON YAN YANA
            [
                InlineKeyboardButton(text=_["H_B_5"], callback_data="help_callback hb5"),
                InlineKeyboardButton(text=_["H_B_6"], callback_data="help_callback hb6"),
                InlineKeyboardButton(text=_["H_B_7"], callback_data="help_callback hb7"),
            ],

            # 4. SIRA → GERİ + KAPAT
            control_btns,
        ]
    )
    return upl



def help_back_markup(_):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"], callback_data="settings_back_helper"
                ),
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"], callback_data="close"
                ),
            ]
        ]
    )


def private_help_panel(_):
    return [
        [
            InlineKeyboardButton(
                text=_["S_B_1"],
                url=f"https://t.me/{app.username}?start=help",
            ),
        ],
    ]