import streamlit as st

# Local Storage for Users (Temporary Login System)
if "users" not in st.session_state:
    st.session_state.users = {"admin": {"password": "admin", "coins": 0, "tasks_completed": 0, "referrals": 0, "clicks": 0}}

# Function for User Authentication
def authenticate(username, password):
    users = st.session_state.users
    return username in users and users[username]["password"] == password

# Function to Register New User
def register(username, password):
    if username in st.session_state.users:
        return False
    st.session_state.users[username] = {"password": password, "coins": 0, "tasks_completed": 0, "referrals": 0, "clicks": 0}
    return True

# Streamlit UI
st.set_page_config(page_title="Task Earning App", page_icon="💰", layout="centered")

st.markdown(
    """
    <style>
    body { background-color: #121212; color: white; }
    .css-1d391kg { background: rgba(0, 0, 0, 0.6); border-radius: 10px; padding: 20px; }
    </style>
    """, unsafe_allow_html=True
)

st.title("🪙 Earn Coins by Completing Tasks!")

# Login / Signup UI
menu = st.sidebar.selectbox("Menu", ["Login", "Sign Up"])
if menu == "Login":
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if authenticate(username, password):
            st.session_state["logged_in"] = True
            st.session_state["current_user"] = username
            st.experimental_rerun()
        else:
            st.sidebar.error("Invalid Credentials!")

elif menu == "Sign Up":
    new_user = st.sidebar.text_input("New Username")
    new_pass = st.sidebar.text_input("New Password", type="password")
    if st.sidebar.button("Register"):
        if register(new_user, new_pass):
            st.sidebar.success("Account Created! Please Login.")
        else:
            st.sidebar.error("Username Already Exists!")

# Dashboard (After Login)
if "logged_in" in st.session_state and st.session_state["logged_in"]:
    user = st.session_state["current_user"]
    st.sidebar.success(f"Logged in as {user}")

    # Coin Balance
    st.subheader(f"💰 Your Balance: {st.session_state.users[user]['coins']} Coins")
    
    # Task Section
    st.subheader("🎯 Complete Tasks")
    if st.button("✅ Watch Ad (5 Coins)"):
        st.session_state.users[user]["coins"] += 5
        st.session_state.users[user]["tasks_completed"] += 1
        st.experimental_rerun()
    
    if st.button("📝 Complete Survey (5 Coins)"):
        st.session_state.users[user]["coins"] += 5
        st.session_state.users[user]["tasks_completed"] += 1
        st.experimental_rerun()
    
    if st.button("📲 Install App (5 Coins)"):
        st.session_state.users[user]["coins"] += 5
        st.session_state.users[user]["tasks_completed"] += 1
        st.experimental_rerun()
    
    # Referral System
    st.subheader("👥 Referral System")
    if st.button("Refer a Friend (10 Coins)"):
        st.session_state.users[user]["coins"] += 10
        st.session_state.users[user]["referrals"] += 1
        st.experimental_rerun()

    # Ad Click System
    st.subheader("🖱️ Click Ads (5 Coins)")
    if st.button("Click Ad"):
        st.session_state.users[user]["coins"] += 5
        st.session_state.users[user]["clicks"] += 1
        st.experimental_rerun()

    # Withdrawal Section
    st.subheader("💸 Withdraw Coins")
    if st.session_state.users[user]["coins"] >= 15000:
        withdraw_method = st.selectbox("Select Withdrawal Method", ["JazzCash", "EasyPaisa", "Payoneer", "PayPal"])
        withdraw_button = st.button("Withdraw")
        if withdraw_button:
            st.success(f"Withdrawal request sent via {withdraw_method}!")
    else:
        st.warning("You need at least 15,000 coins to withdraw.")

    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.experimental_rerun()
