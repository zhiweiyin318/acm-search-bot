from langchain_ollama import ChatOllama

def get_model():
    return  ChatOllama(
    model="llama3.2:latest",
    temperature=0.1,
    format="json",
)
