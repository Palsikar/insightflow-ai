# 🤖 InsightFlow AI

An intelligent data analytics platform that combines **RAG, LLMs, and verified statistical analysis** to help users upload datasets, explore data, and ask natural-language questions.

## 🌐 Live Application

**Website**: [https://insightflow-ai-wheat.vercel.app/](https://insightflow-ai-wheat.vercel.app/)

## 📸 Project Screenshots

| Dataset Upload | AI Data Analysis |
|---|---|
|<img width="1715" height="821" alt="image" src="https://github.com/user-attachments/assets/79e091bc-f22c-4d10-9bcc-9cfcbcf1d528" />|<img width="1731" height="870" alt="image" src="https://github.com/user-attachments/assets/f4e28893-5f9a-45f4-b6ac-98762ac4fe64" />|
| Upload CSV/Excel datasets and generate an automatic profile | Ask natural-language questions and receive AI-powered insights |

| Data Visualization | Dataset Profile |
|---|---|
| <img width="1717" height="867" alt="image" src="https://github.com/user-attachments/assets/1470ae9f-484e-4937-89be-9cb93c696623" />|<img width="1716" height="892" alt="image" src="https://github.com/user-attachments/assets/45944971-3c06-47e5-9dae-646ef1097a9d" />|
| Interactive charts for exploring dataset statistics | Detailed dataset information and column-level statistics |


## 🧠 Project Description

InsightFlow AI is an AI-powered data analytics platform designed to make dataset exploration easier through natural-language interaction.

Users can upload CSV or Excel datasets, automatically generate dataset profiles, visualize important statistics, and ask questions about their data using an intelligent AI assistant.

The platform combines **Retrieval-Augmented Generation (RAG)** with programmatically verified analytics. Statistical calculations are performed using Python and Pandas, while the retrieved dataset context and verified results are provided to an LLM to generate clear and meaningful responses.

This project combines:

- An AI-powered data analytics assistant
- Retrieval-Augmented Generation (RAG)
- Verified statistical and numerical analysis
- Automated dataset profiling
- Persistent cloud dataset storage
- Interactive and responsive frontend

## 🔄 How It Works

1. Upload a CSV or Excel dataset.
2. The backend automatically profiles the dataset.
3. Dataset information is converted into searchable documents.
4. RAG retrieves the most relevant information based on the user's question.
5. Python/Pandas performs verified numerical analysis when required.
6. The retrieved context and verified results are passed to the LLM.
7. InsightFlow AI generates a concise natural-language response.

## 🚀 Tech Stack

- **Frontend**: React, Vite, Tailwind CSS, Recharts
- **Backend**: Python, FastAPI
- **AI/LLM**: Groq, `openai/gpt-oss-120b`
- **RAG**: TF-IDF-based document retrieval
- **Data Analysis**: Pandas, NumPy
- **Data Storage**: Vercel Blob
- **API Server**: Uvicorn
- **Deployment**: Vercel
- **Version Control**: Git, GitHub

## ✨ Features

- Upload CSV and Excel datasets
- Automatic dataset profiling
- Dataset row and column analysis
- Missing-value analysis
- Numerical statistics
- Average, minimum, and maximum calculations
- Fault analysis for sensor datasets
- Correlation analysis
- Natural-language data queries
- RAG-based contextual retrieval
- LLM-generated explanations
- Verified analytics results to reduce numerical hallucinations
- Persistent dataset storage using Vercel Blob
- Interactive charts and data visualizations
- Responsive web interface

## 🧩 Architecture

```text
User
  │
  ▼
React + Vite Frontend
  │
  ▼
FastAPI Backend
  │
  ├── Dataset Upload
  │      │
  │      ▼
  │   Vercel Blob
  │
  ├── Dataset Profiler
  │
  ├── Analytics Engine
  │      │
  │      └── Pandas / NumPy
  │
  └── RAG Pipeline
         │
         ├── TF-IDF Retrieval
         │
         ▼
       Groq LLM
         │
         ▼
   Natural-Language Answer
```

## 📊 Data Analytics

InsightFlow AI performs verified calculations using the uploaded dataset before generating an AI response.

Supported analytical operations include:

- Dataset size analysis
- Column identification
- Missing-value analysis
- Mean/average calculations
- Minimum and maximum values
- Fault analysis
- Correlation analysis
- Numerical column statistics

This approach allows the system to use the LLM primarily for **interpretation and explanation**, while numerical results are generated programmatically.

## 🔍 Retrieval-Augmented Generation

InsightFlow AI uses a lightweight **TF-IDF-based retrieval system** to identify relevant information from the dataset profile.

The RAG pipeline:

```text
User Question
      ↓
TF-IDF Vectorization
      ↓
Similarity Matching
      ↓
Relevant Dataset Information
      ↓
Verified Analytics
      ↓
LLM
      ↓
Final Answer
```

This provides the LLM with relevant dataset context instead of relying only on its general knowledge.

## 🛠️ Setup & Installation

### Clone the Repository

```bash
git clone https://github.com/Palsikar/insightflow-ai.git
cd insightflow-ai
```

### Backend Setup

```bash
cd backend
python -m venv venv
```

Activate the virtual environment on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file inside the `backend` directory:

```env
GROQ_API_KEY=your_groq_api_key
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend will run at:

```text
http://localhost:5173
```

## ☁️ Deployment

The application is deployed using **Vercel**.

The frontend and FastAPI backend are connected through Vercel routing, while uploaded datasets are stored using **Vercel Blob** for persistent cloud storage.

The Groq API key is configured as a server-side environment variable and is not included in the repository.

## 🔐 Security

- API keys are stored using environment variables.
- `.env` files are excluded from Git.
- Uploaded datasets are stored separately using Vercel Blob.
- The LLM is instructed to rely on verified analytics results rather than invent numerical values.
- Sensitive credentials are not included in the frontend.

## 📌 Example Questions

After uploading a dataset, users can ask questions such as:

```text
What is the average Temperature?

What is the maximum Pressure?

How many faulty sensors are there?

How many missing values are present?

What columns are available in the dataset?

What is the correlation between Temperature and Pressure?
```

## 🎯 Purpose

The goal of InsightFlow AI is to demonstrate how **LLMs, RAG, and traditional data analytics can work together** to create a reliable natural-language interface for structured datasets.

Instead of relying entirely on an LLM to perform calculations, the platform uses Python-based analytics for numerical accuracy and uses the LLM primarily for interpretation and explanation.

## 📁 Project Structure

```text
insightflow-ai/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── ai.py
│   │   │   └── datasets.py
│   │   │
│   │   ├── services/
│   │   │   ├── analytics_service.py
│   │   │   ├── data_profiler.py
│   │   │   ├── dataset_storage.py
│   │   │   ├── llm_service.py
│   │   │   └── rag_service.py
│   │   │
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── vercel.json
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── index.css
│   └── package.json
│
├── screenshots/
│   ├── dataset-upload.png
│   ├── ai-analysis.png
│   ├── data-visualization.png
│   └── dataset-profile.png
│
└── README.md
```

## 🙏 Acknowledgments

**Built using modern AI, data analytics, and web development technologies.**

**Built and maintained by Mayank Palsikar**
