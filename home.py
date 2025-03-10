import streamlit as st
import app  # ✅ Explicitly import the app module
from meal_plan import fetch_meal_plan

# ✅ Ensure this is the first Streamlit command
st.set_page_config(page_title="Nutritional Chatbot", page_icon="🥗", layout="wide")

# Sidebar Navigation
st.sidebar.title("Nutritional Chatbot")
page = st.sidebar.radio("Navigation", ["Chat", "Meal Planning", "About"])

if page == "Chat":
    app.main()  # ✅ Call a function inside app.py

elif page == "Meal Planning":
    st.title("Meal Planning & Suggestions")
    st.write("Click the button below to get a random meal suggestion.")

    if st.button("Get Meal Suggestion"):
        meal = fetch_meal_plan()
        if "error" in meal:
            st.error(meal["error"])
        else:
            st.subheader(meal["strMeal"])
            st.image(meal["strMealThumb"], use_column_width=True)
            st.write(f"**Category:** {meal['strCategory']}")
            st.write(f"**Cuisine:** {meal['strArea']}")
            st.write(f"🔗 [Recipe Instructions]({meal['strSource']})")
            st.write("---")

elif page == "About":
    st.title("About")
    st.write("This chatbot provides reliable nutrition advice and meal planning suggestions.")

# ✅ Footer
st.markdown(
    "<hr><center>Built using Streamlit | © 2025 | Developed by Chandana</center>",
    unsafe_allow_html=True
)
