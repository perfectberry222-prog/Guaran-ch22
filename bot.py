import os
import asyncio
from quart import Quart, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

# 1. GET TOKEN & PORT
TOKEN = os.environ.get('TELEGRAM_TOKEN')
PORT = int(os.environ.get('PORT', 8080))

if not TOKEN:
    print("❌ ERROR: TELEGRAM_TOKEN environment variable is missing!")
    exit(1)

print("🤖 Starting Guaraná.ch Bot using Quart Webhook...")

# 2. BUILD APPLICATION
application = ApplicationBuilder().token(TOKEN).build()

# START COMMAND
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

# HANDLE BUTTON CLICKS
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

# 4. CREATE QUART APP (Async compatible!)
app = Quart(__name__)

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(await request.get_json(), application.bot)
    application.process_update(update)
    return "OK", 200

@app.route("/", methods=["GET"])
async def health():
    return "Bot is alive!", 200

# 5. STARTUP
if __name__ == '__main__':
    async def startup_tasks():
        # Force disconnect
        print("🔄 Nuking all ghost connections...")
        await application.bot.delete_webhook(drop_pending_updates=True)
        
        # Initialize bot
        await application.initialize()
        
        # Set webhook
        railway_url = os.environ.get('RAILWAY_PUBLIC_DOMAIN', None)
        if railway_url:
            full_url = f"https://{railway_url}/{TOKEN}"
        else:
            print("⚠️ WARNING: RAILWAY_PUBLIC_DOMAIN not set! Using default.")
            full_url = f"https://localhost/{TOKEN}"
            
        await application.bot.set_webhook(url=full_url)
        
        print(f"✅ Webhook set to: {full_url}")
        print("✅ Bot is live! Go to Telegram and type /start")

    # Run the async setup, then start Quart
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(startup_tasks())
    
    # Run Quart (This doesn't close the loop like Flask does!)
    app.run(host="0.0.0.0", port=PORT, loop=loop)
