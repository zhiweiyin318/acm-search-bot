from langchain_core.messages import SystemMessage,HumanMessage

from model import get_model
from state import SearchState

system_message = """You are a kubernetes expert. 
    The user will identify the resources in which namespace on which cluster he wants to get or list. 
    Your task is to retrieve the resource, name, namespace, cluster from the user's message, and output a JSON string.
    The output should strictly be in JSON without extra fields, comments, or non-JSON text.
    The output JSON format is {"resource": "...", "name": "...", "namespace": "...", "cluster": "..."}.
    The 'resource' and 'cluster' should not be empty.
    The 'resource' should use the plural form.
    The 'namespace' is '' if the 'resource' is namespace or namespaces.
    The 'name' and 'namespace' could be empty.
    Set "" directly in the output if the field is not found in the user's message.
    Use lowercase for all keys in the output.
    """

def search_parser(state: SearchState):
    model = get_model()
    result = model.invoke(
        [
            SystemMessage(content=system_message),
            HumanMessage(content=state["messages"][-1].content)
        ]
    )
    print(f"Requested resource: {result.content}")
    return {"messages": [result]}
