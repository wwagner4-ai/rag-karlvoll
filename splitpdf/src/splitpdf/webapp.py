from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from typing import Optional
import uvicorn
from pathlib import Path

app = FastAPI(title="Text Query API")


@app.get("/query")
async def handle_query(
    text: str = Query(..., description="The text content to process", min_length=1),
    limit: Optional[int] = Query(None, description="Optional limit for results"),
):
    """
    Handles a GET request to /query?text=your_text_here
    """
    return {
        "received_text": text,
        "character_count": len(text),
        "uppercase": text.upper(),
        "limit_applied": limit,
    }

@app.get("/", response_class=HTMLResponse)
async def handle_index():
    index_path = Path(__file__).parent / "web" / "index.html"
    text = index_path.read_text()
    return text


def start():
    uvicorn.run(app, host="0.0.0.0", port=8000)
