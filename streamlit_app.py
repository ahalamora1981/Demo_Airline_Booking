import streamlit as st
import openai
import time


init_system_msg = '''###从用户输入中抽取信息：出发城市、到达城市、航班日期、航空公司、仓位等级###
###如有缺失的信息，填写<未知>，并在最后向用户询问所有缺失的信息###
### 回复格式如下###
"""
以下是您的航班信息：
- 【出发城市】：<出发城市>
- 【到达城市】：<到达城市>
- 【航班日期】：<航班日期>
- 【航空公司】：<航空公司>
- 【仓位等级】：<仓位等级>

麻烦您再告诉我<用逗号分割的所有缺失信息>，谢谢！
"""
'''

# Define function to generate bot response
def generate_response(user_input, init_system_msg, history):
    system_msg = {"role": "system", "content": system_msg}
    messages = [system_msg]
    
    for conv in history:
        messages.append({"role": "user", "content": conv["user"]})
        messages.append({"role": "assistant", "content": conv["bot"]})

    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages,
        temperature = 0
    )
    bot_response = response['choices'][0]['message']['content']
    return bot_response

# Initialize conversation history
if "conversation_history" not in st.session_state.keys():
    st.session_state.conversation_history = []

# Set page title
st.title("航空公司订票AI机器人")    
st.subheader("对话内容：")

# Add a conversation container
conversation_container = st.container()

# Add text input field
with st.form(key='my_form', clear_on_submit=True):
    user_input = st.text_input("请输入: ")
    submit = st.form_submit_button(label='提交', use_container_width=True)
    clear_history = st.form_submit_button("清空历史对话记录", use_container_width=True)

# Add button to submit user input
# if st.button("Submit", use_container_width=True):
if submit:
    # Generate bot response
    bot_response = generate_response(user_input, init_system_msg, st.session_state.conversation_history)
    
    # Add user input and bot response to conversation history
    st.session_state.conversation_history.append({"user": user_input, "bot": bot_response})
    
    # Display conversation history
    i = 0
    for conv in st.session_state.conversation_history:
        if i != 0:
            conversation_container.markdown("---")
        conversation_container.markdown("**用户：**" + conv["user"])
        conversation_container.markdown("**订票AI：**" + conv["bot"])
        i += 1

# Add button to clear conversation history
if clear_history:
    st.session_state.conversation_history = []
