import streamlit as st
import openai

# Set page title
st.title("Chat with Bot")

# Define function to generate bot response
def generate_response(user_input, history):
    if history:
        system_msg = history[-1][1].strip("Bot: ")
    else:
        system_msg = '''### 从用户输入中抽取的发出城市、到达城市、航班日期、航空公司、仓位等级，并回复。如有缺失的信息，请向对方发问；如信息完整，就不要发问。 ###

### 格式（对于缺失的信息，填写<未知>）###

"""
以下是您的航班信息：
【发出城市】：<发出城市>
【到达城市】：<到达城市>
【航班日期】：<航班日期>
【航空公司】：<航空公司>
【仓位等级】：<仓位等级>

请您再告诉我<用顿号分割缺失信息的名称>，谢谢！
"""

以下是您的航班信息：'''
    print("System Msg: ", system_msg)
    
    openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": "Where was it played?"}
        ],
        temperature = 0
    )
    bot_response = "You are great!"
    return bot_response

# Initialize conversation history
if not st.session_state.conversation_history:
    st.session_state.conversation_history = []

# Add text input field
user_input = st.text_input("You: ")

# Add button to submit user input
if st.button("Submit"):
    # Generate bot response
    bot_response = generate_response(user_input, st.session_state.conversation_history)
    # Add user input and bot response to conversation history
    st.session_state.conversation_history.append(("You: " + user_input, "Bot: " + bot_response))
    # Display conversation history
    for user, bot in st.session_state.conversation_history:
        st.text(user)
        st.text(bot)

# Add button to clear conversation history
if st.button("Clear history"):
    st.session_state.conversation_history.clear()
