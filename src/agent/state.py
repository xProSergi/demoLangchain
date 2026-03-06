from typing import TypedDict, Optional, Any, List, Dict

class AgentState(TypedDict):
    """
    This state object is used to store the current question, tool selection (search or calculator), tool inputs and 
    outputs, the final generated answer, possible errors, the conversation history, thoughts and observations.
    """
    question: str
    selected_tool: Optional[str]
    tool_input: Optional[Any]
    tool_result: Optional[Any]
    final_answer: Optional[str]
    error: Optional[str]
    thoughts: List[str]
    observations: List[str]
    history: List[Dict[str, str]]
    iterations: int