from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel
from tiny_pii.pii_pipeline import PIIPipeline
from sqlalchemy import desc
from pii_server.get_database import get_db, PIIAnalysisOutput
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from tiny_pii.types import TinyPIIOutput

app = FastAPI(title="PII API", description="API wrapper for tiny-pii", version="0.1.0")


# Define your request/response models
class InputModel(BaseModel):
    text: str


class OutputModel(BaseModel):
    redacted_text: str
    status: str


class PIIAnalysisOutputResponse(TinyPIIOutput):
    created_at: datetime

    class Config:
        from_attributes = True


@app.post("/process", response_model=OutputModel)
async def process_data(input_data: InputModel, db: Session = Depends(get_db)):
    try:
        # Initialize your library
        piepline = PIIPipeline()
        tiny_pii_output = piepline.process(input_data.text)

        db_record = PIIAnalysisOutput.from_pii_output(tiny_pii_output)
        db.add(db_record)
        db.commit()

        return OutputModel(redacted_text=tiny_pii_output.redacted_text, status="success")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history", response_model=List[PIIAnalysisOutputResponse])
async def get_analyses(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    analyses = (
        db.query(PIIAnalysisOutput)
        .order_by(desc(PIIAnalysisOutput.created_at))
        .offset(skip)
        .limit(limit)
        .all()
    )

    return analyses


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
