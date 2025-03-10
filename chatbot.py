import requests
from config import HF_API_KEY, MODEL_URL

# Function to query Hugging Face model
def get_nutrition_response(user_input):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": user_input}

    try:
        response = requests.post(MODEL_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            return data[0].get("generated_text", "Sorry, I couldn't understand that.")
        elif isinstance(data, dict):
            return data.get("generated_text", "Sorry, I couldn't understand that.")
        else:
            return "Sorry, I couldn't understand that."
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
