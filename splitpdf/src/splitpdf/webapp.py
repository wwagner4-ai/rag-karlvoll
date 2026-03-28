from fastapi import FastAPI, Query
from typing import Optional
import uvicorn

app = FastAPI(title="Text Query API")


@app.get("/query")
async def handle_query(
    text: str = Query(..., description="The text content to process", min_length=1),
    limit: Optional[int] = Query(None, description="Optional limit for results"),
):
    """
    Handles a GET request to /query?text=your_text_here
    """
    # Example logic: returning the text and its metadata
    return {
        "received_text": text,
        "character_count": len(text),
        "uppercase": text.upper(),
        "limit_applied": limit,
    }


def start():
    uvicorn.run(app, host="0.0.0.0", port=8000)
