import os
from typing import Final

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from parsing_service import parse_food_input
from food_service import calculate_macros

BOT_USERNAME: Final = "@szafarzbot"

def print_user_message(text: str) -> None:
    print(f"[FOOD SERVICE] Received: {text}")

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
    parsed = parse_food_input(text)
    if parsed is None:
        await update.message.reply_text(
            'Wrong format. Please use: "120g banana"'
        )
        return
    food_name = parsed["food"]
    amount = parsed["amount"]
    unit = parsed["unit"]

    macros = calculate_macros(food_name, amount, unit)
    if macros is None:
        await update.message.reply_text(
            f"Could not find nutritional information for '{food_name}'."
        )
        return 
    response = f"""You have entered: {amount}{unit} of {food_name}.
        Calories: {macros['calories']}
        Protein: {macros['protein']}
        Carbs: {macros['carbs']}
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