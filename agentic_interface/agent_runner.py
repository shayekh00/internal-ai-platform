# agentic_interface/agent_runner.py

from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from tools.init_agent import init_agent
import os

def main():
    llm = ChatOpenAI(temperature=0, model="gpt-4", openai_api_key=os.getenv("OPENAI_API_KEY"))

    tools = [init_agent]

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    print("\U0001f9e0 SixtAI Dev Agent Ready. Type instructions (or 'exit'):")

    while True:
        user_input = input(">> ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = agent.run(user_input)
        print(response)

if __name__ == "__main__":
    main()
