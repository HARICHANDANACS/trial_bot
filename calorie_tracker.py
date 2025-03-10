import requests

HF_API_KEY = "api key"  # Replace with your actual API key
MODEL_URL = "https://api-inference.huggingface.co/models/your-text-model"

HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

# Function to get calorie information from Hugging Face API
def get_calories(food_item):
    payload = {"inputs": food_item}
    
    try:
        response = requests.post(MODEL_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        data = response.json()
        
        if isinstance(data, list) and len(data) > 0:
            return data[0].get("generated_text", "Calorie info not available.")
        elif isinstance(data, dict):
            return data.get("generated_text", "Calorie info not available.")
        else:
            return "Calorie info not available."
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
