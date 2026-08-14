import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# 1. START COMMAND (French first)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Language selection buttons (Français, English, Deutsch)
    language_keyboard = [
        [InlineKeyboardButton("Français", callback_data='FR'), 
         InlineKeyboardButton("English", callback_data='EN'), 
         InlineKeyboardButton("Deutsch", callback_data='DE')]
    ]
    reply_markup = InlineKeyboardMarkup(language_keyboard)
    
    # Send the Guaraná.ch logo image first
    try:
        # 'logo.png' must be in the same GitHub folder as this code
        await update.message.reply_photo(photo=open('logo.png', 'rb'))
    except Exception as e:
        print(f"Image error: {e}") # Railway logs will show this if it fails

    # Send the French text with the language buttons
    await update.message.reply_text(
        "👋 Bienvenue sur Guaraná.ch\nChoisis ta langue pour accéder au catalogue :",
        reply_markup=reply_markup
    )

# 2. HANDLE BUTTON CLICKS (Language selection and menus)
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # If user selects ENGLISH
    if query.data == 'EN':
        # English Main Menu buttons
        main_menu_keyboard = [
            [InlineKeyboardButton("🛍️ Open shop", url="PUT_YOUR_SHOP_LINK_HERE")], # CHANGE THIS LATER
            [InlineKeyboardButton("📞 Contact us", url="https://t.me/FavelaTerpsPackz")]
        ]
        reply_markup = InlineKeyboardMarkup(main_menu_keyboard)
        
        # Send the English welcome text with the buttons
        await query.edit_message_text(
            text="🤗 Welcome to Guaraná.ch!\nThanks for your trust – order quickly via the shop 👇",
            reply_markup=reply_markup
        )
        
    # If user selects FRENCH
    elif query.data == 'FR':
        # (You can add a French main menu here later if you want)
        await query.edit_message_text(text="Merci d'avoir choisi le Français!")

    # If user selects GERMAN
    elif query.data == 'DE':
        await query.edit_message_text(text="Danke, dass du Deutsch gewählt hast!")

# 3. START THE BOT
if __name__ == '__main__':
    # Railway automatically injects this environment variable
    TOKEN = os.environ.get('TELEGRAM_TOKEN')
    
    if not TOKEN:
        print("Error: TELEGRAM_TOKEN environment variable not set!")
        exit(1)
        
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_click))
    
    print("Bot is running and waiting for users...")
    application.run_polling()
