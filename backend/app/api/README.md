# InsightFlow AI

### AI-Powered RAG-Based Data Analytics Platform

InsightFlow AI is an intelligent data analytics platform that allows users to upload CSV or Excel datasets and interact with their data using natural language.

The platform combines traditional Python-based analytics with Retrieval-Augmented Generation (RAG) and Large Language Models (LLMs) to provide accurate, contextual, and explainable insights.

---

## 🚀 Features

- Upload CSV and Excel datasets
- Automatic dataset profiling
- Dataset quality analysis
- Missing-value detection
- Numerical statistics
- Natural-language data queries
- Verified analytics using Pandas
- Retrieval-Augmented Generation (RAG)
- Semantic search using FAISS
- Local sentence-transformer embeddings
- LLM-powered explanations
- Interactive analytics dashboard
- Missing-value visualization
- Column-level dataset profiling
- Responsive React interface

---

## 🧠 Architecture

```text
User
 │
 ▼
React Frontend
 │
 ▼
FastAPI Backend
 │
 ├── Dataset Upload
 │
 ├── Data Profiler
 │
 ├── Analytics Engine
 │      └── Pandas
 │
 ├── RAG Pipeline
 │      ├── Sentence Transformers
 │      └── FAISS
 │
 └── LLM Service
        └── Groq API