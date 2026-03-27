import os
import logging
from flask import Flask, request, jsonify
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Get bot token from environment variable
TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("No TELEGRAM_TOKEN set in environment")

# Initialize Bot and Application (without building a dispatcher)
bot = Bot(token=TOKEN)
application = Application.builder().token(TOKEN).build()

# Define command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm a simple echo bot. Send me any message and I'll repeat it.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

# Register handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Webhook endpoint
@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    """Receive updates from Telegram."""
    try:
        update = Update.de_json(request.get_json(force=True), bot)
        application.update_queue.put_nowait(update)
        return "ok", 200
    except Exception as e:
        logger.error(f"Error processing update: {e}")
        return "error", 500

@app.route("/")
def index():
    return "Bot is running!"

# Set webhook on startup (optional: you can set it manually or here)
def set_webhook():
    """Set the webhook for the bot."""
    webhook_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/webhook/{TOKEN}"
    if not os.environ.get("RENDER_EXTERNAL_HOSTNAME"):
        logger.warning("RENDER_EXTERNAL_HOSTNAME not set, skipping webhook set")
        return
    result = bot.set_webhook(webhook_url)
    if result:
        logger.info(f"Webhook set successfully to {webhook_url}")
    else:
        logger.error("Failed to set webhook")

# Set webhook when the app starts (this runs in the main thread)
with app.app_context():
    set_webhook()

if __name__ == "__main__":
    # Run Flask on Render's assigned port
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
