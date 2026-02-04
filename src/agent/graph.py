from typing import Literal
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from agent.state import AgentState
from agent.nodes import decide_next_step, run_tool, generate_answer

def route_after_decide(state: AgentState) -> Literal["run_tool", "generate_answer", "__end__"]:
    if state.get("final_answer"):
        return "generate_answer"
    if state.get("selected_tool"):
        return "run_tool"
    return END

def route_after_tool(state: AgentState) -> Literal["decide", "__end__"]:
    if state.get("error"):
        return END
    return "decide"

def route_after_generate(state: AgentState) -> Literal["__end__"]:
    return END

def build_graph():
    graph = StateGraph(AgentState)

    
    graph.add_node("decide", decide_next_step)
    graph.add_node("run_tool", run_tool)
    graph.add_node("generate_answer", generate_answer)

 
    graph.set_entry_point("decide")

 
    graph.add_conditional_edges(
        "decide",
        route_after_decide,
        {
            "run_tool": "run_tool",
            "generate_answer": "generate_answer",
            END: END,
        },
    )

    graph.add_conditional_edges(
        "run_tool",
        route_after_tool,
        {
            "decide": "decide",
            END: END,
        },
    )

    graph.add_conditional_edges(
        "generate_answer",
        route_after_generate,
        {
            END: END,
        },
    )

    memory = MemorySaver()
    return graph.compile(checkpointer=memory)
