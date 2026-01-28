import re
from dataclasses import dataclass
from errors import FoodParsingError
# "120.5g banana" or "120,5g banana"
PATTERN_AMOUNT_UNIT_BEGINNING = re.compile(
    r"^(?P<amount>\d+(?:[.,]\d+)?)\s*(?P<unit>[a-zA-Z]+)\s+(?P<food>[a-zA-Z ]+)$"
)

# "banana 120.5g" or "banana 120,5g"
PATTERN_AMOUNT_UNIT_ENDING = re.compile(
    r"^(?P<food>[a-zA-Z ]+)\s+(?P<amount>\d+(?:[.,]\d+)?)\s*(?P<unit>[a-zA-Z]+)$"
)

@dataclass(frozen=True)
class ParsedFood:
    name: str
    amount: float
    unit: str

def is_number(value: str) -> bool:
    return bool(re.fullmatch(r"\d+(?:\.\d+)?", value))

def parse_food_input(user_input: str):
    text = user_input.strip().lower()
    text = text.replace(",", ".")  # normalize decimal separator

    for pattern in (PATTERN_AMOUNT_UNIT_BEGINNING, PATTERN_AMOUNT_UNIT_ENDING):
            match = pattern.match(text)
            if match:
                return ParsedFood(
                    name=match.group("food").strip(),
                    amount=float(match.group("amount")),
                    unit=match.group("unit"),
                )

    parts = text.split()
    
    if len(parts) == 2 and is_number(parts[0]):
        return ParsedFood(
            name=parts[1],
            amount=float(parts[0]),
            unit="portion",
        )
    
    if len(parts) == 2 and is_number(parts[1]):
        return ParsedFood(
            name=parts[0],
            amount=float(parts[1]),
            unit="portion",
        )

    if len(parts) == 1:
        return ParsedFood(
            name=text,
            amount=1,
            unit="portion",
        )

    raise FoodParsingError(f"Unrecognized food input: '{user_input}'")