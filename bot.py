import os
import time
import requests
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

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

thread = threading.Thread(target=start_webserver, daemon=True)
thread.start()
# -------------------------------------------------

TOKEN = os.environ.get('TELEGRAM_TOKEN')
if not TOKEN:
    print("❌ ERROR: TELEGRAM_TOKEN missing!")
    exit(1)

# 1. Force kill any ghost bots before starting
print("🛑 Force-killing ghost bots...")
requests.get(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook?drop_pending_updates=true")

last_update_id = 0

print("🤖 Bot is running! Go to Telegram and type /start")

while True:
    try:
        # 2. Ask Telegram for new messages
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={last_update_id + 1}&timeout=30"
        response = requests.get(url)
        data = response.json()

        if not data['ok']:
            print("⚠️ Telegram API error:", data)
            time.sleep(2)
            continue

        # 3. Process each message
        for update in data['result']:
            last_update_id = update['update_id']
            
            # Detect if it's a button click or a text message
            if 'callback_query' in update:
                # BUTTON CLICK
                callback = update['callback_query']
                chat_id = callback['message']['chat']['id']
                data_cb = callback['data']

                # Build the second menu buttons
                menu_keyboard = {
                    "inline_keyboard": [
                        [{"text": "🛍️ Open shop", "url": "https://example.com"}],
                        [{"text": "📞 Contact us", "url": "https://t.me/FavelaTerpsPackz"}]
                    ]
                }

                # Send image + menu for each language
                try:
                    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", 
                                  data={'chat_id': chat_id}, 
                                  files={'photo': open('logo.png', 'rb')})
                except Exception:
                    pass

                if data_cb == 'EN':
                    text = "🤗 Welcome to Guaraná.ch!\nThanks for your trust – order quickly via the shop 👇"
                elif data_cb == 'FR':
                    text = "🤗 Bienvenue sur Guaraná.ch!\nMerci de votre confiance – commandez rapidement via la boutique 👇"
                elif data_cb == 'DE':
                    text = "🤗 Willkommen bei Guaraná.ch!\nDanke für dein Vertrauen – bestelle schnell über den Shop 👇"
                else:
                    text = "..."

                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                              json={'chat_id': chat_id, 'text': text, 'reply_markup': menu_keyboard})

            elif 'message' in update:
                # TEXT COMMAND (/start)
                msg = update['message']
                chat_id = msg['chat']['id']
                text = msg.get('text', '')

                if text == '/start':
                    # Send Logo + French menu
                    try:
                        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", 
                                      data={'chat_id': chat_id}, 
                                      files={'photo': open('logo.png', 'rb')})
                    except Exception:
                        pass

                    lang_keyboard = {
                        "inline_keyboard": [
                            [
                                {"text": "Français", "callback_data": "FR"},
                                {"text": "English", "callback_data": "EN"},
                                {"text": "Deutsch", "callback_data": "DE"}
                            ]
                        ]
                    }

                    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                                  json={
                                      'chat_id': chat_id,
                                      'text': "👋 Bienvenue sur Guaraná.ch\nChoisis ta langue pour accéder au catalogue :",
                                      'reply_markup': lang_keyboard
                                  })
                    
    except Exception as e:
        print(f"💥 Crash prevented: {e}")
        time.sleep(3)
