from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.nodes import run_tool, generate_answer


def build_graph():
    graph = StateGraph(AgentState)

  
    graph.add_node("run_tool", run_tool)
    graph.add_node("generate_answer", generate_answer)

    
    graph.set_entry_point("run_tool")
    graph.add_edge("run_tool", "generate_answer")
    graph.add_edge("generate_answer", END)

    return graph.compile()
