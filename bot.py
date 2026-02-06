import asyncio
from flask import Flask
import threading
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from groq import Groq

TOKEN = "8407425681:AAGdbUvAvx5lU5JQGRnzX5J4voPPr0NSSiM"
API_KEY = "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"

client = Groq(api_key=API_KEY)
app_server = Flask(__name__)

@app_server.route('/')
def home(): return "Bot is Alive"

async def reply(update, context):
    if not update.message or not update.message.text: return
    try:
        chat = client.chat.completions.create(
            messages=[{"role": "user", "content": update.message.text}],
            model="llama-3.1-70b-versatile",
        )
        await update.message.reply_text(chat.choices[0].message.content)
    except Exception as e: print(e)

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_server.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    bot = ApplicationBuilder().token(TOKEN).build()
    bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), reply))
    bot.run_polling()
