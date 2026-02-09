import faiss
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"
HF_TOKEN = os.environ.get("HF_TOKEN")

client = InferenceClient(model=MODEL_NAME, token=HF_TOKEN)
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def load_documents(docs_path="docs"):
    texts, sources = [], []
    path = Path(docs_path)
    if not path.exists():
        path.mkdir(exist_ok=True)
    
    for file in path.glob("*"):
        if file.is_file():
            texts.append(file.read_text(encoding="utf-8"))
            sources.append(file.name)
    return texts, sources


def chunk_text(text, chunk_size=150, overlap=50):
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size - overlap)]

documents, sources = load_documents()
all_chunks, chunk_sources = [], []
for doc, source in zip(documents, sources):
    chunks = chunk_text(doc)
    all_chunks.extend(chunks)
    chunk_sources.extend([source] * len(chunks))

embeddings = embed_model.encode(all_chunks, normalize_embeddings=True)
index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(np.array(embeddings).astype('float32'))

question = "What environment manager does this project use?"
query_emb = embed_model.encode([question], normalize_embeddings=True)
scores, indices = index.search(np.array(query_emb).astype('float32'), k=2)

context = "\n\n".join([f"Source: {chunk_sources[i]}\n{all_chunks[i]}" for i in indices[0] if i != -1])

messages = [
    {
        "role": "system",
        "content": f"Answer the question using the context below. Always include the source filename in your answer.\n\nContext:\n{context}"
    },
    {"role": "user", "content": question}
]

try:
    response = client.chat_completion(
        messages=messages,
        max_tokens=250,
        temperature=0
    )
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Error: {e}")