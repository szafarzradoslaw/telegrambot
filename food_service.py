import json
from pathlib import Path

# Load JSON
DATA_PATH = Path(__file__).parent / "food_data.json"
with open(DATA_PATH, "r", encoding="utf-8") as f:
    foods = json.load(f)

def get_food_macros(food_name: str):
    return foods.get(food_name.lower())

def calculate_macros(food_name: str, amount: float, unit: str):
    food = get_food_macros(food_name)
    if not food:
        return None

    # Convert amount to grams if necessary
    if unit == "g":
        weight_in_grams = amount
    elif unit == "kg":
        weight_in_grams = amount * 1000
    else:
        return None  # Unsupported unit

    factor = weight_in_grams / 100.0

    macros = {
        "calories": food["calories_per_100g"] * factor,
        "protein": food["protein_per_100g"] * factor,
        "fat": food["fat_per_100g"] * factor,
        "carbs": food["carbs_per_100g"] * factor,
    }
    return macros