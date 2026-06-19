import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from models import ChatRequest
from llm import ask_llm

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


vector_db = Chroma(
    persist_directory="chroma",
    embedding_function=embedding_model
)


@app.get("/")
def home():

    return {
        "message": "PlacementIQ Backend Running 🚀"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    docs = vector_db.similarity_search(
        request.question,
        k=5
    )

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    answer = ask_llm(
        context,
        request.question
    )

    seen = set()

    sources = []

    for doc in docs:

        filename = doc.metadata["filename"]

        if filename in seen:
            continue

        seen.add(filename)

        sources.append(
            {
                "company": doc.metadata["company"],
                "file": filename,
                "path": doc.metadata["path"]
            }
        )

    return {
        "answer": answer,
        "sources": sources
    }