import os
import logging
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# 1. Mengambil API Key dari Environment Variables GitHub
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    print("Error: Token Telegram atau OpenAI API Key tidak ditemukan!")
    sys.exit(1)

client = OpenAI(api_key=OPENAI_API_KEY)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Saya adalah bot AI yang berjalan via GitHub Actions.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Kamu adalah asisten AI yang pintar dalam bahasa Indonesia."},
                {"role": "user", "content": user_text}
            ]
        )
        ai_reply = response.choices.message.content
        await update.message.reply_text(ai_reply)
    except Exception as e:
        logging.error(f"Error AI: {e}")
        # Mengubah baris ini agar memunculkan detail error asli dari OpenAI ke Telegram
        await update.message.reply_text(f"⚠️ Terjadi error pada API OpenAI:\n`{str(e)}`")


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot sedang berjalan...")
    app.run_polling()

if __name__ == '__main__':
    main()
