# Basic ReAct Agent Demo

## Overview
This project demonstrates a **basic ReAct agent** implemented manually.  
The agent uses **DuckDuckGo** to retrieve information from the web and **Gemini 2.5 Flash LLM** to process the search results and generate answers.  

The project is structured with separate folders for agents and tools.
Environment management is handled with **UV**.

---

## Features
- Basic ReAct architecture 
- DuckDuckGo search integration for information retrieval  
- Gemini 2.5 Flash LLM for generating final answers  
 - Reproducible environment with UV  

---

## Environment Variables

Create a .env file in the root of the project with:
```python
GOOGLE_API_KEY=your_api_key
```

## Roadmap

### Phase 1
 - Basic ReAct agent
 - DuckDuckGo tool integrated
 - Gemini 2.5 Flash LLM to generate answers

### Phase 2

- Add checkpointer to store question/answer history
- Handle errors related to DuckDuckGo
- Add aditional tools (Wikipedia search, calculator, local dataset queries)

### Phase 3

- Tool selection logic (agent decides which tool to use based on the type of question or task)