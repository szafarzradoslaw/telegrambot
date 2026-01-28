from parsing_service import parse_food_input
from food_service import calculate_macros
from errors import FoodNotFoundError, FoodParsingError, UnitConversionError
from telegram import Update
from telegram.ext import ContextTypes

def print_user_message(text: str) -> None:
    print(f"Received: {text}")

async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
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