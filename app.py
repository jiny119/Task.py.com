import streamlit as st

# User Data (Temporary)
users = {"admin": "1234"}  # username: password

# Session State Initialization
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

def login_page():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state["logged_in"] = True
            st.experimental_rerun()
        else:
            st.error("Invalid Username or Password")

def main_app():
    st.title("Earn Coins by Completing Tasks!")
    st.subheader("✅ Complete Tasks")
    st.button("Watch Ad (5 Coins)")
    st.button("Complete Survey (5 Coins)")
    st.button("Install App (5 Coins)")

    st.subheader("👥 Referral System")
    st.button("Refer a Friend (5 Coins)")

    st.subheader("🎯 Click Ads")
    st.button("Click Ad (5 Coins)")

    st.subheader("🏆 Your Balance")
    st.write("💰 0 Coins")

    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.experimental_rerun()

# Login System Check
if not st.session_state["logged_in"]:
    login_page()
else:
    main_app()
