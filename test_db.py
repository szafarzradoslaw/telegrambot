from database import get_connection
from food_repository import add_food, get_food_by_name

food_id = add_food("Banana", 89, 1.1, 0.3, 23)
print(f"Food added with ID: {food_id}")

food = get_food_by_name("Banana")
print("Retrieved food:", dict(food) if food else "Not found")

with get_connection() as conn:
    rows = conn.execute("SELECT * FROM foods").fetchall()
    for row in rows:
        print(dict(row))