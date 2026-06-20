import os
import telebot
from flask import Flask, request

BOT_TOKEN = "8217929766:AAFLqeGkNXgbuoeTFiHURop1-_JC90hPFPA"
YOUR_PERSONAL_ID = 618255891 

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
app = Flask(__name__)

# Dictionary to keep track of messages
message_map = {}

# 1. Welcome Message
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام😁🌷 پیامت رو برام بفرست")

# 2. Handling Incoming Anonymous Messages & Replies
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    if message.chat.id == YOUR_PERSONAL_ID and message.reply_to_message:
        orig_msg_id = message.reply_to_message.message_id
        if orig_msg_id in message_map:
            target_user_id = message_map[orig_msg_id]
            try:
                bot.send_message(target_user_id, message.text)
                bot.reply_to(message, "پاسخ شما ارسال شد. ✅")
            except Exception:
                bot.reply_to(message, "خطا در ارسال پیام.")
        else:
            bot.reply_to(message, "⚠️ نتوانستم فرستنده این پیام را پیدا کنم.")
            
    elif message.chat.id != YOUR_PERSONAL_ID:
        try:
            sent_msg = bot.send_message(YOUR_PERSONAL_ID, f"📩 پیام ناشناس جدید:\n\n{message.text}")
            message_map[sent_msg.message_id] = message.chat.id
            bot.reply_to(message, "فرستادم😌✨")
        except Exception as e:
            print(f"Error: {e}")

@app.route('/' + BOT_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    # This automatically hooks into your Render instance
    bot.set_webhook(url=f"https://my-anonymous-bot-2xsk.onrender.com/{BOT_TOKEN}")
    return "Bot is running!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
