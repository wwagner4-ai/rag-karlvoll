from pathlib import Path
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import uvicorn
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv

import splitpdf.embed as embed_
import splitpdf.llm as llm_
import splitpdf.helper as hlp_


load_dotenv()

vector_database = embed_.VectorDatabase()

llm = llm_.Llm(key=os.environ.get("TOGETHER_KEY"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    print("Shutting down")
    vector_database.close()
    llm.close()


context = {}
app = FastAPI(title="Text Query API", lifespan=lifespan)


def query_vector_database(prompt: str) -> list[str]:
    def to_docstring(index: int, doc: embed_.Document) -> str:
        return f"{index:4d} {doc.page_number:4d} - {doc.text}"

    documents = vector_database.query(hlp_.COLLECTION_NAME, prompt)
    return [to_docstring(i, d) for i, d in enumerate(documents)]


def query_llm(prompt: str) -> list[str]:
    return llm.query(prompt)


@app.get("/query")
async def handle_query(
    text: str = Query(..., description="The text content to process", min_length=1),
):
    # answer = query_vector_database(text)
    answer = query_llm(text)
    html_answer = "</br></br>".join(answer)
    return {
        "received_text": text,
        "answer": html_answer,
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
