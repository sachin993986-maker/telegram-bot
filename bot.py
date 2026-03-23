import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

TOKEN ="8718264717:AAHoPITsR4IfuqaU8VnHddAvb471nQqEmwg"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello bhai! 🤖 Bot live ho gaya 🚀")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Tumne likha: {update.message.text}")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, reply))

    print("Bot chal raha hai...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
