import streamlit as st
import requests
from meal_plan import fetch_meal_plan
from calorie_tracker import get_calories  # New module for calorie tracking

# Hugging Face API Config
HF_API_KEY = "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"
MODEL_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"

# Function to query Hugging Face model for chatbot
def get_nutrition_response(user_input):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": user_input}

    try:
        response = requests.post(MODEL_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and len(data) > 0 and "generated_text" in data[0]:
            return data[0]["generated_text"]
        elif isinstance(data, dict) and "generated_text" in data:
            return data["generated_text"]
        else:
            return "Sorry, I couldn't understand that."
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Streamlit Page Config
st.set_page_config(page_title="Nutritional Chatbot", page_icon="🥗", layout="wide")

# Sidebar Navigation
st.sidebar.title("Nutritional Chatbot")
page = st.sidebar.radio("Navigation", ["Chat", "Meal Planning", "Calorie Tracker", "About"])

# Chatbot Tab
if page == "Chat":
    st.title("Nutritional Chatbot")
    st.write("Ask any nutrition-related questions and get instant responses.")

    # Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display Previous Messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Input
    user_input = st.chat_input("Ask me anything about diet, nutrition, and healthy eating.")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Get chatbot response
        response = get_nutrition_response(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Display chatbot response
        with st.chat_message("assistant"):
            st.markdown(response)

# Meal Planning Tab
elif page == "Meal Planning":
    st.title("Meal Planning & Suggestions")

    # User selects a cuisine
    cuisine = st.selectbox("Choose a Cuisine", ["Indian", "Chinese", "Italian", "Mexican"])

    if st.button("Get Meal Plan"):
        meal_plan = fetch_meal_plan(cuisine)

        if "error" in meal_plan:
            st.error(meal_plan["error"])
        else:
            for meal_time, meal in meal_plan.items():
                if meal:
                    st.subheader(f"{meal_time}: {meal['strMeal']}")
                    st.image(meal["strMealThumb"], width=300)  # Reduced image size
                    st.write(f"🔗 [Recipe Instructions](https://www.themealdb.com/meal/{meal['idMeal']})")
                    st.write("---")

# Calorie Tracker Tab
elif page == "Calorie Tracker":
    st.title("Calorie Tracker")
    
    food_item = st.text_input("Enter a food item (e.g., Apple, Rice, Chicken)")
    
    if st.button("Get Calories"):
        calories = get_calories(food_item)
        if "error" in calories:
            st.error(calories["error"])
        else:
            st.success(f"**{food_item.capitalize()}** contains approximately **{calories['calories']} kcal** per 100g.")

# About Tab
elif page == "About":
    st.title("About")
    st.write("This chatbot provides reliable nutrition advice, meal planning suggestions, and calorie tracking.")

# Footer
st.markdown(
    "<hr><center>Built using Streamlit | © 2025 | Developed by Chandana</center>",
    unsafe_allow_html=True
)
