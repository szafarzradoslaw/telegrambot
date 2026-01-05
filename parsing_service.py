import re
def print_user_message(text: str) -> None:
    print(f"[FOOD SERVICE] Recived: {text}")

def food_parsing(text: str):
    text = text.strip().lower()
    match = re.match(r"^(\d+(?:\.\d+)?)([a-zA-Z]+)\s+(.+)$", text)
    if not match:
        return None
    
    amount = float(match.group(1))   # e.g. 120
    unit = match.group(2)            # e.g. g
    food_name = match.group(3)       # e.g. banana
    return amount, unit, food_name