import os
import logging
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# 1. Mengambil API Key dari GitHub Secrets
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    print("Error: Token Telegram atau Gemini API Key tidak ditemukan!")
    sys.exit(1)

# 2. Konfigurasi Google Gemini
genai.configure(api_key=GEMINI_API_KEY)
# Menggunakan model gemini-2.5-flash yang sangat cepat dan gratis
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction="Kamu adalah asisten AI yang pintar, ramah, dan membantu dalam bahasa Indonesia."
)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Saya adalah bot AI berbasis Google Gemini yang berjalan via GitHub Actions.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        # Mengirim teks ke Google Gemini
        response = model.generate_content(user_text)
        ai_reply = response.text
        await update.message.reply_text(ai_reply)
    except Exception as e:
        logging.error(f"Error AI: {e}")
        await update.message.reply_text(f"⚠️ Terjadi error pada API Gemini:\n`{str(e)}`")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot Gemini sedang berjalan...")
    app.run_polling()

if __name__ == '__main__':
    main()
    
