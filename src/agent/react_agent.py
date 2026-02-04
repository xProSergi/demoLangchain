from agent.graph import build_graph

class SimpleReActAgent:

    def __init__(self) -> None:
        self.app = build_graph()
    
    def run(self, question: str, thread_id: str = "default") -> str:
        """
        Runs the agent on a given question. Creates the initial agent state, invokes the execution graph and returns
        the final answer or an error message.
        Args:
            question: The user question or prompt to process.
            thread_id: Identifier for the execution thread
        """
    
     
        initial_state = {
            "question": question,
            "selected_tool": None,
            "tool_input": None,
            "tool_result": None,
            "final_answer": None,
            "error": None,
            "thoughts": [],
            "observations": [],
            "history": [],
            "iterations": 0,
        }
        
        try:
            result = self.app.invoke(
                initial_state,
                config={"configurable": {"thread_id": thread_id}},
            )
            
            error = result.get("error")
            if error:
                return f"Error: {error}"
            
            return result.get("final_answer", "No answer generated")
            
        except Exception as e:
            return f"Agent execution error: {str(e)}"