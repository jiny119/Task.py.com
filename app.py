import streamlit as st
import json
import os

# Database file
DB_FILE = "users.json"

# Load users from file
def load_users():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as file:
            return json.load(file)
    return {}

# Save users to file
def save_users(users):
    with open(DB_FILE, "w") as file:
        json.dump(users, file)

# Authentication function
def authenticate(username, password):
    users = load_users()
    return users.get(username) == password

# Signup function
def signup(username, password):
    users = load_users()
    if username in users:
        return False  # User already exists
    users[username] = password
    save_users(users)
    return True

# Streamlit UI
st.title("Login / Signup Page")

menu = st.selectbox("Select an option", ["Login", "Signup"])

if menu == "Signup":
    st.subheader("Create an Account")
    new_username = st.text_input("Enter Username")
    new_password = st.text_input("Enter Password", type="password")
    
    if st.button("Signup"):
        if new_username and new_password:
            if signup(new_username, new_password):
                st.success("Signup successful! Now login.")
            else:
                st.error("Username already exists!")
        else:
            st.warning("Please enter all details!")

elif menu == "Login":
    st.subheader("Login to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate(username, password):
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid username or password!")
