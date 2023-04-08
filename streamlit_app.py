import streamlit as st

# Set page title
st.title("Chat with Bot")

# Define function to generate bot response
def generate_response(user_input):
    # Do some processing here to generate bot response
    bot_response = "I'm sorry, I don't understand. Please try again."
    return bot_response

# Initialize conversation history
if not st.session_state.conversation_history:
    st.session_state.conversation_history = []

# Add text input field
user_input = st.text_input("You: ")

# Add button to submit user input
if st.button("Submit"):
    st.write(st.session_state.conversation_history)
    # Generate bot response
    bot_response = generate_response(user_input)
    # Add user input and bot response to conversation history
    st.session_state.conversation_history.append(("You: " + user_input, "Bot: " + bot_response))
    # Display conversation history
    for user, bot in st.session_state.conversation_history:
        st.text(user)
        st.text(bot)

# Add button to clear conversation history
if st.button("Clear history"):
    conversation_history.clear()
