
import os
from dotenv import load_dotenv

from langchain_openrouter import ChatOpenRouter
from langchain_core.messages import HumanMessage , SystemMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3


# Load environment variables from .env
load_dotenv()

CONFIG = {
    "configurable": {
        "thread_id": "thread-1"
    }
}

# Initialize the OpenRouter language model
llm = ChatOpenRouter(
    model="deepseek/deepseek-chat",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


# Define the chatbot node
def chat_node(state: MessagesState):
    # Get conversation messages from the graph state
    messages = state["messages"]

    # Add system instructions before the conversation
    response = llm.invoke(
        [
            SystemMessage(
                content="You are a helpful AI chatbot. "
                        "Answer clearly and politely."
            ),
            *messages
        ]
    )

    # Return the AI response to LangGraph
    return {"messages": [response]}


conn = sqlite3.connect(database='chatbot.db',check_same_thread=False)

# Create the graph using MessagesState
graph = StateGraph(MessagesState)

# Register the chatbot node
graph.add_node("chat_node", chat_node)

# Define graph flow
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)


# Configure the checkpointer for conversation memory
checkpointer = SqliteSaver(conn)

# Compile the graph
chatbot = graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)


