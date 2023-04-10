import time
import streamlit as st
import openai



# This is the initial message for ChatGPT
INIT_SYSTEM_MSG = '''### 你是一个航空公司订票专员，你的任务是根据用户的输入获取下面“航班预订信息标准格式”中的预订信息，不准获取“航班预订信息标准格式”以外的其他任何信息。 ###
### 如果“航班预订信息标准格式”内的预订信息获取不完整，请继续向用户提问，直到预订信息获取完整为止。 ###
### 在获取预订信息的过程中，只需要获取“航班预订信息标准格式”内的预订信息，不要和用户重复确认已经获取的预订信息。 ###
### 获得完整的航班预订信息后，向用户确认航班预订信息标准格式内的全部预订信息，客户确认后感谢客户的预订并结束本次航班预订流程。 ###

### 航班预订信息标准格式 ###
- 【出发城市】：
- 【到达城市】：
- 【航班日期】：
- 【航空公司】：
- 【仓位等级】：

### 可选仓位等级，等级从高到低排列 ###
- 头等舱
- 商务舱
- 超级经济舱
- 经济舱

### 禁止提问的内容 ###
- 单程机票还是往返机票
- 出发的机场
- 到达的机场
'''

# Define function to generate bot response
def generate_response(user_msg, history, init_system_msg=INIT_SYSTEM_MSG):
    """
    Use system message and user input to generate ChatGPT response.
    """
    system_msg = {"role": "system", "content": init_system_msg}
    messages = [system_msg]

    if history:
        for msg in history:
            messages.append({"role": "user", "content": msg["user"]})
            messages.append({"role": "assistant", "content": msg["bot"]})

    messages.append({"role": "user", "content": user_msg})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0
    )
    response = response['choices'][0]['message']['content']
    return response


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
if submit:
    # Generate bot response
    bot_response = generate_response(
        user_input, history=st.session_state.conversation_history)

    # Add user input and bot response to conversation history
    st.session_state.conversation_history.append(
        {"user": user_input, "bot": bot_response})

    # Display conversation history in a form
    with st.form(key='output_form', clear_on_submit=True):
        for conv in st.session_state.conversation_history:
            conversation_container.markdown("**用户:**   " + conv["user"])
            conversation_container.markdown("**订票AI:**   " + conv["bot"])
            conversation_container.markdown("---")

# Add button to clear conversation history
if clear_history:
    st.session_state.conversation_history = []

# Display the number of current conversation rounds
st.write("对话次数: " + str(len(st.session_state.conversation_history)))
