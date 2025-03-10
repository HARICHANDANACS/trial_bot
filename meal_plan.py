import requests
import random

# Free API for meal plans (Indian & International)
API_URL = "https://www.themealdb.com/api/json/v1/1/filter.php?a={}"

def fetch_meal_plan(cuisine):
    try:
        response = requests.get(API_URL.format(cuisine))
        response.raise_for_status()
        meals = response.json().get("meals")

        if not meals:
            return {"error": "No meal suggestions available for this cuisine."}

        # Pick 3 random meals for a structured meal plan
        selected_meals = random.sample(meals, min(len(meals), 3))
        return selected_meals
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching meals: {e}"}
