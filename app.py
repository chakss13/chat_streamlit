# app.py

import streamlit as st
from session import login, signup
from messaging import send_message, get_messages
from db import users_collection, messages_collection

def main():
    # Configure the Streamlit app's page
    st.set_page_config(page_title="Messaging Client", layout="wide")
    st.title("🚀 Messaging Client")

    # Initialize session state for username if not already set
    if 'username' not in st.session_state:
        st.session_state['username'] = None

    # Sidebar Navigation
    if st.session_state['username']:
        st.sidebar.header(f"Welcome, {st.session_state['username']}!")
        if st.sidebar.button("Logout"):
            st.session_state['username'] = None
            st.experimental_rerun()  # Refresh the app to update the UI
    else:
        # Allow users to choose between Login and Sign Up
        choice = st.sidebar.selectbox("Choose Action", ["Login", "Sign Up"])
        if choice == "Login":
            login()
        else:
            signup()

    # Main Interface for Logged-In Users
    if st.session_state['username']:
        user = st.session_state['username']
        st.subheader(f"Hello, {user}! Start messaging below ✉️")

        # Create a two-column layout: Users list and Chat area
        col1, col2 = st.columns([1, 3])

        with col1:
            st.header("📋 Users")
            search_query = st.text_input("🔍 Search Users", key='search_users')

            if search_query:
                # Search for users matching the query, excluding the current user
                available_users = [u['username'] for u in users_collection.find({
                    "username": {"$regex": search_query, "$options": "i"},
                    "username": {"$ne": user}
                })]
            else:
                # Display all users except the current user
                available_users = [u['username'] for u in users_collection.find({"username": {"$ne": user}})]

            if available_users:
                # Dropdown to select a user to chat with
                selected_user = st.selectbox("Select User to Chat", available_users)
            else:
                st.info("No other users available to message.")
                selected_user = None

        with col2:
            if selected_user:
                st.header(f"💬 Chat with {selected_user}")

                # Retrieve all messages between the logged-in user and the selected user
                messages = get_messages(user, selected_user)

                # Display the chat history
                chat = ""
                for msg in messages:
                    timestamp = msg['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                    if msg['sender'] == user:
                        chat += f"**You** [{timestamp}]: {msg['message']}\n"
                    else:
                        chat += f"**{msg['sender']}** [{timestamp}]: {msg['message']}\n"

                st.text_area("Chat", value=chat, height=300, max_chars=None, key='chat_area', disabled=True)

                # Message Input Form
                with st.form(key='message_form', clear_on_submit=True):
                    message_input = st.text_input("Type your message here", key='message_input')
                    submit_button = st.form_submit_button(label="Send")

                    if submit_button:
                        if message_input.strip() != "":
                            send_message(user, selected_user, message_input)
                            st.success("Message sent!")
                            # No need to manually clear the input; clear_on_submit=True handles it
                        else:
                            st.error("Cannot send an empty message.")
    else:
        st.info("Please log in or sign up to start messaging.")

if __name__ == "__main__":
    main()