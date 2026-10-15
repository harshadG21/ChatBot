
import os
from dotenv import load_dotenv

from langchain_openrouter import ChatOpenRouter
from langchain_core.messages import HumanMessage , SystemMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.memory import MemorySaver


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


# Create the graph using MessagesState
graph = StateGraph(MessagesState)

# Register the chatbot node
graph.add_node("chat_node", chat_node)

# Define graph flow
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

# Configure the checkpointer for conversation memory
checkpointer = MemorySaver()

# Compile the graph
chatbot = graph.compile(checkpointer=checkpointer)

