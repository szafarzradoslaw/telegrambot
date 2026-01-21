from database import get_connection

def add_food(
        name: str,
        calories_per_100g: float,
        protein_per_100g: float,
        fat_per_100g: float,
        carbs_per_100g: float
    ) -> int:
    
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO foods (name, calories_per_100g, protein_per_100g, fat_per_100g, carbs_per_100g) VALUES (?, ?, ?, ?, ?)",
                (name, calories_per_100g, protein_per_100g, fat_per_100g, carbs_per_100g)
            )
        return cursor.lastrowid

def get_food_by_name(name: str):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM foods WHERE name = ?",
            (name,)
        )
        if row:
            return row.fetchone()
        return None