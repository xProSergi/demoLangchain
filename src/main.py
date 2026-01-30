from dotenv import load_dotenv
from agent.react_agent import SimpleReActAgent

if __name__ == "__main__":
    load_dotenv()  

    agent = SimpleReActAgent()
    agent.run("What is the capital of Austria?")
