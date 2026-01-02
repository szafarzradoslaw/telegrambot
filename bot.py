from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_USERNAME: Final = "@szafarzbot"

# TAKING TOKEN
import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

# COMMANDS
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("START")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("HELP")

async def customcommand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("CUSTOM COMMAND")

# COMMAND RESPONSES
def handle_response(text: str) -> str: 
    text = text.lower()

    if "hello" in text:
        return "hello"
    else:
        return "no hello"
    
# MESSEGE HANDLER
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # 1. Send message to backend (for now: print to terminal)
    print(f"Received message: {text}")

    # 2. Optional: process or respond
    response = handle_response(text)
    await update.message.reply_text(response)


if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("customcommand", customcommand))

    # Messages
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )
    # START THE BOT
    app.run_polling()