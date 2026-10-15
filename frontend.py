
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
    response = chatbot.invoke(
        {
            "messages": [
                HumanMessage(content=user_input)
            ]
        },
        config=CONFIG
    )

    # Extract the latest assistant response
    ai_message = response["messages"][-1].content

    # Store and display the assistant's response
    st.session_state["message_history"].append({
        "role": "assistant",
        "content": ai_message
    })

    with st.chat_message("assistant"):
        st.write(ai_message)