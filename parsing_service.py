import re

# "120g banana"
PATTERN_AMOUNT_UNIT_BEGINNING = re.compile(
    r"^(?P<amount>\d+)\s*(?P<unit>[a-zA-Z]+)\s+(?P<food>[a-zA-Z ]+)$"
)

# "banana 120g"
PATTERN_AMOUNT_UNIT_ENDING = re.compile(
    r"^(?P<food>[a-zA-Z ]+)\s+(?P<amount>\d+)\s*(?P<unit>[a-zA-Z]+)$"
)

def prarse_food_input(user_input: str):
    text = user_input.strip().lower()

    for pattern in (PATTERN_AMOUNT_UNIT_BEGINNING, PATTERN_AMOUNT_UNIT_ENDING):
            match = pattern.match(text)
            if match:
                return {
                    "food": match.group("food").strip(),
                    "amount": int(match.group("amount")),
                    "unit": match.group("unit"),
                }
            
    parts = text.split()
    if len(parts) == 2 and parts[0].isdigit():
        return {
            "food": parts[1],
            "amount": int(parts[0]),
            "unit": "portion",
        }
    if len(parts) == 2 and parts[1].isdigit():
        return {
            "food": parts[0],
            "amount": int(parts[1]),
            "unit": "portion",
        }
    
    return {
        "food": text,
        "amount": 1,
        "unit": "portion",
    }