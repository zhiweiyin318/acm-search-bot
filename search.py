import json
from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, END
from langchain_core.globals import set_verbose
from langgraph.graph.message import add_messages
from agents.parser import search_parser
from agents.view import search_tool_view

set_verbose(True)

class SearchState(TypedDict):
    messages: Annotated[list, add_messages]


def main():
    search_workflow = StateGraph(SearchState)
    search_workflow.add_node("search_parser", search_parser)
    search_workflow.add_node("search_tool_view", search_tool_view)
    search_workflow.set_entry_point("search_parser")
    search_workflow.add_edge("search_parser", "search_tool_view")
    search_workflow.add_edge("search_tool_view", END)

    search = search_workflow.compile()

    print("I'm ACM Search Bot, you can ask me to get or list the resources on the managed cluster. \n"
          "(type 'bye' to exit)\n")
    while True:
        try:
            user_input = input("Request: ")
            if user_input.lower() == "bye":
                print("Goodbye!")
                break

            if not user_input:
                continue

            # Execute the workflow
            for step in search.stream({"messages": [user_input]}):
                for node, value in step.items():
                    if node == "search_tool_view":
                        print(f"Results: \n{value['resources']}\n")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Results: {json.dumps({'error': str(e)},indent=2,sort_keys=True)}\n")
if __name__ == "__main__":
    main()