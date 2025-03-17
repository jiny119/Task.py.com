import streamlit as st
import bcrypt
import pandas as pd

# Fake Database (Local Dictionary for Testing)
users_db = {}
tasks = [
    {"id": 1, "task": "Watch an Ad", "completed": False},
    {"id": 2, "task": "Complete a Survey", "completed": False},
    {"id": 3, "task": "Install a Gaming App", "completed": False},
]

# Function to Hash Password
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Function to Verify Password
def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# Signup Function
def signup(username, password):
    if username in users_db:
        return False, "Username already exists!"
    hashed_pw = hash_password(password)
    users_db[username] = hashed_pw
    return True, "Signup successful! You can now login."

# Login Function
def login(username, password):
    if username not in users_db:
        return False, "User not found!"
    if verify_password(password, users_db[username]):
        st.session_state["logged_in"] = True
        st.session_state["username"] = username
        return True, "Login successful!"
    return False, "Incorrect password!"

# Mark Task as Completed
def complete_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            break

# Logout Function
def logout():
    st.session_state["logged_in"] = False
    st.session_state["username"] = None

# Streamlit UI
st.title("Task Earning App")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    option = st.selectbox("Select an option", ["Login", "Signup"])

    if option == "Signup":
        st.subheader("Create an Account")
        new_username = st.text_input("Choose a Username")
        new_password = st.text_input("Choose a Password", type="password")
        if st.button("Signup"):
            success, message = signup(new_username, new_password)
            st.success(message) if success else st.error(message)

    else:
        st.subheader("Login to Your Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            success, message = login(username, password)
            st.success(message) if success else st.error(message)

else:
    st.subheader(f"Welcome, {st.session_state['username']}!")

    # Task Dashboard
    st.write("### Your Tasks")
    task_df = pd.DataFrame(tasks)
    st.table(task_df)

    task_id = st.number_input("Enter Task ID to Complete", min_value=1, max_value=len(tasks), step=1)
    if st.button("Mark as Completed"):
        complete_task(task_id)
        st.success(f"Task {task_id} marked as completed!")

    if st.button("Logout"):
        logout()
        st.experimental_rerun()
