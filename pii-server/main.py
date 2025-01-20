from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tiny_pii.pii_pipeline import PIIPipeline

app = FastAPI(title="PII API", description="API wrapper for tiny-pii", version="0.1.0")


# Define your request/response models
class InputModel(BaseModel):
    text: str


class OutputModel(BaseModel):
    redacted_text: str
    status: str


@app.post("/process", response_model=OutputModel)
async def process_data(input_data: InputModel):
    try:
        # Initialize your library
        piepline = PIIPipeline()
        tiny_pii_output = piepline.process(input_data.text)

        # For demonstration
        result = f"Received {input_data.text}"

        return OutputModel(redacted_text=tiny_pii_output.redacted_text, status="success")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
