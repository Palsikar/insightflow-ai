from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.llm_service import ask_llm
from app.services.data_profiler import profile_dataset
from app.services.rag_service import (
    create_profile_documents,
    add_documents,
    search_documents
)
from app.services.analytics_service import analyze_dataset

import pandas as pd
from io import BytesIO
from app.services.dataset_storage import load_dataset


router = APIRouter(
   prefix="/api/ai",
    tags=["AI"]
)

class QuestionRequest(BaseModel):
    dataset_id: str
    question: str


@router.post("/ask")
async def ask_question(request: QuestionRequest):
    stored_dataset = await load_dataset(request.dataset_id)

    if stored_dataset is None:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    extension, contents = stored_dataset

    try:
        if extension == ".csv":
            dataframe = pd.read_csv(BytesIO(contents))
        else:
            dataframe = pd.read_excel(BytesIO(contents))

        # -----------------------------------
        # 1. PROFILE DATASET
        # -----------------------------------

        profile = profile_dataset(dataframe)

        # -----------------------------------
        # 2. CREATE RAG DOCUMENTS
        # -----------------------------------

        profile_documents = create_profile_documents(profile)

        add_documents(profile_documents)

        # -----------------------------------
        # 3. RETRIEVE RELEVANT INFORMATION
        # -----------------------------------

        relevant_documents = search_documents(
            request.question,
            top_k=3
        )

        context = "\n\n".join(
            relevant_documents
        )

        # -----------------------------------
        # 4. PERFORM ACTUAL DATA ANALYSIS
        # -----------------------------------

        analytics_result = analyze_dataset(
            dataframe,
            request.question
        )

        # -----------------------------------
        # 5. CREATE FINAL LLM PROMPT
        # -----------------------------------

        prompt = f"""
You are InsightFlow AI, an intelligent data analytics assistant.

Use the retrieved dataset information and verified
analytics results to answer the user's question.

Retrieved information:
{context}

Verified analytics result:
{analytics_result}

User question:
{request.question}

Instructions:
- Use the verified analytics result whenever it is available.
- Do not invent numerical values.
- Do not perform calculations yourself when a verified result is provided.
- Use the retrieved information to provide additional context.
- If the available information is insufficient, clearly say so.
- Keep the answer clear and concise.
"""

        # -----------------------------------
        # 6. ASK LLM
        # -----------------------------------

        answer = ask_llm(prompt)

        return {
            "dataset_id": request.dataset_id,
            "question": request.question,
            "analytics_result": analytics_result,
            "retrieved_documents": relevant_documents,
            "answer": answer
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"AI analysis error: {str(error)}"
        )