from typing import TypedDict, Optional, Any


class AgentState(TypedDict):

    question: str

    # Name of the tool selected
    selected_tool: Optional[str]

    # Input arguments passed to the selected tool
    tool_input: Optional[Any]

    # Result returned by the tool execution 
    tool_result: Optional[Any]

   
    final_answer: Optional[str]

   
    error: Optional[str]
