from pyrogram.types import InlineKeyboardButton
from ArchMusic import app


# ===================================================================
# STREAM MARKUP (TIMER)
# ===================================================================
def stream_markup_timer(_, videoid, chat_id, played, dur):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"],
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton("🩵 Kanal", url="https://t.me/MaviDuyuru"),
            InlineKeyboardButton("✖️ Kapat", callback_data="close"),
        ],
    ]
    return buttons


# ===================================================================
# TELEGRAM MARKUP (TIMER)
# ===================================================================
def telegram_markup_timer(_, chat_id, played, dur, videoid):
    # bar = random.choice(selection)  # Bar kullanılmıyor, hata vermesin diye kaldırıldı
    buttons = [
        [
            InlineKeyboardButton(
                text="🩵 Mavi Duyuru",
                url="https://t.me/MaviDuyuru"
            ),
            InlineKeyboardButton(
                text="🗑️ Kapat",
                callback_data="close"
            ),
        ],
    ]
    return buttons


# ===================================================================
# STREAM MARKUP (NO TIMER)
# ===================================================================
def stream_markup(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="➕ 𝗕𝗲𝗻𝗶 𝗚𝗿𝘂𝗯𝘂𝗻𝗮 𝗘𝗸𝗹𝗲",
                url=f"https://t.me/{app.username}?startgroup=true"
            )
        ],
        [
            InlineKeyboardButton(
                text="🩵 𝗞𝗮𝗻𝗮𝗹",
                url="https://t.me/MaviDuyuru"
            ),
            InlineKeyboardButton(
                text="🗑️ 𝗞𝗮𝗽𝗮𝘁",
                callback_data="close"
            )
        ]
    ]
    return buttons


# ===================================================================
# TELEGRAM MARKUP (NO TIMER)
# ===================================================================
def telegram_markup(_, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["PL_B_3"],
                callback_data=f"PanelMarkup None|{chat_id}",
            ),
            InlineKeyboardButton(
                text=_["CLOSEMENU_BUTTON"], callback_data="close"
            ),
        ],
    ]
    return buttons


# ===================================================================
# 🔍 Arama / Track Seçimi
# (KUMSAL BOTS versiyonu)
# ===================================================================
def track_markup(_, videoid, user_id, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text="𝙆𝙐𝙈𝙎𝘼𝙇 𝘽𝙊𝙏𝙎",
                url="https://t.me/the_team_kumsal",
            )
        ],
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
    ]
    return buttons


# ===================================================================
# 📜 Playlist Markup
# ===================================================================
def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text="⚡ 𝙆𝙐𝙈𝙎𝘼𝙇 𝘽𝙊𝙏𝙎 ⚡",
                url="https://t.me/the_team_kumsal",
            )
        ],
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"ArchMusicPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"ArchMusicPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}",
            ),
        ],
    ]
    return buttons


# ===================================================================
# 📺 Canlı Yayın Menüsü
# ===================================================================
def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_3"],
                callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["CLOSEMENU_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
    ]
    return buttons


# ===================================================================
# 🔁 Slider Query Markup
# ===================================================================
def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    query = f"{query[:20]}"
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="❮",
                callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {query}|{user_id}",
            ),
            InlineKeyboardButton(
                text="❯",
                callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
        ],
    ]
    return buttons


# ===================================================================
# 🧩 Kontrol Paneli — Sayfa 1
# ===================================================================
def panel_markup_1(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="⏸ Pause", callback_data=f"ADMIN Pause|{chat_id}"
            ),
            InlineKeyboardButton(
                text="▶️ Resume",
                callback_data=f"ADMIN Resume|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="⏯ Skip", callback_data=f"ADMIN Skip|{chat_id}"
            ),
            InlineKeyboardButton(
                text="⏹ Stop", callback_data=f"ADMIN Stop|{chat_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="◀️",
                callback_data=f"Pages Back|0|{videoid}|{chat_id}",
            ),
            InlineKeyboardButton(
                text="🔙 Back",
                callback_data=f"MainMarkup {videoid}|{chat_id}",
            ),
            InlineKeyboardButton(
                text="▶️",
                callback_data=f"Pages Forw|0|{videoid}|{chat_id}",
            ),
        ],
    ]
    return buttons


# ===================================================================
# 🧩 Kontrol Paneli — Sayfa 2
# ===================================================================
def panel_markup_2(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="🔇 Mute", callback_data=f"ADMIN Mute|{chat_id}"
            ),
            InlineKeyboardButton(
                text="🔊 Unmute",
                callback_data=f"ADMIN Unmute|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔀 Shuffle",
                callback_data=f"ADMIN Shuffle|{chat_id}",
            ),
            InlineKeyboardButton(
                text="🔁 Loop", callback_data=f"ADMIN Loop|{chat_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="◀️",
                callback_data=f"Pages Back|1|{videoid}|{chat_id}",
            ),
            InlineKeyboardButton(
                text="🔙 Back",
                callback_data=f"MainMarkup {videoid}|{chat_id}",
            ),
            InlineKeyboardButton(
                text="▶️",
                callback_data=f"Pages Forw|1|{videoid}|{chat_id}",
            ),
        ],
    ]
    return buttons


# ===================================================================
# 🧩 Kontrol Paneli — Sayfa 3
# ===================================================================
def panel_markup_3(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="⏮ 10 Seconds",
                callback_data=f"ADMIN 1|{chat_id}",
            ),
            InlineKeyboardButton(
                text="⏭ 10 Seconds",
                callback_data=f"ADMIN 2|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="⏮ 30 Seconds",
                callback_data=f"ADMIN 3|{chat_id}",
            ),
            InlineKeyboardButton(
                text="⏭ 30 Seconds",
                callback_data=f"ADMIN 4|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="◀️",
                callback_data=f"Pages Back|2|{videoid}|{chat_id}",
            ),
            InlineKeyboardButton(
                text="🔙 Back",
                callback_data=f"MainMarkup {videoid}|{chat_id}",
            ),
            InlineKeyboardButton(
                text="▶️",
                callback_data=f"Pages Forw|2|{videoid}|{chat_id}",
            ),
        ],
    ]
    return buttons