from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from google.generativeai import configure, GenerativeModel
import requests
import nest_asyncio
import asyncio

nest_asyncio.apply()

# تنظیمات
TELEGRAM_TOKEN = '729864260:v4YYzPGxvatHPCKrnfUr7h4DyDN9ATxgjahyUHxg'
RPI_URL = 'http://آی‌پی‌رزبری:5000/control?device=light&action=on'
GEMINI_API_KEY = 'AIzaSyDGw45ZF4KzfBjRy3Qnp9CVVhKzu25amhg'

# پیکربندی مدل
configure(api_key=GEMINI_API_KEY)
model = GenerativeModel("gemini-pro")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    if "چراغ" in user_text or "روشن" in user_text:
        try:
            requests.get(RPI_URL)
            await update.message.reply_text("چراغ روشن شد! 💡")
        except Exception as e:
            await update.message.reply_text(f"خطا در اتصال به رزبری‌پای: {e}")
    else:
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)

async def main_async():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).base_url("https://tapi.bale.ai/").build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

if __name__ == '__main__':
    asyncio.run(main_async())
