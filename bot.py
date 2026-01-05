from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from parsing_service import food_parsing, print_user_message
from food_service import calculate_macros
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

# MESSAGE HANDLER
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    print_user_message(text)
    parsed = food_parsing(text)
    if parsed is None:
        await update.message.reply_text(
            'Wrong format. Please use: "120g banana"'
        )
        return
    amount, unit, food_name = parsed
    macros = calculate_macros(food_name, amount, unit)
    response = f"""You have entered: {amount}{unit} of {food_name}.
    Calories: {macros['calories']},
    Protein: {macros['protein']},
    Carbs: {macros['carbs']},
    Fat: {macros['fat']}"""
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