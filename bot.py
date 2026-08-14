import os
import asyncio
import logging
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

# SETUP LOGGING
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 1. GET TOKEN & PORT
TOKEN = os.environ.get('TELEGRAM_TOKEN')
PORT = int(os.environ.get('PORT', 8080))

if not TOKEN:
    print("❌ ERROR: TELEGRAM_TOKEN environment variable is missing!")
    exit(1)

print("🤖 Starting Guaraná.ch Bot using Flask...")

# 2. BUILD APPLICATION
application = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context):
    language_keyboard = [
        [InlineKeyboardButton("Français", callback_data='FR'), 
         InlineKeyboardButton("English", callback_data='EN'), 
         InlineKeyboardButton("Deutsch", callback_data='DE')]
    ]
    reply_markup = InlineKeyboardMarkup(language_keyboard)
    
    try:
        with open('logo.png', 'rb') as photo:
            await update.message.reply_photo(photo=photo)
    except Exception:
        pass

    await update.message.reply_text(
        "👋 Bienvenue sur Guaraná.ch\nChoisis ta langue pour accéder au catalogue :",
        reply_markup=reply_markup
    )

async def button_click(update: Update, context):
    query = update.callback_query
    await query.answer() 

    main_menu_keyboard = [
        [InlineKeyboardButton("🛍️ Open shop", url="https://example.com")], 
        [InlineKeyboardButton("📞 Contact us", url="https://t.me/FavelaTerpsPackz")]
    ]
    reply_markup = InlineKeyboardMarkup(main_menu_keyboard)

    if query.data == 'EN':
        try:
            with open('logo.png', 'rb') as photo:
                await query.message.reply_photo(photo=photo)
        except Exception:
            pass
        await query.message.reply_text(
            text="🤗 Welcome to Guaraná.ch!\nThanks for your trust – order quickly via the shop 👇",
            reply_markup=reply_markup
        )
    elif query.data == 'FR':
        try:
            with open('logo.png', 'rb') as photo:
                await query.message.reply_photo(photo=photo)
        except Exception:
            pass
        await query.message.reply_text(
            text="🤗 Bienvenue sur Guaraná.ch!\nMerci de votre confiance – commandez rapidement via la boutique 👇",
            reply_markup=reply_markup
        )
    elif query.data == 'DE':
        try:
            with open('logo.png', 'rb') as photo:
                await query.message.reply_photo(photo=photo)
        except Exception:
            pass
        await query.message.reply_text(
            text="🤗 Willkommen bei Guaraná.ch!\nDanke für dein Vertrauen – bestelle schnell über den Shop 👇",
            reply_markup=reply_markup
        )

# 3. ADD HANDLERS
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button_click))

# 4. CREATE FLASK APP
app = Flask(__name__)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(), application.bot)
    application.process_update(update)
    return "OK", 200

@app.route("/", methods=["GET"])
def health():
    return "Bot is alive!", 200

# 5. ASYNC STARTUP (ALL IN ONE FUNCTION)
async def startup():
    print("🔄 Clearing ghost connections...")
    await application.bot.delete_webhook(drop_pending_updates=True)
    await application.initialize()
    
    # Set webhook
    railway_url = f"https://{os.environ.get('RAILWAY_PUBLIC_DOMAIN', 'localhost')}"
    await application.bot.set_webhook(url=f"{railway_url}/{TOKEN}")
    
    print(f"✅ Webhook set to: {railway_url}/{TOKEN}")
    print("✅ Bot is live! Go to Telegram and type /start")

if __name__ == '__main__':
    # RUN ASYNC STARTUP FIRST
    asyncio.run(startup())
    
    # THEN RUN FLASK (This prevents the 'Event loop is closed' crash!)
    app.run(host="0.0.0.0", port=PORT)
