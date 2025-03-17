import json
import bcrypt
import streamlit as st
import os

# Set Streamlit Page Config
st.set_page_config(page_title="Task Web App", page_icon="✅", layout="centered")

DB_FILE = "users.json"
TASKS_FILE = "tasks.json"

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

# Load tasks from file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    return {}

# Save tasks to file
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file)

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
st.title("🎯 Task Web App")

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
    st.subheader("🔑 Login to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        success, message = login(username, password)
        if success:
            st.success(message)
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
        else:
            st.error(message)

# Task Dashboard (If logged in)
if "logged_in" in st.session_state and st.session_state["logged_in"]:
    st.subheader(f"🚀 Welcome, {st.session_state['username']}!")

    # Stylish Task Dashboard Layout
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="💰 Coins", value="500")
    with col2:
        st.metric(label="📝 Tasks Completed", value="2 / 10")
    with col3:
        st.metric(label="🎯 Referral Progress", value="3 / 10")

    st.markdown("---")
    
    # Show Tasks
    st.subheader("📌 Your Tasks for Today")
    
    tasks = load_tasks()
    if st.session_state["username"] not in tasks:
        tasks[st.session_state["username"]] = [
            {"task": "Watch an ad", "completed": False},
            {"task": "Complete a survey", "completed": False},
            {"task": "Install a gaming app", "completed": False},
        ]
        save_tasks(tasks)

    user_tasks = tasks[st.session_state["username"]]
    
    for i, task in enumerate(user_tasks):
        with st.expander(f"🔹 {task['task']}"):
            if task["completed"]:
                st.success("✅ Task Completed!")
            else:
                if st.button(f"Mark as Complete ✅", key=i):
                    user_tasks[i]["completed"] = True
                    save_tasks(tasks)
                    st.experimental_rerun()
    
    st.markdown("---")
    st.subheader("💸 Withdraw Your Earnings")
    if st.button("Withdraw Now"):
        st.warning("Minimum 15,000 coins required for withdrawal!")

    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = None
        st.experimental_rerun()
