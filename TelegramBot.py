import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = "8064163574:AAG7aiyepD2eDW47M-oaKFkAkBqDmcSRvYg"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! Send me a long URL and I'll shorten it for you!"
    )

async def shorten_url(url: str) -> str:
    try:
        response = requests.get(f"http://tinyurl.com/api-create.php?url={url}")
        response.raise_for_status()
        return response.text
    except Exception as e:
        logging.error(f"Error shortening URL: {e}")
        return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    logging.info(f"Received message: {user_message}")
    
    if user_message.startswith(('http://', 'https://')):
        short_url = await shorten_url(user_message)
        if short_url:
            reply = f"Shortened URL:\n{short_url}"
        else:
            reply = "Failed to shorten URL. Please try again later."
    else:
        reply = "Please send a valid URL starting with http:// or https://"
    
    await update.message.reply_text(reply)

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logging.info("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
