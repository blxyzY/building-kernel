import os
import logging
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai
from google.genai import types

# 1. Mengambil API Key dari GitHub Secrets
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    print("Error: Token Telegram atau Gemini API Key tidak ditemukan!")
    sys.exit(1)

# 2. Inisialisasi Google Gen AI Client terbaru
client = genai.Client(api_key=GEMINI_API_KEY)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Saya adalah bot AI berbasis Google Gemini Lite yang hemat kuota.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        # MENGGUNAKAN MODEL LITE YANG LEBIH HEMAT KUOTA
        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=user_text,
            config=types.GenerateContentConfig(
                system_instruction="Kamu adalah asisten AI yang pintar, ramah, dan membantu dalam bahasa Indonesia."
            )
        )
        ai_reply = response.text
        await update.message.reply_text(ai_reply)
        
    except Exception as e:
        logging.error(f"Error AI: {e}")
        error_msg = str(e).upper()
        
        # Penanganan error kuota habis secara halus agar ramah pengguna
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            await update.message.reply_text("😴 Maaf, otak AI saya sedang lelah karena terlalu banyak pertanyaan hari ini. Silakan coba lagi besok ya!")
        else:
            await update.message.reply_text("⚠️ Terjadi gangguan koneksi pada server AI. Silakan coba sesaat lagi.")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot Gemini Lite terbaru sedang berjalan...")
    app.run_polling()

if __name__ == '__main__':
    main()
    
