import streamlit as st
import openai
import time


# This is the initial message for ChatGPT
init_system_msg = '''###你是一个航空公司订票专员，你的任务是根据用户的输入获取下面“航班预订信息标准格式”中的信息，不要获取“航班预订信息标准格式”以外的任何信息。###
###如果信息获取不完整，请继续向用户提问，直到预订信息获取完整为止。###
###如果用户要更改信息，直接更改，不要问“航班预订信息标准格式”以外的任何信息。###
###获得完整的航班预订信息后，向用户确认航班预订信息标准格式内的全部信息，客户确认后感谢客户的预订并结束本次航班预订流程。###

[航班预订信息标准格式]
"""
- 【出发城市】：<出发城市>
- 【到达城市】：<到达城市>
- 【航班日期】：<航班日期>
- 【航空公司】：<航空公司>
- 【仓位等级】：<仓位等级>

"""

[可选仓位等级，等级从高到低排列]
"""
- 头等舱
- 商务舱
- 超级经济舱
- 经济舱
"""
'''

# Define function to generate bot response
def generate_response(user_input, init_system_msg=init_system_msg, history=[]):
    system_msg = {"role": "system", "content": init_system_msg}
    messages = [system_msg]
    
    if history:
        for conv in history:
            messages.append({"role": "user", "content": conv["user"]})
            messages.append({"role": "assistant", "content": conv["bot"]})
        
    messages.append({"role": "user", "content": user_input})
    
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
with st.form(key='input_form', clear_on_submit=True):
    user_input = st.text_input("请输入: ")
    submit = st.form_submit_button(label='提交', use_container_width=True)
    clear_history = st.form_submit_button("清空历史对话记录", use_container_width=True)

# Add button to submit user input
# if st.button("Submit", use_container_width=True):
if submit:
    # Generate bot response
    bot_response = generate_response(user_input, history=st.session_state.conversation_history)
    
    # Add user input and bot response to conversation history
    st.session_state.conversation_history.append({"user": user_input, "bot": bot_response})
    
    # Display conversation history in a form
    with st.form(key='output_form', clear_on_submit=True):
        for conv in st.session_state.conversation_history:
            conversation_container.markdown("**用户:** " + conv["user"])
            conversation_container.markdown("**订票AI:** " + conv["bot"])
            conversation_container.markdown("---")

# Add button to clear conversation history
if clear_history:
    st.session_state.conversation_history = []

st.write("对话次数: " + str(len(st.session_state.conversation_history)))
