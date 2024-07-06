# imports for langchain, streamlit
from langchain_openai import ChatOpenAI
from langchain.schema import(
    SystemMessage,
    HumanMessage,
    AIMessage
)

import streamlit as st
from streamlit_chat import message

st.set_page_config(
    page_title='Custom Chatbot with memory',
    page_icon='🖥️',
    initial_sidebar_state='collapsed'
)
st.subheader('Custom Chatbot with memory 💻')

chat = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.5)

# creating the messages (chat history) in the Streamlit session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
    # adding a default SystemMessage
    st.session_state.messages.insert(0, SystemMessage(content='You are an AI assistant.'))

# creating the sidebar
with st.sidebar:
    # streamlit text input widget for the system message (role)
    system_message = st.text_input(label='Chatbot role', placeholder='You are an AI assistant.')

    if system_message:
        # if system message already exists then remove it and insert new one
        if isinstance(st.session_state.messages[0], SystemMessage):
            st.session_state.messages.pop(0)
        
        st.session_state.messages.insert(0, SystemMessage(content=system_message))
    
    # debugging for system message
    st.write(st.session_state.messages[0])

# streamlit chat input widget for the user message
if user_prompt := st.chat_input("Say something"):
    # if the user entered a question
    st.session_state.messages.append(
        HumanMessage(content=user_prompt)
    )

    with st.spinner('Working on your request ...'):
        # creating the ChatGPT response
        response = chat.invoke(st.session_state.messages)

    # adding the response's content to the session state
    st.session_state.messages.append(
        AIMessage(content=response.content)
    )

# displaying the messages (chat history)
# not showing messages[0], as that is the system message 
for i, msg in enumerate(st.session_state.messages[1:]):
    if i % 2 == 0:
        message(msg.content, is_user=True, key=f'{i} + 👽') # user's question
    else:
        message(msg.content, is_user=False, key=f'{i} + 💻') # ChatGPT response

# run the app: streamlit run ./streamlit_app.py
