# session.py

import streamlit as st
from auth import authenticate_user, register_user

def login():
    """
    Renders the login form in the sidebar using Streamlit Forms.
    """
    st.sidebar.header("Login")
    
    with st.sidebar.form(key='login_form'):
        login_username = st.text_input("Username")
        login_password = st.text_input("Password", type='password')
        submit_button = st.form_submit_button(label='Login')
        
        if submit_button:
            if authenticate_user(login_username, login_password):
                st.session_state['username'] = login_username
                st.success("Logged in successfully!")
                # No rerun; Streamlit will naturally update the UI on next interaction
            else:
                st.error("Invalid username or password.")

def signup():
    """
    Renders the signup form in the sidebar using Streamlit Forms.
    """
    st.sidebar.header("Sign Up")
    
    with st.sidebar.form(key='signup_form'):
        signup_username = st.text_input("Username for Sign Up")
        signup_password = st.text_input("Password for Sign Up", type='password')
        submit_button = st.form_submit_button(label='Sign Up')
        
        if submit_button:
            success, message = register_user(signup_username, signup_password)
            if success:
                st.success(message)
                st.session_state['username'] = signup_username  # Auto-login after signup
            else:
                st.error(message)