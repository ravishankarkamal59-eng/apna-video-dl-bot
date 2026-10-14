import telebot
import os
import yt_dlp
import threading
from flask import Flask

# यहाँ अपना नया टोकन डालें
BOT_TOKEN = '8482930052:AAHTDbcF0u-OwLGZA2yHIw2jsVKK3OBAlbg'
bot = telebot.TeleBot(BOT_TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running successfully!"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "नमस्ते भाई! मुझे वीडियो का लिंक भेजें, मैं डाउनलोड करके आपको भेज दूंगा। (कॉपीराइट वीडियो के लिए परमिशन जरूरी है)")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    if "http" not in url:
        bot.reply_to(message, "कृपया एक सही वीडियो लिंक भेजें।")
        return
        
    bot.reply_to(message, "वीडियो डाउनलोड हो रहा है, कृपया प्रतीक्षा करें...")
    
    try:
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': 'video.mp4',
            'quiet': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        with open("video.mp4", "rb") as video:
            bot.send_video(message.chat.id, video)
            
        os.remove("video.mp4")
        
    except Exception as e:
        bot.reply_to(message, f"एरर: {str(e)}")

def run_bot():
    print("बॉट चालू हो गया है...")
    bot.polling(none_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
