from langchain_core.messages import SystemMessage

from agents.acm_tools import search_tools
from model import get_model
from state import SearchState

system_message = SystemMessage(
        """You are a helpful AI Assistant who calls the right function to complete the task
        Carefully identify the final parameters to be used to call the function. Pay attention to each message in the conversation.
        """
    )

def get_acm_search_bot(state: SearchState):
    model = get_model().bind_tools(search_tools)
    messages = [system_message] + state["messages"]

    return {"messages": [model.invoke(messages)]}
