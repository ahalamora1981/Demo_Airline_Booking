import streamlit as st

# Set page title
st.title("Input-Output App")

# Add text input field
user_input = st.text_input("Enter some text:")

# Add text output field
st.write("Output:", user_input)
