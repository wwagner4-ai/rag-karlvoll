from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import uvicorn
from pathlib import Path

context = {}
app = FastAPI(title="Text Query API")


@app.get("/query")
async def handle_query(
    text: str = Query(..., description="The text content to process", min_length=1),
):
    # print(f"query/text: '{text}'")
    answer = f"Answer to: '{text}'"
    return {
        "received_text": text,
        "answer": answer,
    }


@app.get("/", response_class=HTMLResponse)
async def handle_index():
    index_path = Path(__file__).parent / "web" / "index.html"
    text = index_path.read_text()
    text = text.replace("{{port}}", context["port"])
    return text


@app.get("/jquery.js", response_class=HTMLResponse)
async def handle_jquiry():
    path_ = Path(__file__).parent / "web" / "jquery-4.0.0.min.js"
    text = path_.read_text()
    return text


def start(port: int):
    context["port"] = str(port)
    uvicorn.run(app, host="0.0.0.0", port=port)
