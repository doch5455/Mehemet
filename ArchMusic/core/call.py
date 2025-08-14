#.
#

import asyncio
from datetime import datetime, timedelta
from typing import Union

from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import InlineKeyboardMarkup
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.exceptions import (
    AlreadyJoinedError,
    NoActiveGroupCall,
    TelegramServerError,
)
from pytgcalls.types import (
    JoinedGroupCallParticipant,
    LeftGroupCallParticipant,
    Update,
)
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.stream import StreamAudioEnded

import config
from strings import get_string
from ArchMusic import LOGGER, YouTube, app
from ArchMusic.misc import db
from ArchMusic.utils.database import (
    add_active_chat,
    add_active_video_chat,
    get_assistant,
    get_audio_bitrate,
    get_lang,
    get_loop,
    get_video_bitrate,
    group_assistant,
    is_autoend,
    music_on,
    mute_off,
    remove_active_chat,
    remove_active_video_chat,
    set_loop,
)
from ArchMusic.utils.exceptions import AssistantErr
from ArchMusic.utils.inline.play import stream_markup, telegram_markup
from ArchMusic.utils.stream.autoclear import auto_clean

autoend = {}
counter = {}
AUTO_END_TIME = 3

async def _clear_(chat_id: int) -> None:
    db[chat_id] = []
    await remove_active_video_chat(chat_id)
    await remove_active_chat(chat_id)

class Call(PyTgCalls):
    def __init__(self):
        self.userbot1 = Client(
            "ArchMusicString1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
        )
        self.one = PyTgCalls(self.userbot1, cache_duration=100)

        self.userbot2 = Client(
            "ArchMusicString2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2),
        )
        self.two = PyTgCalls(self.userbot2, cache_duration=100)

        self.userbot3 = Client(
            "ArchMusicString3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3),
        )
        self.three = PyTgCalls(self.userbot3, cache_duration=100)

        self.userbot4 = Client(
            "ArchMusicString4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4),
        )
        self.four = PyTgCalls(self.userbot4, cache_duration=100)

        self.userbot5 = Client(
            "ArchMusicString5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5),
        )
        self.five = PyTgCalls(self.userbot5, cache_duration=100)

    async def pause_stream(self, chat_id: int) -> None:
        assistant = await group_assistant(self, chat_id)
        await assistant.pause_stream(chat_id)

    async def resume_stream(self, chat_id: int) -> None:
        assistant = await group_assistant(self, chat_id)
        await assistant.resume_stream(chat_id)

    async def mute_stream(self, chat_id: int) -> None:
        assistant = await group_assistant(self, chat_id)
        await assistant.mute_stream(chat_id)

    async def unmute_stream(self, chat_id: int) -> None:
        assistant = await group_assistant(self, chat_id)
        await assistant.unmute_stream(chat_id)

    async def stop_stream(self, chat_id: int) -> None:
        assistant = await group_assistant(self, chat_id)
        try:
            await _clear_(chat_id)
            await assistant.leave_group_call(chat_id)
        except Exception:
            pass

    async def force_stop_stream(self, chat_id: int) -> None:
        assistant = await group_assistant(self, chat_id)
        try:
            check = db.get(chat_id)
            check.pop(0)
        except IndexError:
            pass
        await remove_active_video_chat(chat_id)
        await remove_active_chat(chat_id)
        try:
            await assistant.leave_group_call(chat_id)
        except Exception:
            pass

    async def skip_stream(
        self, chat_id: int, link: str, video: Union[bool, str] = None
    ) -> None:
        assistant = await group_assistant(self, chat_id)
        audio_stream_quality = await get_audio_bitrate(chat_id)
        video_stream_quality = await get_video_bitrate(chat_id)
        stream = (
            AudioVideoPiped(
                link,
                audio_parameters=audio_stream_quality,
                video_parameters=video_stream_quality,
            )
            if video
            else AudioPiped(link, audio_parameters=audio_stream_quality)
        )
        await assistant.change_stream(chat_id, stream)

    async def seek_stream(
        self,
        chat_id: int,
        file_path: str,
        to_seek: str,
        duration: str,
        mode: str,
    ) -> None:
        assistant = await group_assistant(self, chat_id)
        audio_stream_quality = await get_audio_bitrate(chat_id)
        video_stream_quality = await get_video_bitrate(chat_id)
        stream = (
            AudioVideoPiped(
                file_path,
                audio_parameters=audio_stream_quality,
                video_parameters=video_stream_quality,
                additional_ffmpeg_parameters=f"-ss {to_seek} -to {duration}",
            )
            if mode == "video"
            else AudioPiped(
                file_path,
                audio_parameters=audio_stream_quality,
                additional_ffmpeg_parameters=f"-ss {to_seek} -to {duration}",
            )
        )
        await assistant.change_stream(chat_id, stream)

    async def stream_call(self, link: str) -> None:
        assistant = await group_assistant(self, config.LOG_GROUP_ID)
        await assistant.join_group_call(
            config.LOG_GROUP_ID,
            AudioVideoPiped(link),
            stream_type=StreamType().pulse_stream,
        )
        await asyncio.sleep(0.5)
        await assistant.leave_group_call(config.LOG_GROUP_ID)

    async def join_assistant(self, original_chat_id: int, chat_id: int) -> None:
        language = await get_lang(original_chat_id)
        _ = get_string(language)
        userbot = await get_assistant(chat_id)
        try:
            try:
                get = await app.get_chat_member(chat_id, userbot.id)
            except ChatAdminRequired:
                raise AssistantErr(_["call_1"])
            if get.status in (ChatMemberStatus.BANNED, ChatMemberStatus.LEFT):
                raise AssistantErr(_["call_2"].format(userbot.username, userbot.id))
        except UserNotParticipant:
            chat = await app.get_chat(chat_id)
            if chat.username:
                try:
                    await userbot.join_chat(chat.username)
                except UserAlreadyParticipant:
                    pass
                except Exception as e:
                    raise AssistantErr(_["call_3"].format(e))
            else:
                try:
                    invitelink = chat.invite_link
                    if invitelink is None:
                        invitelink = await app.export_chat_invite_link(chat_id)
                except ChatAdminRequired:
                    raise AssistantErr(_["call_4"])
                except Exception as e:
                    raise AssistantErr(str(e))

                m = await app.send_message(original_chat_id, _["call_5"])
                if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace("https://t.me/+", "https://t.me/joinchat/")
                await asyncio.sleep(3)
                await userbot.join_chat(invitelink)
                await asyncio.sleep(4)
                await m.edit(_["call_6"].format(userbot.name))

    async def join_call(
        self,
        chat_id: int,
        original_chat_id: int,
        link,
        video: Union[bool, str] = None,
    ) -> None:
        assistant = await group_assistant(self, chat_id)
        audio_stream_quality = await get_audio_bitrate(chat_id)
        video_stream_quality = await get_video_bitrate(chat_id)
        stream = (
            AudioVideoPiped(
                link,
                audio_parameters=audio_stream_quality,
                video_parameters=video_stream_quality,
            )
            if video
            else AudioPiped(link, audio_parameters=audio_stream_quality)
        )
        try:
            await assistant.join_group_call(
                chat_id,
                stream,
                stream_type=StreamType().pulse_stream,
            )
        except NoActiveGroupCall:
            try:
                await self.join_assistant(original_chat_id, chat_id)
                await assistant.join_group_call(
                    chat_id,
                    stream,
                    stream_type=StreamType().pulse_stream,
                )
            except Exception:
                raise AssistantErr(
                    "**Aktif Sesli Sohbet Bulunamadı**\n\n"
                    "Lütfen grubun sesli sohbetinin etkinleştirildiğinden emin olun. "
                    "Zaten etkinse, lütfen sonlandırın ve yeniden yeni sesli sohbet başlatın. "
                    "Sorun devam ederse /yeniden başlatmayı deneyin."
                )
        except AlreadyJoinedError:
            raise AssistantErr(
                "**Asistan Zaten Sesli Sohbette**\n\n"
                "Sistemler, asistanın zaten sesli sohbette bulunduğunu tespit etti; "
                "bu sorun genellikle 2 sorguyu birlikte yürüttüğünüzde ortaya çıkar.\n\n"
                "Asistan sesli sohbette yoksa lütfen sesli sohbeti sonlandırın ve "
                "yeni sesli sohbeti yeniden başlatın; sorun devam ederse /yeniden başlatmayı deneyin."
            )
        except TelegramServerError:
            raise AssistantErr(
                "**Telegram Sunucu Hatası**\n\n"
                "Telegram'da bazı dahili sunucu sorunları yaşanıyor. Lütfen tekrar deneyin.\n\n"
                "Bu sorun devam ederse, sesli sohbetinizi sonlandırıp yeniden başlatın."
            )

        await add_active_chat(chat_id)
        await mute_off(chat_id)
        await music_on(chat_id)
        if video:
            await add_active_video_chat(chat_id)
        if await is_autoend():
            counter[chat_id] = {}
            users = len(await assistant.get_participants(chat_id))
            if users == 1:
                autoend[chat_id] = datetime.now() + timedelta(minutes=AUTO_END_TIME)

    async def change_stream(self, client, chat_id: int) -> None:
        check = db.get(chat_id)
        popped = None
        loop = await get_loop(chat_id)
        try:
            if loop == 0:
                popped = check.pop(0)
            else:
                loop -= 1
                await set_loop(chat_id, loop)
            if popped and config.AUTO_DOWNLOADS_CLEAR == str(True):
                await auto_clean(popped)
            if not check:
                await _clear_(chat_id)
                return await client.leave_group_call(chat_id)
        except Exception:
            try:
                await _clear_(chat_id)
                return await client.leave_group_call(chat_id)
            except Exception:
                return

        queued = check[0]["file"]
        language = await get_lang(chat_id)
        _ = get_string(language)
        title = check[0]["title"].title()
        user = check[0]["by"]
        original_chat_id = check[0]["chat_id"]
        streamtype = check[0]["streamtype"]
        audio_stream_quality = await get_audio_bitrate(chat_id)
        video_stream_quality = await get_video_bitrate(chat_id)
        videoid = check[0]["vidid"]
        check[0]["played"] = 0

        if "live_" in queued:
            n, link = await YouTube.video(videoid, True)
            if n == 0:
                return await app.send_message(original_chat_id, text=_["call_9"])
            stream = (
                AudioVideoPiped(
                    link,
                    audio_parameters=audio_stream_quality,
                    video_parameters=video_stream_quality,
                )
                if str(streamtype) == "video"
                else AudioPiped(link, audio_parameters=audio_stream_quality)
            )
            try:
                await client.change_stream(chat_id, stream)
            except Exception:
                return await app.send_message(original_chat_id, text=_["call_9"])
            button = telegram_markup(_, chat_id)
            run = await app.send_message(
                chat_id=original_chat_id,
                text=_["stream_1"].format(
                    title,
                    f"https://t.me/{app.username}?start=info_{videoid}",
                    check[0]["dur"],
                    user,
                ),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"

        elif "vid_" in queued:
            mystic = await app.send_message(original_chat_id, _["call_10"])
            try:
                file_path, direct = await YouTube.download(
                    videoid,
                    mystic,
                    videoid=True,
                    video=True if str(streamtype) == "video" else False,
                )
            except Exception:
                return await mystic.edit_text(_["call_9"], disable_web_page_preview=True)

            stream = (
                AudioVideoPiped(
                    file_path,
                    audio_parameters=audio_stream_quality,
                    video_parameters=video_stream_quality,
                )
                if str(streamtype) == "video"
                else AudioPiped(file_path, audio_parameters=audio_stream_quality)
            )
            try:
                await client.change_stream(chat_id, stream)
            except Exception:
                return await app.send_message(original_chat_id, text=_["call_9"])

            button = stream_markup(_, videoid, chat_id)
            await mystic.delete()
            run = await app.send_message(
                chat_id=original_chat_id,
                text=_["stream_1"].format(
                    title,
                    f"https://t.me/{app.username}?start=info_{videoid}",
                    check[0]["dur"],
                    user,
                ),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"

        elif "index_" in queued:
            stream = (
                AudioVideoPiped(
                    videoid,
                    audio_parameters=audio_stream_quality,
                    video_parameters=video_stream_quality,
                )
                if str(streamtype) == "video"
                else AudioPiped(videoid, audio_parameters=audio_stream_quality)
            )
            try:
                await client.change_stream(chat_id, stream)
            except Exception:
                return await app.send_message(original_chat_id, text=_["call_9"])
            button = telegram_markup(_, chat_id)
            run = await app.send_message(
                chat_id=original_chat_id,
                text=_["stream_2"].format(
                    title,
                    f"https://t.me/{app.username}?start=info_{videoid}",
                    check[0]["dur"],
                    user,
                ),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"

        else:
            stream = (
                AudioVideoPiped(
                    queued,
                    audio_parameters=audio_stream_quality,
                    video_parameters=video_stream_quality,
                )
                if str(streamtype) == "video"
                else AudioPiped(queued, audio_parameters=audio_stream_quality)
            )
            try:
                await client.change_stream(chat_id, stream)
            except Exception:
                return await app.send_message(original_chat_id, text=_["call_9"])

            if videoid == "telegram":
                button = telegram_markup(_, chat_id)
                run = await app.send_message(
                    original_chat_id,
                    text=_["stream_3"].format(title, check[0]["dur"], user),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"
            elif videoid == "soundcloud":
                button = telegram_markup(_, chat_id)
                run = await app.send_message(
                    original_chat_id,
                    text=_["stream_3"].format(title, check[0]["dur"], user),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"
            else:
                button = stream_markup(_, videoid, chat_id)
                run = await app.send_message(
                    chat_id=original_chat_id,
                    text=_["stream_1"].format(
                        title,
                        f"https://t.me/{app.username}?start=info_{videoid}",
                        check[0]["dur"],
                        user,
                    ),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "stream"

    async def ping(self) -> str:
        pings = []
        for client in (self.one, self.two, self.three, self.four, self.five):
            if config.STRING1 and client is self.one:
                pings.append(await client.ping)
            if config.STRING2 and client is self.two:
                pings.append(await client.ping)
            if config.STRING3 and client is self.three:
                pings.append(await client.ping)
            if config.STRING4 and client is self.four:
                pings.append(await client.ping)
            if config.STRING5 and client is self.five:
                pings.append(await client.ping)
        return str(round(sum(pings) / len(pings), 3)) if pings else "0"

    async def start(self) -> None:
        LOGGER(__name__).info("Starting PyTgCalls Client\n")
        for client, string in (
            (self.one, config.STRING1),
            (self.two, config.STRING2),
            (self.three, config.STRING3),
            (self.four, config.STRING4),
            (self.five, config.STRING5),
        ):
            if string:
                await client.start()

    async def decorators(self) -> None:
        for client in (self.one, self.two, self.three, self.four, self.five):
            if not hasattr(client, "on_kicked"):
                continue

            @client.on_kicked()
            @client.on_closed_voice_chat()
            @client.on_left()
            async def stream_services_handler(_, chat_id: int):
                await self.stop_stream(chat_id)

            @client.on_stream_end()
            async def stream_end_handler(client, update: Update):
                if isinstance(update, StreamAudioEnded):
                    await self.change_stream(client, update.chat_id)

            @client.on_participants_change()
            async def participants_change_handler(client, update: Update):
                if isinstance(update, (JoinedGroupCallParticipant, LeftGroupCallParticipant)):
                    chat_id = update.chat_id
                    users = counter.get(chat_id)
                    if not users:
                        try:
                            got = len(await client.get_participants(chat_id))
                        except Exception:
                            return
                        counter[chat_id] = got
                        if got == 1:
                            autoend[chat_id] = datetime.now() + timedelta(minutes=AUTO_END_TIME)
                        else:
                            autoend[chat_id] = {}
                    else:
                        final = (
                            users + 1
                            if isinstance(update, JoinedGroupCallParticipant)
                            else users - 1
                        )
                        counter[chat_id] = final
                        if final == 1:
                            autoend[chat_id] = datetime.now() + timedelta(minutes=AUTO_END_TIME)
                        else:
                            autoend[chat_id] = {}

ArchMusic = Call()
