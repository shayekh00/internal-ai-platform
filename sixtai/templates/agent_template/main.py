# from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

def run_agent(prompt: str) -> str:
    llm = ChatOpenAI(temperature=0)
    msg = HumanMessage(content=prompt)
    return llm([msg]).content



if __name__ == "__main__":
    response = run_agent("Hello!")
    print("Agent response:", response)
