# app.py

import streamlit as st
from auth import register_user, authenticate_user, get_all_users
from messaging import send_message, get_messages
from db import cursor, conn
from utils import hash_password, check_password

# Set the title of the Streamlit app
st.title("✨ Messaging App")

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ''

# Function to handle user logout
def logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = ''
    st.success("You have been logged out.")

# Display Logout button if user is logged in
if st.session_state['logged_in']:
    st.sidebar.button("🔒 Logout", on_click=logout)

# Define menu options based on login status
if st.session_state['logged_in']:
    menu = ["Home", "Messages"]
else:
    menu = ["Home", "Register", "Login"]

# Navigation menu in the main area instead of the sidebar
choice = st.selectbox("Main Menu", menu)

# Handle the "Register" option
if choice == "Register":
    st.header("📝 Create a New Account")
    with st.form(key="register_form"):
        username = st.text_input("📛 Username")
        password = st.text_input("🔒 Password", type="password")
        confirm_password = st.text_input("🔒 Confirm Password", type="password")
        submit_button = st.form_submit_button("🚀 Register")

    if submit_button:
        if not username or not password or not confirm_password:
            st.error("⚠️ Please fill in all fields.")
        elif password != confirm_password:
            st.error("⚠️ Passwords do not match.")
        else:
            success, message = register_user(username, password)
            if success:
                st.success(message)
            else:
                st.error(message)

# Handle the "Login" option
elif choice == "Login":
    st.header("🔑 Login to Your Account")
    with st.form(key="login_form"):
        username = st.text_input("📛 Username")
        password = st.text_input("🔒 Password", type="password")
        login_button = st.form_submit_button("🚀 Login")

    if login_button:
        if not username or not password:
            st.error("⚠️ Please enter both username and password.")
        elif authenticate_user(username, password):
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.success(f"🎉 Welcome, {username}!")
        else:
            st.error("❌ Invalid username or password.")

# Handle the "Home" option
elif choice == "Home":
    st.header("🏠 Home")
    st.write("Welcome to the Messaging App! Please register or log in to continue.")

# Handle the "Messages" option
elif choice == "Messages":
    if st.session_state.get('logged_in'):
        st.header("💬 Your Messages")

        # Section to send a new message
        st.subheader("📨 Send a Message")
        with st.form(key="send_message_form"):
            recipient = st.selectbox("➡️ Select Recipient", get_all_users(st.session_state['username']))
            message = st.text_area("✍️ Message")
            send_button = st.form_submit_button("📤 Send")

        if send_button:
            if not message.strip():
                st.error("⚠️ Message cannot be empty.")
            else:
                success, msg = send_message(st.session_state['username'], recipient, message)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)

        # Section to view messages with a specific user
        st.subheader("📥 View Messages")
        selected_user = st.selectbox("👥 Chat With", get_all_users(st.session_state['username']))
        if selected_user:
            messages = get_messages(st.session_state['username'], selected_user)
            if messages:
                for msg in messages:
                    timestamp = msg['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
                    sender = msg['sender']
                    content = msg['message']
                    if sender == st.session_state['username']:
                        # Messages sent by the user
                        st.markdown(f"**You** [{timestamp}]: {content}")
                    else:
                        # Messages received by the user
                        st.markdown(f"**{sender}** [{timestamp}]: {content}")
            else:
                st.info("📭 No messages to display with this user.")
    else:
        st.error("⚠️ You need to log in to view and send messages.")
