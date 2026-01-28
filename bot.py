import os
from typing import Final

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from parsing_service import parse_food_input
from food_service import calculate_macros
from errors import TelegramBotTokenError, FoodParsingError, FoodNotFoundError, UnitConversionError

BOT_USERNAME: Final = "@szafarzbot"
load_dotenv()
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise TelegramBotTokenError("TELEGRAM_BOT_TOKEN is not set") 

# COMMANDS
#async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#    await update.message.reply_text("START")

#async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#    await update.message.reply_text("HELP")

#async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#    await update.message.reply_text("CUSTOM COMMAND")

def print_user_message(text: str) -> None:
    print(f"Received: {text}")

async def handle_response(update: Update) -> str:
    text = update.message.text
    print_user_message(text)

    try:
        parsed = parse_food_input(text)
    except FoodParsingError:
        return 'Wrong format. Please use: "120g banana"'
    
    try:
        macros = calculate_macros(parsed.name, parsed.amount, parsed.unit)
    except FoodNotFoundError as error:
        return f"Error: {error}"
    except UnitConversionError as error:
        return f"Error: {error}"
    
    return f"""{parsed.name.upper()} ({parsed.amount}{parsed.unit}):
    - Calories: {round(macros['calories'], 2)}kcal
    - Protein: {round(macros['protein'], 2)}g
    - Carbohydrates: {round(macros['carbs'], 2)}g
    - Fats: {round(macros['fat'], 2)}g
    """

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = await handle_response(update)
    await update.message.reply_text(response)

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()

    # Commands
    #app.add_handler(CommandHandler("start", start_command))
    #app.add_handler(CommandHandler("help", help_command))
    #app.add_handler(CommandHandler("customcommand", custom_command))

    # Messages
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )
    # START THE BOT
    app.run_polling()