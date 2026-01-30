from agent.state import AgentState
from tools.search import search
from langchain_google_genai import ChatGoogleGenerativeAI
import os


def run_tool(state: AgentState) -> dict:
    
    try:
        result = search(state["question"])
        return {
            "selected_tool": "duckduckgo_search",
            "tool_input": state["question"],
            "tool_result": result,
        }
    except Exception as e:
        return {"error": str(e)}


def generate_answer(state: AgentState) -> dict:
 
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return {"error": "GOOGLE_API_KEY not set"}

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        api_key=api_key,
    )

    prompt = f"""
    Use the following information to answer the question clearly:

    {state['tool_result']}

    Question: {state['question']}

    Provide only the final answer, without explanations.
    """

    response = llm.invoke(prompt)

    return {"final_answer": response.content}
