import json
from pathlib import Path
from errors import FoodNotFoundError, UnitConversionError

# Load JSON
DATA_PATH = Path(__file__).parent / "food_data.json"
with open(DATA_PATH, "r", encoding="utf-8") as f:
    foods = json.load(f)

def get_food_macros(food_name: str):
    food = foods.get(food_name.lower())
    if food is None:
        raise FoodNotFoundError(f"Food '{food_name}' not found in database.")
    return food

def convert_units_to_grams(amount: float, unit: str, food_name: str) -> float:
    unit_key = unit.lower()
    food = get_food_macros(food_name.lower())
    UNIT_MULTIPLIER = {
        "g": 1,
        "kg": 1000,
        "ml": 1,   # for milk/water
        "l": 1000,
        "portion": food.get("portion_grams", 100),  # default to 100g if not specified
        "x": food.get("portion_grams", 100)  # same as portion
    }
    if unit_key not in UNIT_MULTIPLIER:
        raise UnitConversionError(f"Unit '{unit}' not recognized.")

    return amount * UNIT_MULTIPLIER[unit_key]
    

def calculate_macros(food_name: str, amount: float, unit: str):
    food = get_food_macros(food_name)
    grams = convert_units_to_grams(amount, unit, food_name)
    macros = {
        "calories": food["calories_per_100g"] * grams / 100,
        "protein": food["protein_per_100g"] * grams / 100,
        "fat": food["fat_per_100g"] * grams / 100,
        "carbs": food["carbs_per_100g"] * grams / 100,
    }
    return macros