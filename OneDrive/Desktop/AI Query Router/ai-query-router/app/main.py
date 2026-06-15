from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
import os

app = FastAPI(
    title="AI Query Router",
    description="Routes natural language questions to Groq (LLaMA3)",
    version="1.0.0"
)

# ── Request / Response models ─────────────────────────────────
class QueryRequest(BaseModel):
    question: str
    max_tokens: int = 500

class QueryResponse(BaseModel):
    answer: str
    model: str
    tokens_used: int

# ── Health check ──────────────────────────────────────────────
@app.get("/health")
def health_check():
    return {"status": "ok", "service": "ai-query-router"}

# ── Main query endpoint ────────────────────────────────────────
@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not set")

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": request.question}
        ],
        max_tokens=request.max_tokens
    )

    return QueryResponse(
        answer=response.choices[0].message.content,
        model=response.model,
        tokens_used=response.usage.total_tokens
    )