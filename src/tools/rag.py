import os
from pathlib import Path

DOCS_CACHE = {}

def load_docs(docs_folder="../docs"):
   
    if DOCS_CACHE:
        return DOCS_CACHE
    
    docs_path = Path(docs_folder)
    if not docs_path.exists():
        return {}
    
    for file in docs_path.glob("*.md"):
        DOCS_CACHE[file.name] = file.read_text()
    
    for file in docs_path.glob("*.txt"):
        DOCS_CACHE[file.name] = file.read_text()
    
    return DOCS_CACHE

def search_docs(query: str) -> str:
  
    docs = load_docs()
    
    if not docs:
        return "No available documentation disponible."
    

    query_words = query.lower().split()
    results = []
    
    for filename, content in docs.items():
        content_lower = content.lower()
        score = sum(1 for word in query_words if word in content_lower)
        
        if score > 0:
        
            lines = content.split('\n')
            relevant_lines = []
            for line in lines:
                if any(word in line.lower() for word in query_words):
                    relevant_lines.append(line)
                    if len(relevant_lines) >= 5:
                        break
            
            if relevant_lines:
                results.append({
                    'file': filename,
                    'score': score,
                    'snippet': '\n'.join(relevant_lines)
                })
    
    if not results:
        return "I did not find relevant information"
    

    results.sort(key=lambda x: x['score'], reverse=True)
    

    output = []
    for r in results[:2]:
        output.append(f"[{r['file']}]\n{r['snippet']}")
    
    return '\n\n---\n\n'.join(output)