import asyncio
import speedtest
import time
from pyrogram import filters
from pyrogram.types import Message
from ArchMusic import app
from ArchMusic.utils.decorators.language import language

# SUDOERS: Botun izinli kullanıcılarının Telegram ID'lerini buraya ekle
SUDOERS = [123456789]  # Örnek: kendi Telegram ID'nizi buraya yazın

def format_speed(bps):
    """Bps cinsinden hızı Mbps olarak döner"""
    return f"{bps / 1_000_000:.2f} Mbps"

def progress_bar(percentage, length=20):
    """Yüzdeye göre ASCII ilerleme çubuğu oluşturur"""
    filled_length = int(length * percentage // 100)
    bar = "█" * filled_length + "─" * (length - filled_length)
    return f"[{bar}] {percentage:.0f}%"

def run_speedtest_real_time(m):
    """Download ve upload hızını saniye saniye güncelleyerek test eder"""
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m.edit_text("Sunucu seçildi ✅")

        # Download ölçümü
        m.edit_text("İndirme başlıyor ⏳")
        download_speed = 0
        start = time.time()
        while True:
            download_speed = test.download()
            elapsed = time.time() - start
            percentage = min((elapsed / 10) * 100, 100)
            bar = progress_bar(percentage)
            m.edit_text(f"İndirme: {bar} ({format_speed(download_speed)})")
            if percentage >= 100:
                break
            time.sleep(1)
        m.edit_text(f"İndirme tamamlandı ✅ ({format_speed(download_speed)})")

        # Upload ölçümü
        m.edit_text("Yükleme başlıyor ⏳")
        upload_speed = 0
        start = time.time()
        while True:
            upload_speed = test.upload()
            elapsed = time.time() - start
            percentage = min((elapsed / 10) * 100, 100)
            bar = progress_bar(percentage)
            m.edit_text(f"Yükleme: {bar} ({format_speed(upload_speed)})")
            if percentage >= 100:
                break
            time.sleep(1)
        m.edit_text(f"Yükleme tamamlandı ✅ ({format_speed(upload_speed)})")

        # Sonuçları paylaş
        test.results.share()
        return test.results.dict()

    except Exception as e:
        m.edit_text(f"<code>{e}</code>")
        return None

@app.on_message(filters.command(["speedtest", "spt"]) & filters.user(SUDOERS))
@language
async def speedtest_function(client, message: Message, _):
    m = await message.reply_text("Speedtest başlatılıyor... ⏳")

    # Speedtest'i ayrı thread'te çalıştır
    result = await asyncio.to_thread(run_speedtest_real_time, m)

    if not result:
        return

    output = f"""
**ISP:** {result['client']['isp']}
**Ülke:** {result['client']['country']}
**Sunucu:** {result['server']['name']} ({result['server']['country']})
**Sponsor:** {result['server']['sponsor']}
**Ping:** {result['ping']} ms
**Latency:** {result['server']['latency']} ms
"""

    await message.reply_photo(photo=result["share"], caption=output)
    await m.delete()
    
