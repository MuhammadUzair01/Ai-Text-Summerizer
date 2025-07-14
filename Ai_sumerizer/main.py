from fastapi import FastAPI, HTTPException, File, UploadFile
import aiofiles
from model import TextIn, SummaryOut, SummaryRecord
from sumerizer import summarize_text
from db import summary_collection
from datetime import datetime

app = FastAPI()

def format_summary_record(doc):
    return {
        "id": str(doc["_id"]),
        "text": doc["text"],
        "summary": doc["summary"],
        "created_at": doc["created_at"]
    }

@app.post("/summarize", response_model=SummaryOut)
async def summarize(data: TextIn):
    if len(data.text.strip()) < 50:
        raise HTTPException(status_code=400, detail="Text is too short to summarize")
    summary = summarize_text(data.text)
    doc = {
        "text": data.text,
        "summary": summary,
        "created_at": datetime.utcnow()
    }
    await summary_collection.insert_one(doc)
    return {"summary": summary}

@app.get("/history", response_model=list[SummaryRecord])
async def get_history():
    cursor = summary_collection.find().sort("created_at", -1).limit(20)
    summaries = []
    async for doc in cursor:
        summaries.append(format_summary_record(doc))
    return summaries

@app.post("/summarize-file", response_model=SummaryOut)
async def summarize_file(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.txt'):
        raise HTTPException(status_code=400, detail="Only .txt files are supported")

    try:
        content = await file.read()
        text = content.decode("utf-8", errors="ignore")
    except Exception:
        raise HTTPException(status_code=400, detail="Could not decode file content. Make sure it's a UTF-8 text file.")

    if len(text.strip()) < 50:
        raise HTTPException(status_code=400, detail="Text is too short to summarize")

    summary = summarize_text(text)

    doc = {
        "text": text,
        "summary": summary,
        "created_at": datetime.utcnow()
    }

    await summary_collection.insert_one(doc)
    return {"summary": summary}
