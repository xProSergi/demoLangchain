from agent.graph import build_graph


class SimpleReActAgent:
    
    def __init__(self):
        self.app = build_graph()

    def run(self, question: str) -> str:
        initial_state = {
            "question": question,
            "selected_tool": None,
            "tool_input": None,
            "tool_result": None,
            "final_answer": None,
            "error": None,
        }

        result = self.app.invoke(initial_state)

        if result.get("error"):
            raise RuntimeError(result["error"])

        print("Answer:", result["final_answer"])
        return result["final_answer"]
