import asyncio
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

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

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    # bot ko alive rakhne ke liye
    while True:
        await asyncio.sleep(10)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
