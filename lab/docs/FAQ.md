# Frequently Asked Questions (FAQ)

## General Project Questions

**Q1: What is the purpose of this project?**  
A1: This project demonstrates a basic Retrieval-Augmented Generation (RAG) system using Sentence Transformers and FAISS. It allows users to query project documentation and get answers based on relevant chunks of text.

**Q2: Which files are included in the lab folder?**  
A2: The lab folder includes the main RAG script (`rag.py`) and a `docs/` folder containing `.md` and `.txt` files that are used as the knowledge base.

**Q3: How is the project structured?**  
A3: 
- `rag.py` → Main RAG script  
- `docs/` → Folder containing documentation files  
- `README.md` → Overview of the project  
- `INSTALL.md` → Installation guide  
- `USAGE.md` → Usage examples  
- `ARCHITECTURE.md` → Project architecture description  
- `ENV_VARS.md` → Environment variables needed  
- `FAQ.md` → Frequently asked questions  
- `EXAMPLES.txt` → Example queries  

---

## RAG & Retrieval Questions

**Q4: What is Retrieval-Augmented Generation (RAG)?**  
A4: RAG is a system that combines information retrieval with generative models. Instead of relying only on the LLM's memory, it retrieves relevant chunks from a knowledge base to generate precise answers.

**Q5: How are documents processed in the RAG system?**  
A5: Documents are read from the `docs/` folder, split into chunks of approximately 120 words with 25 words overlap, embedded using a Sentence Transformer, and stored in a FAISS index for semantic search.

**Q6: Which model is used to create embeddings?**  
A6: The project uses the `all-MiniLM-L6-v2` model from Hugging Face's Sentence Transformers. This is an encoder model that creates 384-dimensional embeddings suitable for semantic similarity tasks.

**Q7: How does FAISS help in the project?**  
A7: FAISS provides a fast vector similarity search. After encoding all chunks, FAISS allows the system to retrieve the top-k most similar chunks to a given query using cosine similarity.

**Q8: How is similarity measured?**  
A8: Similarity between the query and document chunks is measured using cosine similarity. Embeddings are normalized so that the inner product in FAISS directly reflects cosine similarity.

**Q9: What happens if multiple chunks are equally relevant?**  
A9: FAISS will return the top-k closest chunks. In case of duplicates or highly similar content, the same chunk might appear multiple times. This can be improved by filtering duplicates in post-processing.

---

## Chunking & Preprocessing Questions

**Q10: What is chunking and why is it important?**  
A10: Chunking divides a large document into smaller parts (chunks) to feed them into the embedding model. This ensures the LLM can process information efficiently and retrieve relevant context without exceeding token limits.

**Q11: What chunk size is used?**  
A11: Chunks are set to 120 words with an overlap of 25 words between chunks to maintain context across boundaries.

**Q12: Can we use RecursiveCharacterTextSplitter?**  
A12: Yes, for production-level systems or very long documents, RecursiveCharacterTextSplitter (like in LangChain) is recommended. It splits text by characters instead of words and preserves semantic boundaries.

**Q13: How is Markdown handled?**  
A13: Markdown formatting (like `#`, `**`, `---`) is currently kept in chunks. Optional cleaning can remove these symbols for a cleaner prompt for the LLM.

---

## Query & LLM Questions

**Q14: How does the RAG system answer questions?**  
A14: When a query is received, the system:  
1. Converts the query into an embedding  
2. Searches the FAISS index for the most relevant chunks  
3. Combines retrieved chunks into a prompt  
4. Sends the prompt to a generative LLM to produce the answer

**Q15: Which LLMs are compatible?**  
A15: Any LLM that can take a text prompt. Examples include OpenAI GPT-3.5, GPT-4, Hugging Face models, and local LLaMA derivatives.

**Q16: Can this system answer any question?**  
A16: The system answers questions only based on the documents in the `docs/` folder. It cannot generate answers outside its knowledge base unless connected to an external LLM with internet access.

**Q17: Can multiple queries be processed simultaneously?**  
A17: Currently, the script handles one query at a time, but it can be extended to batch queries or build a web interface for interactive querying.

---

## Technical Questions

**Q18: Are positional embeddings used?**  
A18: No. The project ignores positional embeddings, as recommended. Only sentence embeddings are used.

**Q19: Is the CLS token used?**  
A19: No. Only the embeddings of the chunk as a whole are used. CLS tokens are ignored.

**Q20: How can I add more documents to the RAG system?**  
A20: Simply place additional `.md` or `.txt` files into the `docs/` folder. They will automatically be included in the next run of the script.

**Q21: How can I update embeddings after adding new documents?**  
A21: Re-run the script. For larger projects, consider caching embeddings to avoid recomputation.

**Q22: Can PDFs be used?**  
A22: Yes, by extracting text using libraries like `PyMuPDF` or `pdfplumber` and saving them as `.txt` or `.md` files.

---

## Example Queries

**Q23: What are some example queries I can try?**  
A23:  
- "Which environment manager does the project use?"  
- "How is the RAG system implemented?"  
- "Which Sentence Transformer model is used?"  
- "How are documents chunked?"  
- "Which LLMs are compatible with this project?"  

**Q24: How can I test the system?**  
A24: Run `uv run python rag.py` and check the printed retrieved chunks and the prompt. You can then feed the prompt into an LLM for answers.

---


