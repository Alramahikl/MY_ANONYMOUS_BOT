import telebot

BOT_TOKEN = "8217929766:AAFLqeGkNXgbuoeTFiHURop1-_JC90hPFPA"
YOUR_PERSONAL_ID = 618255891 

bot = telebot.TeleBot(BOT_TOKEN)

# Dictionary to keep track of messages (maps your forwarded message ID to the sender's User ID)
# Format: { forwarded_message_id : original_sender_user_id }
message_map = {}

# 1. Welcome Message
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام😁🌷 پیامت رو برام بفرست")

# 2. Handling Incoming Anonymous Messages & Replies
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    # CASE A: If YOU are replying to a message that the bot forwarded to you
    if message.chat.id == YOUR_PERSONAL_ID and message.reply_to_message:
        orig_msg_id = message.reply_to_message.message_id
        
        if orig_msg_id in message_map:
            target_user_id = message_map[orig_msg_id]
            try:
                # Send your reply back to the anonymous user
                bot.send_message(target_user_id, message.text)
                bot.reply_to(message, "پاسخ شما ارسال شد. ✅")
            except Exception as e:
                bot.reply_to(message, "خطا در ارسال پیام. ممکن است کاربر ربات را بلاک کرده باشد.")
        else:
            bot.reply_to(message, "⚠️ نتوانستم فرستنده این پیام را پیدا کنم. (شاید ربات ریستارت شده است)")
            
    # CASE B: Someone else is sending an anonymous message to you
    elif message.chat.id != YOUR_PERSONAL_ID:
        try:
            # Forward the text to you
            sent_msg = bot.send_message(YOUR_PERSONAL_ID, f"📩 پیام ناشناس جدید:\n\n{message.text}")
            
            # Save the link between the message you got and the person who sent it
            message_map[sent_msg.message_id] = message.chat.id
            
            # Confirm to the sender
            bot.reply_to(message, "فرستادم😌✨")
        except Exception as e:
            bot.reply_to(message, "An error occurred. Make sure the admin has started the bot.")
            print(f"Error: {e}")

print("Bot is starting up successfully...")
bot.infinity_polling()