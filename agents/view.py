import json

from agents.acm_tools import get_resources
from state import SearchState


def search_tool_view(state: SearchState):
    last_message = state["messages"][-1].content
    try:
        data_list = json.loads(last_message)
    except json.JSONDecodeError as e :
        raise ValueError("The input is not a json string. ",str(e))

    result = get_resources(data_list["resource"], data_list["name"],data_list["namespace"],data_list["cluster"])
  #  print(f"Result: {result}")
    return {"resources": result}
