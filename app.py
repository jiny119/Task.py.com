import json
import bcrypt
import streamlit as st
import os

# Set Streamlit Page Config
st.set_page_config(page_title="Task Web App", page_icon="✅", layout="centered")

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

# Hash password
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Verify password
def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# Signup function
def signup(username, password):
    users = load_users()
    if username in users:
        return False, "Username already exists!"
    users[username] = hash_password(password)
    save_users(users)
    return True, "Signup successful! You can now login."

# Login function
def login(username, password):
    users = load_users()
    if username not in users:
        return False, "User not found!"
    if not verify_password(password, users[username]):
        return False, "Incorrect password!"
    return True, "Login successful!"

# Streamlit UI
st.title("Task Web App")

# Sidebar Menu
menu = st.sidebar.selectbox("Menu", ["Signup", "Login"])

if menu == "Signup":
    st.subheader("Create a New Account")
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    if st.button("Signup"):
        success, message = signup(new_username, new_password)
        st.success(message) if success else st.error(message)

elif menu == "Login":
    st.subheader("Login to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        success, message = login(username, password)
        if success:
            st.success(message)
            st.subheader("Welcome to the Task Dashboard!")  # Show dashboard after login
        else:
            st.error(message)
