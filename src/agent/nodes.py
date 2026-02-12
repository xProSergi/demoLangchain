from agent.state import AgentState
from tools.search import search
from tools.calculator import calculate
from tools.rag import search_docs
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import json
import re

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
    - docs
    - finish
    """
    if state["iterations"] >= MAX_ITERATIONS:
        return {"final_answer": "I could not reach a confident answer within the allowed number of steps."}

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return {"error": "GOOGLE_API_KEY not set"}

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        api_key=api_key,
    )

    react_history = _build_react_history(state)

    prompt = f"""You are a ReAct agent. You must respond with ONLY a JSON object, nothing else.

{{
    "thought": "your reasoning here",
    "action": "one of [search, calculator, docs, finish]",
    "action_input": "input for the action or leave empty if finish"
}}

Rules:
- Use calculator ONLY for math expressions
- Use search for factual or real-world knowledge
- Use docs for internal project documentation
- Use finish ONLY when you can answer confidently

ReAct history:
{react_history}

User question:
{state["question"]}

Respond with ONLY the JSON object, no explanations before or after.""".strip()

    response = llm.invoke(prompt)
    text = response.content.strip()
    
  
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        text = json_match.group()
  
    try:
        parsed = json.loads(text)
        thought = parsed.get("thought", "").strip()
        action = parsed.get("action", "").strip().lower()
        action_input = parsed.get("action_input", "").strip()
    except Exception as e:
        print(f"Error parsing JSON. LLM response was:\n{response.content}")
        return {"error": f"LLM returned invalid JSON format: {str(e)}"}

  
    new_thoughts = state["thoughts"] + [thought]
    new_iterations = state["iterations"] + 1
 
    if action == "finish":
        return {
            "thoughts": new_thoughts,
            "iterations": new_iterations,
            "final_answer": action_input or "No answer provided"
        }

    return {
        "thoughts": new_thoughts,
        "iterations": new_iterations,
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
        elif tool == "docs":
            result = search_docs(tool_input)
        else:
            return {"error": f"Unknown tool: {tool}"}

        observation = f"Result of {tool}: {result}"
        new_observations = state["observations"] + [observation]

        return {
            "tool_result": result,
            "observations": new_observations,
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