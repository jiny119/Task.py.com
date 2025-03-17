import streamlit as st
import json
import os
import bcrypt

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
        json.dump(users, file, indent=4)

# Function to Hash Password
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Function to Verify Password
def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# Signup Function
def signup(username, password):
    users = load_users()
    if username in users:
        return False, "Username already exists!"
    
    users[username] = {
        "password": hash_password(password),
        "tasks": {
            "Watch an Ad": False,
            "Complete a Survey": False,
            "Install a Gaming App": False
        }
    }
    save_users(users)
    return True, "Signup successful! You can now login."

# Login Function
def login(username, password):
    users = load_users()
    if username not in users:
        return False, "User not found!"
    
    if verify_password(password, users[username]["password"]):
        return True, "Login successful!"
    return False, "Incorrect password!"

# Mark Task as Completed
def complete_task(username, task):
    users = load_users()
    if username in users and task in users[username]["tasks"]:
        users[username]["tasks"][task] = True
        save_users(users)
        return f"Task '{task}' completed!"
    return "Task not found!"

# Streamlit UI
st.title("Task Web App")

menu = st.sidebar.selectbox("Menu", ["Signup", "Login"])

if menu == "Signup":
    st.subheader("Create an Account")
    new_user = st.text_input("Choose a Username")
    new_pass = st.text_input("Choose a Password", type="password")

    if st.button("Signup"):
        success, message = signup(new_user, new_pass)
        if success:
            st.success(message)
        else:
            st.error(message)

elif menu == "Login":
    st.subheader("Login to Your Account")
    user = st.text_input("Username")
    passwd = st.text_input("Password", type="password")

    if st.button("Login"):
        success, message = login(user, passwd)
        if success:
            st.success(message)

            # Show tasks after login
            users = load_users()
            st.subheader("Your Tasks:")
            for task, completed in users[user]["tasks"].items():
                if not completed:
                    if st.button(f"Complete: {task}"):
                        st.success(complete_task(user, task))
        else:
            st.error(message)
