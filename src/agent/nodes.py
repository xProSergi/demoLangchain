from agent.state import AgentState
from tools.search import search
from tools.calculator import calculate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import json

MAX_ITERATIONS = 5

def _build_react_history(state: AgentState) -> str:
    """
    Builds the explicit ReAct history.
    """
    history = ""
    for t, o in zip(state["thoughts"], state["observations"]):
        history += f"Thought: {t}\nObservation: {o}\n"
    return history.strip()

def decide_next_step(state: AgentState) -> dict:
    """
    Uses an LLM (Gemini 2.0 Flash) to decide the next ReAct step:
    - search
    - calculator
    - finish
    """
    if state["iterations"] >= MAX_ITERATIONS:
        state["final_answer"] = "I could not reach a confident answer within the allowed number of steps."
        return {"selected_tool": None}

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return {"error": "GOOGLE_API_KEY not set"}

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0,
        api_key=api_key,
    )

    react_history = _build_react_history(state)

    prompt = f"""
You are a ReAct agent.

Respond in strict JSON format ONLY:
{{
    "thought": "your reasoning here",
    "action": "one of [search, calculator, finish]",
    "action_input": "input for the action or leave empty if finish"
}}

Rules:
- Use calculator ONLY for math expressions
- Use search for factual or real-world knowledge
- Use finish ONLY when you can answer confidently

ReAct history:
{react_history}

User question:
{state["question"]}
""".strip()

    response = llm.invoke(prompt)
    text = response.content.strip()

  
    try:
        parsed = json.loads(text)
        thought = parsed.get("thought", "").strip()
        action = parsed.get("action", "").strip().lower()
        action_input = parsed.get("action_input", "").strip()
    except Exception:
        return {"error": "LLM returned invalid JSON format."}

   
    state["thoughts"].append(thought)
    state["iterations"] += 1

 
    if action == "finish":
        state["final_answer"] = action_input or "No answer provided"
        return {"selected_tool": None}

    return {
        "selected_tool": action,
        "tool_input": action_input,
    }

def run_tool(state: AgentState) -> dict:
    """
    Executes the selected tool.
    """
    tool = state.get("selected_tool")
    tool_input = state.get("tool_input")

    try:
        if tool == "search":
            result = search(tool_input)
        elif tool == "calculator":
            result = calculate(tool_input)
        else:
            return {"error": f"Unknown tool: {tool}"}

        observation = f"Result of {tool}: {result}"
        state["observations"].append(observation)

        return {
            "tool_result": result,
            "observations": state["observations"],
        }

    except Exception as e:
        return {"error": str(e)}

def generate_answer(state: AgentState) -> dict:
    
    full_history = ""
    for t, o in zip(state["thoughts"], state["observations"]):
        full_history += f"Thought: {t}\nObservation: {o}\n"

    final_answer = state.get("final_answer") or "No answer generated"
    full_history += f"Final Answer: {final_answer}"

    return {"final_answer": final_answer, "history": full_history.strip()}
