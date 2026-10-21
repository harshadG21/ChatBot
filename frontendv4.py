
import streamlit as st
from backendv2 import chatbot,retrieve_all_threads
from langchain_core.messages import HumanMessage
import uuid

#utitlity functions

def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    config = {
        "configurable": {
            "thread_id": str(thread_id)
        }
    }

    # Retrieve the saved state for this conversation
    state = chatbot.get_state(config=config)

    # Check whether a usable state exists
    if not state or not state.values:
        return []

    return state.values.get("messages", [])

#session setup
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()

add_thread(st.session_state['thread_id'])

# Configuration required by the LangGraph checkpointer
CONFIG = {
        "configurable": {"thread_id": st.session_state["thread_id"]},
        "metadata": {
            "thread_id": st.session_state["thread_id"]
        },
        "run_name": "chat_turn",
    }



# sidebar ui 

st.sidebar.title('LangGraph chatbot')

if st.sidebar.button('New Conversation'):
    reset_chat()

st.sidebar.header('My Conversations')

for thread_id in st.session_state['chat_threads']:
   if st.sidebar.button(str(thread_id)):
       st.session_state['thread_id'] = thread_id
       messages = load_conversation(thread_id)

       temp_messages=[]

       for msg in messages:
           if isinstance(msg,HumanMessage):
               role='user'
           else:
               role='assistant'
           temp_messages.append({'role':role,'content':msg.content})

       st.session_state['message_history'] = temp_messages

# Display previous messages
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Get input from the user
user_input = st.chat_input("Type here")

if user_input:

    # Display and store the user's message
    st.session_state["message_history"].append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    # Invoke LangGraph with the required thread configuration
    

    with st.chat_message("assistant"):

        ai_message=st.write_stream(
            message_chunk.content for message_chunk,metadata in chatbot.stream({
                            "messages": [
                                HumanMessage(content=user_input)
                            ]
                        },
                        config=CONFIG,
                        stream_mode="messages"
            )
        )
    st.session_state['message_history'].append({
        'role':'assistant',
        'content':ai_message
        })