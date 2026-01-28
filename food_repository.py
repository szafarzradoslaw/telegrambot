from database import get_connection
from dataclasses import dataclass
from errors import FoodNotFoundError
from typing import Optional

@dataclass(frozen=True)
class Food:
    id: int
    name: str
    calories_per_100g: float
    protein_per_100g: float
    carbs_per_100g: float
    fat_per_100g: float
    gram_per_portion: Optional[float] = None

def add_food(
        name: str,
        calories_per_100g: float,
        protein_per_100g: float,
        fat_per_100g: float,
        carbs_per_100g: float,
        gram_per_portion: Optional[float] = None
    ) -> int:   
    
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO foods (name, calories_per_100g, protein_per_100g, fat_per_100g, carbs_per_100g, gram_per_portion) VALUES (?, ?, ?, ?, ?, ?)",
                (name, calories_per_100g, protein_per_100g, fat_per_100g, carbs_per_100g, gram_per_portion)
            )
        return cursor.lastrowid

def get_food_by_name(name: str) -> Food | None:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT id, name, calories_per_100g, protein_per_100g, fat_per_100g, carbs_per_100g, gram_per_portion
            FROM foods
            WHERE LOWER(name) = ?
            """,
            (name.lower(),)
        )   
        row = cursor.fetchone()
        if row is None:
            raise FoodNotFoundError(f"Food '{name}' not found in database.")

        return Food(**dict(row))
    
if __name__ == "__main__":
    print(get_food_by_name("Banana"))