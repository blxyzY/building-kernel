import logging
import time
import asyncio
import os  # Ditambahkan untuk membaca Environment Variables dari GitHub
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai
from google.genai import types

# Mengaktifkan LOGGING untuk memantau aktivitas bot di terminal
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# =========================================================================
# KONFIGURASI AMAN (Membaca dari GitHub Secrets / Environment Variables)
# =========================================================================
TELEGRAM_TOKEN = "8910446402:AAHcPSOJsRb-6HlgrPWPUbsxkEZVn2UcJrw"
GEMINI_API_KEY = "AQ.Ab8RN6ITpk1rnV9dr_hLqhhVrYIgfoh0c3XZ2zu3PxDHM46BHA"

MODEL_NAME = "gemini-2.5-flash"

# Validasi awal untuk memastikan variabel lingkungan sudah terisi
if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    logging.critical("ERROR: TELEGRAM_TOKEN atau GEMINI_API_KEY belum diatur di Environment Variables / GitHub Secrets!")
    exit(1)

# Inisialisasi klien resmi Google GenAI SDK
client = genai.Client(api_key=GEMINI_API_KEY)

# Fungsi ketika user mengetik /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Halo! Saya bot ahli kernel Linux.\n\n"
        "Silakan kirimkan teks log error compile kernel Anda langsung ke sini, "
        "atau unggah file dokumen log (.txt/.log). Saya akan menganalisis solusinya dengan sistem Auto-Retry!"
    )

# Fungsi utama untuk memproses pesan teks & dokumen log
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = ""

    # Cek jika pengguna mengirim File Dokumen (.txt atau .log)
    if update.message.document:
        await update.message.reply_text("Log file terdeteksi. Mengunduh dan menganalisis teks...")
        file = await context.bot.get_file(update.message.document.file_id)
        file_bytes = await file.download_as_bytearray()
        user_input = file_bytes.decode('utf-8', errors='ignore')
    # Cek jika pengguna mengirim teks biasa
    elif update.message.text:
        user_input = update.message.text
    else:
        return

    # Ambil 150 baris terakhir jika teks terlalu panjang (mencegah overload token Telegram/AI)
    lines = user_input.splitlines()
    if len(lines) > 150:
        user_input = "\n".join(lines[-150:])

    # Instruksi System Prompt Pintar untuk Pakar Kernel
    system_instruction = (
        "Anda adalah seorang pengembang senior kernel Linux dan Android OS (Kernel Developer). "
        "Tugas utama Anda adalah menganalisis error kompilasi kernel yang dikirim pengguna. "
        "Berikan jawaban dalam Bahasa Indonesia yang jelas, runut, dan langsung ke solusi teknis. "
        "Sebutkan file dan baris mana yang bermasalah, jelaskan penyebabnya, dan berikan contoh "
        "perbaikan kodenya atau perintah git/patch yang harus dijalankan."
    )

    max_retries = 3      # Maksimal mencoba ulang jika Google overload
    retry_delay = 4      # Jeda waktu menunggu sebelum coba lagi (dalam detik)
    response_stream = None

    for attempt in range(max_retries):
        try:
            # Panggil AI Gemini dengan metode Streaming
            response_stream = client.models.generate_content_stream(
                model=MODEL_NAME,
                contents=user_input,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.2,
                )
            )
            break # Jika sukses terkoneksi ke AI, keluar dari loop pencarian (retry)
            
        except Exception as e:
            # Jika terkena eror server sibuk (503), jalankan fungsi tunggu dan coba lagi
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                if attempt < max_retries - 1:
                    logging.warning(f"Server Google sibuk (503). Mencoba ulang ke-{attempt + 1} dalam {retry_delay} detik...")
                    await asyncio.sleep(retry_delay)
                    continue
            
            # Jika eror lain atau jatah mencoba ulang sudah habis, tampilkan ke user
            logging.error(f"Error AI terjadi: {str(e)}")
            await update.message.reply_text(f"Gagal memproses ke AI. Error: {str(e)}")
            return

    # Jika berhasil terkoneksi, mulai proses pengaliran teks ke Telegram
    if response_stream:
        try:
            current_chunk = ""
            for chunk in response_stream:
                if chunk.text:
                    current_chunk += chunk.text
                    
                    # Batasi pengiriman per 1500 karakter agar struktur Markdown tidak berantakan
                    if len(current_chunk) >= 1500:
                        try:
                            await update.message.reply_text(current_chunk, parse_mode="Markdown")
                        except Exception:
                            await update.message.reply_text(current_chunk)
                        current_chunk = ""
                        await asyncio.sleep(0.5) # Jeda singkat untuk menghindari batasan spam API Telegram
                        
            if current_chunk:
                try:
                    await update.message.reply_text(current_chunk, parse_mode="Markdown")
                except Exception:
                    await update.message.reply_text(current_chunk)
        except Exception as stream_error:
            logging.error(f"Error saat streaming teks: {str(stream_error)}")

def main():
    # Membangun aplikasi Telegram bot
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT | filters.Document.ALL, handle_message))
    
    print("=== BOT KERNEL SIAP JALAN (DENGAN PROTEKSI RETRY 503) ===")
    app.run_polling()

if __name__ == '__main__':
    main()
