import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- PASTE YOUR TOKEN HERE ---
TOKEN = "8848851165:AAGptx8dtWh3q90z4KgkdEn731zHAGCpk2g"
# -----------------------------

print("🤖 Starting Guaraná.ch Bot locally...")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    await app.initialize()
    await app.bot.delete_webhook(drop_pending_updates=True)
    
    print("✅ Clearing ghost connections...")
    await app.updater.start_polling()
    print("✅ Bot is running locally! Go to Telegram and type /start")
    
    try:
        await asyncio.Future()
    except KeyboardInterrupt:
        pass
    finally:
        await app.updater.stop()
        await app.shutdown()

if __name__ == '__main__':
    asyncio.run(main())
