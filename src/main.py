from dotenv import load_dotenv
from agent.react_agent import SimpleReActAgent

if __name__ == "__main__":
    load_dotenv()
    
    agent = SimpleReActAgent()
    
    print("Test 1")
    result1 = agent.run("What is the capital of Austria?", thread_id="conv_1")
    print(f"Answer: {result1}")
    
    print("\nTest 2")
    result2 = agent.run("What is the population of its capital?", thread_id="conv_1")
    print(f"Answer: {result2}")
    
    print("\nTest 3" )
    result3 = agent.run("What is the capital of Spain?", thread_id="conv_2")
    print(f"Answer: {result3}")
    
    print("\n Test 4")
    result4 = agent.run("What is 23*7?", thread_id="conv_2")
    print(f"Answer: {result4}")
    
    