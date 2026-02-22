"""Script to insert dummy calorie data for testing metrics across multiple days and weeks."""
import sys
from datetime import datetime, timedelta
from random import randint, choice

# Add the Calorie_Tracker directory to path
sys.path.insert(0, '/Users/illorente/Desktop/Hackathon/calorieCounter_python/Calorie_Tracker')

from database import get_database

db = get_database()

# Sample food items with calorie values
foods = [
    ("Apple", 95),
    ("Banana", 105),
    ("Chicken Breast", 165),
    ("Rice Bowl", 206),
    ("Salad", 150),
    ("Pasta", 221),
    ("Burger", 540),
    ("Pizza Slice", 285),
    ("Yogurt", 120),
    ("Almonds", 164),
    ("Salmon", 280),
    ("Eggs", 155),
    ("Bread", 80),
    ("Cheese", 115),
    ("Chocolate", 235),
    ("Oatmeal", 150),
    ("Sandwich", 350),
    ("Nuts", 200),
]

# Realistic meal times throughout the day
meal_times = [7, 8, 9, 12, 13, 14, 18, 19, 20, 21]

# Get the first user (assuming user_id = 1)
user_id = 1

# Generate data for 3 weeks (21 days)
now = datetime.now()

for day_offset in range(21):
    current_date = now - timedelta(days=day_offset)
    
    # Vary daily calories between 1500-2500
    daily_total = randint(1500, 2500)
    
    # Insert 3-5 food items per day
    num_meals = randint(3, 5)
    remaining = daily_total
    used_times = set()
    
    for i in range(num_meals):
        food_name, base_cal = choice(foods)
        
        # Slight variation on base calories
        calories = base_cal + randint(-30, 30)
        
        # Last meal gets remaining calories
        if i == num_meals - 1:
            calories = max(remaining, 1)
        else:
            remaining -= calories
        
        # Pick random time that hasn't been used
        available_times = [t for t in meal_times if t not in used_times]
        hour = choice(available_times)
        used_times.add(hour)
        minute = randint(0, 59)
        
        # Create timestamp
        logged_at = current_date.replace(hour=hour, minute=minute, second=0)
        
        # Insert into database
        db.execute(
            """
            INSERT INTO calories 
            (user_id, calories, food_name, food_type, quantity, unit, source, logged_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, calories, food_name, "food", 1, "serving", "estimate", logged_at.strftime('%Y-%m-%d %H:%M:%S.%f'))
        )
        
        print(f"Inserted: {food_name} ({calories} cal) on {logged_at}")

print("\n✓ Dummy data insertion complete! 21 days of data inserted.")
