import streamlit as st
import json
import pymongo
# Title
st.set_page_config(page_title="Home", initial_sidebar_state="collapsed"
)
st.title("Welcome to 🧠 ThinkFlow!")

# Pretty Box
def pretty_box(text, color="#4CAF50"):
    st.markdown(
        f"""
        <div style="
            background-color: {color}; 
            padding: 15px; 
            border-radius: 10px;
            color: black; 
            font-size: 16px;
            font-weight: normal;
            text-align: center;
            box-shadow: 3px 3px 10px rgba(0,0,0,0.2);
            ">
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )

# Display Example Boxes
pretty_box("I am an AI-powered digital learning enhancement tool. \n Please enter your details below to step into a new world of learning!", "#B1D4E0")  # Blue Box
st.write("")
st.write("")
st.write("")
st.write("")

# MongoDB Connection (Use your actual connection string)
MONGO_URI = "mongodb+srv://hack:ritika@hack.6nemp.mongodb.net/?retryWrites=true&w=majority&appName=Hack"
client = pymongo.MongoClient(MONGO_URI)
db = client["mind_map_db"]  # Database Name
collection = db["User"] 

# Collect user information
name = st.text_input("Enter your name")
email = st.text_input("Enter your email")
age = st.selectbox(
    "Select your age group:",
    ("8-12", "12-18", "18+"),
)
difficulty = st.selectbox("Select difficult level: ", ("Easy", "Medium", "Hard"))

user = {
    'name': name,
    'email': email,
    'age': age,
    'difficulty': difficulty
}

with open("user.json", "w") as file:
    json.dump(user, file, indent=4)
    

print("User profile saved!")

# Store data in session state
if st.button("Continue to Mind Map Generator"):
    if name and email and age and difficulty:
        st.session_state["user_info"] = {
            "name": name,
            "email": email,
            "age": age,
            "difficulty": difficulty
        }
        collection.insert_one(st.session_state["user_info"] )
        st.success("Information saved! Redirecting...")
        st.switch_page("pages\MindMapGen.py")  # Redirect to the mind map app
    else:
        st.error("Please fill in all fields before proceeding.")
