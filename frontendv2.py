
import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage

# Configuration required by the LangGraph checkpointer
CONFIG = {
    "configurable": {
        "thread_id": "thread-1"
    }
}

# Initialize conversation history once per Streamlit session
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

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
                                HumanMessage(content='what is the recipe to make pasta ')
                            ]
                        },
                        config=CONFIG,
                        stream_mode="messages"
            )
        )
    st.session_state['message_history'.apend({'role':'assistant','content':ai_message})]