import json
from pathlib import Path

def print_user_message(text: str) -> None:
    print(f"[FOOD SERVICE] Received: {text}")

# Load JSON
DATA_PATH = Path(__file__).parent / "food_data.json"
with open(DATA_PATH, "r", encoding="utf-8") as f:
    foods = json.load(f)

def get_food_macros(food_name: str):
    return foods.get(food_name.lower())

def convert_units_to_grams(amount: float, unit: str, food_name: str) -> float:
    unit = unit.lower()
    food = foods.get(food_name.lower())
    if not food:
        print(f"WARNING: food_service.py - Food '{food_name}' not found")
        return None
    
    UNIT_MULTIPLIER = {
        "g": 1,
        "kg": 1000,
        "ml": 1,   # for milk/water
        "l": 1000,
        "portion": food.get("portion_grams", 100),  # default to 100g if not specified
    }
    if unit not in UNIT_MULTIPLIER:
        print(f"WARNING: Unsupported unit '{unit}'")
        return None
    
    return amount * UNIT_MULTIPLIER[unit]
    

def calculate_macros(food_name: str, amount: float, unit: str):
    food = get_food_macros(food_name)
    if not food:
        print(f"WARNING:calculate_macros.py - Food '{food_name}' not found")
        return None
    
    grams = convert_units_to_grams(amount, unit, food_name)
    if grams is None:
        print(f"WARNING:calculate_macros.py - Cannot convert {amount} {unit} of '{food_name} to grams'")
        return None
    macros = {
        "calories": food["calories_per_100g"] * grams / 100,
        "protein": food["protein_per_100g"] * grams / 100,
        "fat": food["fat_per_100g"] * grams / 100,
        "carbs": food["carbs_per_100g"] * grams / 100,
    }
    return macros