import os
import telebot

# Render-এর Environment Variable থেকে টোকেন নেবে
API_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

# /start কমান্ডের উত্তর
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "হ্যালো! আপনার ম্যানেজার বট এখন সচল আছে।")

# যেকোনো টেক্সট মেসেজের উত্তর (টেস্ট করার জন্য)
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "আমি আপনার মেসেজ পেয়েছি!")

# বট চালু করার মেইন ফাংশন
if __name__ == "__main__":
    print("Bot is starting...")
    bot.infinity_polling()
