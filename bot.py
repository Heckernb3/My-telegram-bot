import os
import telebot

# Render থেকে টোকেনটি অটোমেটিক নেবে
API_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

# কেউ /start দিলে এই উত্তর দেবে
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "অভিনন্দন! আপনার ম্যানেজার বট এখন পুরোপুরি সচল।")

# যেকোনো মেসেজ দিলে রিপ্লাই দেবে (টেস্টের জন্য)
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "আমি আপনার মেসেজ পেয়েছি!")

if __name__ == "__main__":
    bot.infinity_polling()
