import faiss
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()

MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"
HF_TOKEN = os.environ.get("HF_TOKEN")
PROMPT_VERSION = "v1.0"

TOP_K = 5
SIMILARITY_THRESHOLD = 0.30       
ANSWER_SIMILARITY_THRESHOLD = 0.25 

client = InferenceClient(model=MODEL_NAME, token=HF_TOKEN)
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def load_documents(docs_path="docs"):
    texts, sources = [], []
    path = Path(docs_path)

    if not path.exists():
        path.mkdir(exist_ok=True)

    for file in path.glob("*"):
        content = file.read_text(encoding="utf-8")
        texts.append(content)
        sources.append(file.name)

    return texts, sources

def chunk_text(text, chunk_size=120, overlap=40):
    words = text.split()
    return [
        " ".join(words[i:i + chunk_size])
        for i in range(0, len(words), chunk_size - overlap)
    ]

documents, sources = load_documents()

if not documents:
    print("No documents found in docs folder.")
    exit()

all_chunks = []
chunk_sources = []

for doc, source in zip(documents, sources):
    chunks = chunk_text(doc)
    all_chunks.extend(chunks)
    chunk_sources.extend([source] * len(chunks))

embeddings = embed_model.encode(all_chunks, normalize_embeddings=True)
index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(np.array(embeddings).astype("float32"))


def build_system_prompt(context: str, prompt_version: str) -> str:
    return f"""
[Prompt Version: {prompt_version}]

You are a RAG + CAG assistant.
Use ONLY the provided context to answer.
Do NOT invent information.
If the answer is not contained in the context, say so clearly.
Always include the source filename in your answer.

Context:
{context}
""".strip()


def build_messages(context: str, question: str, prompt_version: str):
    system_prompt = build_system_prompt(context, prompt_version)

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question},
    ]


@lru_cache(maxsize=128)
def answer_question(question: str, prompt_version: str = PROMPT_VERSION) -> str:

    query_emb = embed_model.encode([question], normalize_embeddings=True)
    scores, indices = index.search(
        np.array(query_emb).astype("float32"),
        k=TOP_K
    )

    context_chunks = [
        f"Source: {chunk_sources[i]}\n{all_chunks[i]}"
        for score, i in zip(scores[0], indices[0])
        if i != -1 and score >= SIMILARITY_THRESHOLD
    ]

    if not context_chunks:
        return "No relevant information found in the documents."

    for c in context_chunks:
        print(c, "\n---\n")

    context = "\n\n".join(context_chunks)

    messages = build_messages(context, question, prompt_version)

    
    response = client.chat_completion(
        messages=messages,
        max_tokens=500,
        temperature=0.0  
    )

    answer = response.choices[0].message.content

    
    answer_emb = embed_model.encode([answer], normalize_embeddings=True)
    chunk_embeddings = embed_model.encode(
        [all_chunks[i] for score, i in zip(scores[0], indices[0])
         if i != -1 and score >= SIMILARITY_THRESHOLD],
        normalize_embeddings=True
    )
    similarities = np.dot(answer_emb, chunk_embeddings.T)[0]
    similarity = float(np.max(similarities))

  
    return f"Similarity Score: {similarity:.3f}\n\n{answer}"


if __name__ == "__main__":
   while True:
        question = input("Question: ").strip()
        if not question or question.lower() in ['exit', 'salir']:
            break
        try:
            print(answer_question(question))
        except Exception as e:
            print(f"Error: {e}")
