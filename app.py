import streamlit as st
import pandas as pd
import json
import os

# Load or Create User Data
USER_DATA_FILE = "users.json"
if not os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, "w") as f:
        json.dump({}, f)

with open(USER_DATA_FILE, "r") as f:
    users = json.load(f)

# Streamlit Page Configuration
st.set_page_config(page_title="Tasking App", layout="wide")

# Sidebar - Login/Signup
st.sidebar.image("logo.png", use_column_width=True)
st.sidebar.title("Login / Signup")

choice = st.sidebar.selectbox("Login or Signup", ["Login", "Signup"])
username = st.sidebar.text_input("Enter Username")
password = st.sidebar.text_input("Enter Password", type="password")

if choice == "Signup":
    if username in users:
        st.sidebar.warning("Username already exists! Try a different one.")
    elif st.sidebar.button("Create Account"):
        users[username] = {"password": password, "coins": 0, "referrals": 0}
        with open(USER_DATA_FILE, "w") as f:
            json.dump(users, f)
        st.sidebar.success("Account Created! Now Login.")

if choice == "Login":
    if username in users and users[username]["password"] == password:
        st.sidebar.success(f"Welcome {username}!")
        logged_in = True
    else:
        st.sidebar.warning("Invalid Username or Password")
        logged_in = False

if "logged_in" in locals() and logged_in:
    st.title("Welcome to Tasking Web App")
    st.markdown("### Earn by Completing Tasks!")
    st.write("**Available Tasks:** Watch Ads, Install Apps, Complete Surveys, Play Games")

    # Tasking System
    tasks = [
        {"name": "Watch Ad", "coins": 5},
        {"name": "Install App", "coins": 5},
        {"name": "Complete Survey", "coins": 5},
        {"name": "Play Game", "coins": 5},
    ]

    for task in tasks:
        if st.button(f"Complete {task['name']}"):
            users[username]["coins"] += task["coins"]
            with open(USER_DATA_FILE, "w") as f:
                json.dump(users, f)
            st.success(f"You earned {task['coins']} coins!")

    # Show User Coins
    st.sidebar.subheader("Your Coins")
    st.sidebar.write(f"Total Coins: {users[username]['coins']}")

    # Referral System
    st.sidebar.subheader("Referral System")
    ref_code = st.sidebar.text_input("Enter Referral Code (if any)")
    if st.sidebar.button("Submit Referral"):
        users[username]["referrals"] += 1
        with open(USER_DATA_FILE, "w") as f:
            json.dump(users, f)
        st.sidebar.success("Referral Added Successfully!")

    # Withdraw System
    st.subheader("Withdraw Coins")
    coins_to_withdraw = st.number_input("Enter Coins to Withdraw", min_value=15000, step=5000)
    if st.button("Request Withdrawal"):
        if users[username]["coins"] >= coins_to_withdraw:
            users[username]["coins"] -= coins_to_withdraw
            with open(USER_DATA_FILE, "w") as f:
                json.dump(users, f)
            st.success("Withdrawal Request Sent!")
        else:
            st.error("Not enough coins!")

    # Leaderboard
    st.subheader("Leaderboard")
    leaderboard = sorted(users.items(), key=lambda x: x[1]["coins"], reverse=True)
    leaderboard_df = pd.DataFrame(leaderboard, columns=["User", "Data"])
    leaderboard_df["Coins"] = leaderboard_df["Data"].apply(lambda x: x["coins"])
    leaderboard_df = leaderboard_df[["User", "Coins"]]
    st.table(leaderboard_df)
