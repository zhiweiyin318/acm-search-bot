from typing import Annotated
from typing_extensions import TypedDict,List
from langgraph.graph.message import add_messages

class SearchState(TypedDict):
    messages:  Annotated[list, add_messages]
    resources: List[dict]