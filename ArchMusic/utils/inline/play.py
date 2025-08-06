
import math
from pyrogram.types import InlineKeyboardButton
from ArchMusic.utils.formatters import time_to_seconds


def get_colored_progress_bar(percentage: float, length: int = 15) -> str:
    filled_length = int(length * percentage // 100)
    bar = "🟩" * filled_length + "⬜" * (length - filled_length)
    return f"{bar} {percentage:.0f}%"


def make_callback(action: str, chat_id: int) -> str:
    return f"ADMIN {action}|{chat_id}"


def colorful_stream_controls(chat_id: int):
    buttons_config = [
        {"text": "🟢 Başlat ▶️", "action": "Resume"},
        {"text": "⏸️ Duraklat ⏸", "action": "Pause"},
        {"text": "⏭️ Atla ⏩", "action": "Skip"},
        {"text": "🔴 Bitir ⏹️", "action": "Stop"},
    ]
    return [
        [InlineKeyboardButton(text=btn["text"], callback_data=make_callback(btn["action"], chat_id))]
        for btn in buttons_config
    ]


def colorful_stream_markup_timer(_, videoid, chat_id, played, dur):
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    percentage = (played_sec / duration_sec) * 100 if duration_sec else 0

    progress_bar = get_colored_progress_bar(percentage)

    buttons = [
        [
            InlineKeyboardButton(
                text=f"⏳ {played} {progress_bar} {dur}",
                callback_data="GetTimer"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔁 Döngüye Al 🔂",
                callback_data=make_callback("Loop", chat_id)
            ),
        ],
        [
            InlineKeyboardButton(text="⏪ -10s ⏮️", callback_data=make_callback("JumpBack10", chat_id)),
            InlineKeyboardButton(text="⏩ +10s ⏭️", callback_data=make_callback("JumpForward10", chat_id)),
            InlineKeyboardButton(text="⏪ -30s ⏮️", callback_data=make_callback("JumpBack30", chat_id)),
            InlineKeyboardButton(text="⏩ +30s ⏭️", callback_data=make_callback("JumpForward30", chat_id)),
        ],
    ] + colorful_stream_controls(chat_id) + [
        [
            InlineKeyboardButton(text="❌ Kapat ✖️", callback_data="close"),
        ],
    ]
    return buttons


def colorful_stream_markup(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="🔁 Döngüye Al 🔂",
                callback_data=make_callback("Loop", chat_id)
            ),
        ],
        [
            InlineKeyboardButton(text="⏪ -10s ⏮️", callback_data=make_callback("JumpBack10", chat_id)),
            InlineKeyboardButton(text="⏩ +10s ⏭️", callback_data=make_callback("JumpForward10", chat_id)),
            InlineKeyboardButton(text="⏪ -30s ⏮️", callback_data=make_callback("JumpBack30", chat_id)),
            InlineKeyboardButton(text="⏩ +30s ⏭️", callback_data=make_callback("JumpForward30", chat_id)),
        ],
    ] + colorful_stream_controls(chat_id) + [
        [
            InlineKeyboardButton(text="❌ Kapat ✖️", callback_data="close"),
        ],
    ]
    return buttons


def colorful_telegram_markup_timer(_, chat_id, played, dur):
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    percentage = (played_sec / duration_sec) * 100 if duration_sec else 0

    progress_bar = get_colored_progress_bar(percentage)

    buttons = [
        [
            InlineKeyboardButton(
                text=f"⏳ {played} {progress_bar} {dur}",
                callback_data="GetTimer",
            )
        ],
        [
            InlineKeyboardButton(
                text="📋 Panel 🛠️",
                callback_data=f"PanelMarkup None|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(text="▶️ Başlat ▶️", callback_data=make_callback("Resume", chat_id)),
            InlineKeyboardButton(text="⏸️ Duraklat ⏸️", callback_data=make_callback("Pause", chat_id)),
            InlineKeyboardButton(text="⏭️ Atla ⏩", callback_data=make_callback("Skip", chat_id)),
            InlineKeyboardButton(text="⏹️ Durdur ⏹️", callback_data=make_callback("Stop", chat_id)),
        ],
        [
            InlineKeyboardButton(text="❌ Kapat ✖️", callback_data="close"),
        ],
    ]
    return buttons


def colorful_telegram_markup(_, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="📋 Panel 🛠️",
                callback_data=f"PanelMarkup None|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(text="▶️ Başlat ▶️", callback_data=make_callback("Resume", chat_id)),
            InlineKeyboardButton(text="⏸️ Duraklat ⏸️", callback_data=make_callback("Pause", chat_id)),
            InlineKeyboardButton(text="⏭️ Atla ⏩", callback_data=make_callback("Skip", chat_id)),
            InlineKeyboardButton(text="⏹️ Durdur ⏹️", callback_data=make_callback("Stop", chat_id)),
        ],
        [
            InlineKeyboardButton(text="❌ Kapat ✖️", callback_data="close"),
        ],
    ]
    return buttons


def colorful_track_markup(_, videoid, user_id, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text="🎵 Sesli Oynat 🔊",
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text="📹 Video Oynat 🎥",
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="❌ Kapat ✖️", callback_data=f"forceclose {videoid}|{user_id}"
            )
        ],
    ]
    return buttons


def colorful_playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text="🎵 Sesli Oynat 🔊",
                callback_data=f"YukkiPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text="📹 Video Oynat 🎥",
                callback_data=f"YukkiPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="❌ Kapat ✖️", callback_data=f"forceclose {videoid}|{user_id}"
            ),
        ],
    ]
    return buttons


def colorful_livestream_markup(_, videoid, user_id, mode, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text="📡 Canlı Yayın 🔴",
                callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text="❌ Kapat ✖️",
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
    ]
    return buttons


def colorful_slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    query = f"{query[:20]}"
    buttons = [
        [
            InlineKeyboardButton(
                text="🎵 Sesli Oynat 🔊",
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text="📹 Video Oynat 🎥",
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="❮ Önceki",
                callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text="❌ Kapat ✖️", callback_data=f"forceclose {query}|{user_id}"
            ),
            InlineKeyboardButton(
                text="Sonraki ❯",
                callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
        ],
    ]
    return buttons


def colorful_panel_markup_1(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(text="⏸️ Duraklat ⏸️", callback_data=make_callback("Pause", chat_id)),
            InlineKeyboardButton(text="▶️ Devam Et ▶️", callback_data=make_callback("Resume", chat_id)),
        ],
        [
            InlineKeyboardButton(text="⏭️ Atla ⏩", callback_data=make_callback("Skip", chat_id)),
            InlineKeyboardButton(text="⏹️ Durdur ⏹️", callback_data=make_callback("Stop", chat_id)),
        ],
        [
            InlineKeyboardButton(text="🔁 Tekrarla 🔂", callback_data=make_callback("Replay", chat_id)),
        ],
        [
            InlineKeyboardButton(text="◀️ Geri", callback_data=f"Pages Back|0|{videoid}|{chat_id}"),
            InlineKeyboardButton(text="🔙 Ana Menü", callback_data=f"MainMarkup {videoid}|{chat_id}"),
            InlineKeyboardButton(text="▶️ İleri", callback_data=f"Pages Forw|0|{videoid}|{chat_id}"),
        ],
    ]
    return buttons


def colorful_panel_markup_2(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(text="🔇 Sessiz 🔕", callback_data=make_callback("Mute", chat_id)),
            InlineKeyboardButton(text="🔊 Ses Aç 🔉", callback_data=make_callback("Unmute", chat_id)),
        ],
        [
            InlineKeyboardButton(text="🔀 Karıştır 🔄", callback_data=make_callback("Shuffle", chat_id)),
            InlineKeyboardButton(text="🔁 Döngüye Al 🔂", callback_data=make_callback("Loop", chat_id)),
        ],
        [
            InlineKeyboardButton(text="◀️ Geri", callback_data=f"Pages Back|1|{videoid}|{chat_id}"),
            InlineKeyboardButton(text="🔙 Ana Menü", callback_data=f"MainMarkup {videoid}|{chat_id}"),
            InlineKeyboardButton(text="▶️ İleri", callback_data=f"Pages Forw|1|{videoid}|{chat_id}"),
        ],
    ]
    return buttons


def colorful_panel_markup_3(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(text="⏮️ 10 Saniye Geri ⏪", callback_data=make_callback("JumpBack10", chat_id)),
            InlineKeyboardButton(text="⏭️ 10 Saniye İleri ⏩", callback_data=make_callback("JumpForward10", chat_id)),
        ],
        [
            InlineKeyboardButton(text="⏮️ 30 Saniye Geri ⏪", callback_data=make_callback("JumpBack30", chat_id)),
            InlineKeyboardButton(text="⏭️ 30 Saniye İleri ⏩", callback_data=make_callback("JumpForward30", chat_id)),
        ],
        [
            InlineKeyboardButton(text="◀️ Geri", callback_data=f"Pages Back|2|{videoid}|{chat_id}"),
            InlineKeyboardButton(text="🔙 Ana Menü", callback_data=f"MainMarkup {videoid}|{chat_id}"),
            InlineKeyboardButton(text="▶️ İleri", callback_data=f"Pages Forw|2|{videoid}|{chat_id}"),
        ],
    ]
    return buttons
