import os
import logging
from telegram import Update, constants
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask
import threading

# লগিং সেটআপ (ত্রুটি খোঁজার জন্য)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Render-এর জন্য ওয়েব সার্ভার
server = Flask('')

@server.route('/')
def home():
    return "Bot is running 24/7!"

def run_web():
    server.run(host='0.0.0.0', port=8080)

# --- ফিচারের ফাংশনসমূহ ---

# ১. স্বাগতম জানানো (Welcome)
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        name = member.full_name
        await update.message.reply_text(f"স্বাগতম {name}! আমাদের গ্রুপে আসার জন্য ধন্যবাদ। নিয়ম মেনে চলবেন।")

# ২. ব্যান করা (Ban)
async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("কাকে ব্যান করব? মেসেজ রিপ্লাই দিয়ে কমান্ড দিন।")
    
    user = update.message.reply_to_message.from_user
    await context.bot.ban_chat_member(update.effective_chat.id, user.id)
    await update.message.reply_text(f"ব্যবহারকারী {user.full_name}-কে ব্যান করা হয়েছে। 🚫")

# ৩. কিক করা (Kick)
async def kick_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("কাকে কিক করব? মেসেজ রিপ্লাই দিন।")
    
    user = update.message.reply_to_message.from_user
    await context.bot.unban_chat_member(update.effective_chat.id, user.id)
    await update.message.reply_text(f"ব্যবহারকারী {user.full_name}-কে গ্রুপ থেকে বের করে দেওয়া হয়েছে।")

# ৪. মিউট করা (Mute)
async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("কাকে মিউট করব? মেসেজ রিপ্লাই দিন।")
    
    user = update.message.reply_to_message.from_user
    permissions = constants.ChatPermissions(can_send_messages=False)
    await context.bot.restrict_chat_member(update.effective_chat.id, user.id, permissions)
    await update.message.reply_text(f"{user.full_name}-কে মিউট করা হয়েছে। 🤐")

# ৫. আনমিউট করা (Unmute)
async def unmute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.reply_to_message.from_user
    permissions = constants.ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_polls=True, can_send_other_messages=True)
    await context.bot.restrict_chat_member(update.effective_chat.id, user.id, permissions)
    await update.message.reply_text(f"{user.full_name} এখন আবার কথা বলতে পারবেন। ✅")

# ৬. অটো-ডিলিট স্প্যাম লিঙ্ক (Anti-Link)
async def filter_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "http" in update.message.text or "t.me" in update.message.text:
        await update.message.delete()
        await update.message.reply_text(f"@{update.effective_user.username}, গ্রুপে লিঙ্ক শেয়ার করা নিষেধ!")

# মূল ফাংশন
def main():
    TOKEN = os.getenv("BOT_TOKEN") # Render-এ এই ভেরিয়েবল সেট করতে হবে
    
    app = Application.builder().token(TOKEN).build()
    
    # হ্যান্ডলার যোগ করা
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.add_handler(CommandHandler("ban", ban_user))
    app.add_handler(CommandHandler("kick", kick_user))
    app.add_handler(CommandHandler("mute", mute_user))
    app.add_handler(CommandHandler("unmute", unmute_user))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), filter_links))
    
    # সার্ভার শুরু
    threading.Thread(target=run_web).start()
    
    print("বট সচল হয়েছে...")
    app.run_polling()

if __name__ == '__main__':
    main()
