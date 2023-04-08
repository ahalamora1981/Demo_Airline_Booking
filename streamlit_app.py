import streamlit as st

# Set page title
st.title("Chat with Bot")

# Define function to generate bot response
def generate_response(user_input):
    # Do some processing here to generate bot response
    bot_response = "I'm sorry, I don't understand. Please try again."
    return bot_response

# Add text input field
user_input = st.text_input("You: ")

# Add button to submit user input
if st.button("Submit"):
    # Generate bot response
    bot_response = generate_response(user_input)
    # Display bot response
    st.text("Bot: " + bot_response)
