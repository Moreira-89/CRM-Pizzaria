import streamlit as st

def login_view():
    st.title("Login Page")
    
    # Create a form for user login
    with st.form(key='login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        # Submit button
        submit_button = st.form_submit_button(label='Login')
        
        if submit_button:
            if username == "admin" and password == "password":
                st.success("Login successful!")
            else:
                st.error("Invalid username or password.")