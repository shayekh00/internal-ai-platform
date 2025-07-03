# main.py
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

def run_agent(prompt: str) -> str:
    llm = ChatOpenAI(temperature=0.2)
    message = HumanMessage(content=prompt)
    return llm([message]).content
