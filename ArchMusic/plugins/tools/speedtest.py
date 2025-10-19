import asyncio
from collections import deque
from pyrogram import filters, types
from pyrogram.enums import ParseMode
from ArchMusic import app
import speedtest

# Komutlar
HIZ_TESTI_KOMUTLARI = ["speedtest", "hiztesti"]

# Kuyruk sistemi
test_kuyrugu = deque()
test_lock = asyncio.Lock()

# Hız testi fonksiyonu
async def hiz_testi():
    test = speedtest.Speedtest()
    await asyncio.to_thread(test.get_best_server)
    await asyncio.to_thread(test.download)
    await asyncio.to_thread(test.upload)
    await asyncio.to_thread(test.results.share)
    return test.results.dict()

# Emoji grafik fonksiyonu
def hiz_grafik_otomatik(indir, yukle, bar_length=20):
    max_speed = max(indir, yukle, 1)
    indir_bar = "🟩" * int((indir/max_speed)*bar_length) + "⬜" * (bar_length - int((indir/max_speed)*bar_length))
    yukle_bar = "🟩" * int((yukle/max_speed)*bar_length) + "⬜" * (bar_length - int((yukle/max_speed)*bar_length))
    return indir_bar, yukle_bar

# Komut: Hız testi başlatma butonu
@app.on_message(filters.command(HIZ_TESTI_KOMUTLARI))
async def speedtest_start(client, mesaj):
    button = types.InlineKeyboardMarkup(
        [[types.InlineKeyboardButton("🚀 Hız Testini Başlat", callback_data="start_speedtest")]]
    )
    await mesaj.reply_text(
        "📶 Hız testi yapmak için aşağıdaki butona tıklayın:",
        reply_markup=button
    )

# Callback: Hız testi sıralı olarak çalışır
@app.on_callback_query(filters.regex("start_speedtest"))
async def speedtest_callback(client, callback_query):
    user_id = callback_query.from_user.id
    m = callback_query.message

    # Kuyruğa ekle
    test_kuyrugu.append((user_id, callback_query))
    await callback_query.answer("✅ Test sırasına eklendin.", show_alert=False)

    async with test_lock:
        while test_kuyrugu:
            current_user, current_callback = test_kuyrugu[0]

            # Sırada değilse bekle
            if current_user != user_id:
                await callback_query.answer("⏳ Sıranı bekliyorsun...", show_alert=True)
                return

            # Test başlat
            await current_callback.answer("🚀 Hız testi başlatılıyor...", show_alert=False)
            m_edit = await current_callback.message.edit_text("📡 Hız testi yapılıyor...")

            try:
                sonuc = await hiz_testi()
            except Exception as e:
                await m_edit.edit(f"⚠ Hata: {e}")
                test_kuyrugu.popleft()
                return

            indir_mbps = round(sonuc['download'] / 10**6, 2)
            yukle_mbps = round(sonuc['upload'] / 10**6, 2)
            ping_ms = round(sonuc['ping'], 2)
            indir_grafik, yukle_grafik = hiz_grafik_otomatik(indir_mbps, yukle_mbps)

            client_lat = sonuc['client']['lat']
            client_lon = sonuc['client']['lon']
            server_lat = sonuc['server']['lat']
            server_lon = sonuc['server']['lon']

            client_map = f"https://www.google.com/maps/search/?api=1&query={client_lat},{client_lon}"
            server_map = f"https://www.google.com/maps/search/?api=1&query={server_lat},{server_lon}"

            cikti = f"""📊 <b>Hız Testi Sonuçları</b> 📊

<u><b>Müşteri:</b></u>
<b>» ISP:</b> {sonuc['client']['isp']}
<b>» Ülke:</b> {sonuc['client']['country']}
<b>» Konum:</b> <a href="{client_map}">Haritada Göster</a>

<u><b>Sunucu:</b></u>
<b>» Adı:</b> {sonuc['server']['name']}
<b>» Ülke:</b> {sonuc['server']['country']}, {sonuc['server']['cc']}
<b>» Sponsor:</b> {sonuc['server']['sponsor']}
<b>» Ping:</b> {ping_ms} ms
<b>» Konum:</b> <a href="{server_map}">Haritada Göster</a>

<b>» İndirme:</b> {indir_mbps} Mbps {indir_grafik}
<b>» Yükleme:</b> {yukle_mbps} Mbps {yukle_grafik}
"""

            share_url = sonuc.get("share")
            if share_url:
                await m.reply_photo(
                    share_url, caption=cikti, parse_mode=ParseMode.HTML
                )
            else:
                await m.reply_text(cikti, parse_mode=ParseMode.HTML)

            await m_edit.delete()
            test_kuyrugu.popleft()  # Kuyruktan çıkar
