from pathlib import Path
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import uvicorn
from contextlib import asynccontextmanager

import splitpdf.embed as embed_
import splitpdf.helper as hlp_


vector_database = embed_.VectorDatabase()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    print("Shutting down")
    print("- Closing vector database")
    vector_database.close()


context = {}
app = FastAPI(title="Text Query API", lifespan=lifespan)


@app.get("/query")
async def handle_query(
    text: str = Query(..., description="The text content to process", min_length=1),
):
    def to_docstring(index: int, doc: embed_.Document) -> str:
        return f"{index:4d} {doc.page_number:4d} - {doc.text}"

    documents = vector_database.query(hlp_.COLLECTION_NAME, text)
    docs_text = "</br></br>".join([to_docstring(i, d) for i, d in enumerate(documents)])
    return {
        "received_text": text,
        "answer": docs_text,
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
