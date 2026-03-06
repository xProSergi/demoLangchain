from dotenv import load_dotenv
from agent.react_agent import SimpleReActAgent

if __name__ == "__main__":
    load_dotenv()
    
    agent = SimpleReActAgent()
    
    print("Test 1")
    result1 = agent.run("Which environment manager does the project use?", thread_id="conv_1")
    print(f"Answer: {result1}")
 