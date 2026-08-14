import os
import sys
import time
import threading
import random
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# --- CRASH PREVENTION LOCK ---
# If the bot restarts too fast, Railway is stuck in a loop.
# This forces the bot to wait a random time before starting to clear ghost processes.
time.sleep(random.randint(3, 8))
print("🚀 Starting up...")

# --- DUMMY WEB SERVER TO KEEP RAILWAY ALIVE ---
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is online!")

def start_webserver():
    port = int(os.environ.get('PORT', 8080))
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    print(f"🌐 Keep-Alive server started on port {port}")
    server.serve_forever()

# Start the webserver in a background thread immediately
thread = threading.Thread(target=start_webserver, daemon=True)
thread.start()
# -------------------------------------------------

# 1. START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    language_keyboard = [
        [InlineKeyboardButton("Français", callback_data='FR'), 
         InlineKeyboardButton("English", callback_data='EN'), 
         InlineKeyboardButton("Deutsch", callback_data='DE')]
    ]
    reply_markup = InlineKeyboardMarkup(language_keyboard)
    
    try:
        await update.message.reply_photo(photo=open('logo.png', 'rb'))
    except Exception:
        pass

    await update.message.reply_text(
        "👋 Bienvenue sur Guaraná.ch\nChoisis ta langue pour accéder au catalogue :",
        reply_markup=reply_markup
    )

# 2. HANDLE BUTTON CLICKS
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    main_menu_keyboard = [
        [InlineKeyboardButton("🛍️ Open shop", url="https://example.com")], 
        [InlineKeyboardButton("📞 Contact us", url="https://t.me/FavelaTerpsPackz")]
    ]
    reply_markup = InlineKeyboardMarkup(main_menu_keyboard)
    
    if query.data == 'EN':
        # ------- IMAGE ADDED HERE FOR ENGLISH -------
        try:
            await query.message.reply_photo(photo=open('logo.png', 'rb'))
        except Exception:
            pass
        # -------------------------------------------
        
        await query.message.reply_text(
            text="🤗 Welcome to Guaraná.ch!\nThanks for your trust – order quickly via the shop 👇",
            reply_markup=reply_markup
        )
    elif query.data == 'FR':
        try:
            await query.message.reply_photo(photo=open('logo.png', 'rb'))
        except Exception:
            pass
        await query.message.reply_text(
            text="🤗 Bienvenue sur Guaraná.ch!\nMerci de votre confiance – commandez rapidement via la boutique 👇",
            reply_markup=reply_markup
        )
    elif query.data == 'DE':
        try:
            await query.message.reply_photo(photo=open('logo.png', 'rb'))
        except Exception:
            pass
        await query.message.reply_text(
            text="🤗 Willkommen bei Guaraná.ch!\nDanke für dein Vertrauen – bestelle schnell über den Shop 👇",
            reply_markup=reply_markup
        )

# 3. MAIN ASYNC FUNCTION
async def main():
    TOKEN = os.environ.get('TELEGRAM_TOKEN')
    if not TOKEN:
        print("Error: TELEGRAM_TOKEN environment variable not set!")
        return
        
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_click))
    
    await application.initialize()
    
    # Force kill stale webhooks before polling starts
    await application.bot.delete_webhook(drop_pending_updates=True)
    
    await application.updater.start_polling()
    print("✅ Bot is running! Go to Telegram and type /start")
    
    try:
        while True:
            await asyncio.sleep(3600)
    except KeyboardInterrupt:
        pass
    finally:
        await application.updater.stop()
        await application.shutdown()

# 4. RUN THE BOT
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
