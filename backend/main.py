from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from models import ChatRequest
from llm import ask_llm

BASE_DIR = Path(__file__).resolve().parent
CHROMA_DIR = BASE_DIR / "chroma"

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


try:
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"local_files_only": True},
    )

    vector_db = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embedding_model,
    )
except Exception as exc:
    embedding_model = None
    vector_db = None
    startup_error = exc
else:
    startup_error = None


def clean_company_name(company):

    name = company.replace("_", " ").strip()

    for prefix in ["JDs-", "JD-", "Job Description "]:
        if name.startswith(prefix):
            name = name[len(prefix):]

    for suffix in [" profiles", " profile"]:
        if name.lower().endswith(suffix):
            name = name[:-len(suffix)]

    return name.strip()


@app.get("/")
def home():

    return {
        "message": "PlacementIQ Backend Running 🚀"
    }


@app.post("/chat")
def chat(request: ChatRequest):
    if vector_db is None:
        raise HTTPException(
            status_code=503,
            detail=(
                "Vector database is unavailable. Run backend/ingest.py after "
                "the sentence-transformers model has been downloaded once."
            ),
        ) from startup_error

    company_query_words = ["company", "companies"]
    is_company_query = any(
        word in request.question.lower()
        for word in company_query_words
    )

    try:
        docs = vector_db.similarity_search(
            request.question,
            # Company-list questions need a wider result set before keyword filtering.
            k=20 if is_company_query else 5
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Unable to search the vector database. Re-run backend/ingest.py.",
        ) from exc

    if is_company_query:
        ignored_words = {
            "all", "any", "are", "company", "companies", "for", "list",
            "show", "the", "which", "with"
        }
        query_terms = [
            word
            for word in request.question.lower().replace("?", "").split()
            if word not in ignored_words
        ]

        keyword_docs = [
            doc
            for doc in docs
            if any(
                term in " ".join(
                    [
                        doc.page_content,
                        doc.metadata.get("company", ""),
                        doc.metadata.get("filename", ""),
                        doc.metadata.get("path", "")
                    ]
                ).lower()
                for term in query_terms
            )
        ]

        # Keep the wider search only as a fallback if keyword filtering finds nothing.
        docs = keyword_docs or docs

    seen = set()
    sources = []

    for doc in docs:
        filename = doc.metadata.get("filename") or doc.metadata.get("source")
        company = clean_company_name(
            doc.metadata.get("company") or Path(filename or "unknown").stem
        )
        path = doc.metadata.get("path") or filename or ""

        if filename in seen or company.lower() == "extracted":
            continue

        seen.add(filename)
        sources.append(
            {
                "company": company,
                "file": filename,
                "path": path
            }
        )

    source_context = "\n".join(
        f"- Company: {source['company']} | File: {source['file']} | Path: {source['path']}"
        for source in sources
    )

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    if is_company_query:
        company_names = []
        seen_companies = set()

        for source in sources:
            key = source["company"].lower()

            if key in seen_companies:
                continue

            seen_companies.add(key)
            company_names.append(source["company"])

        # Company questions should be exact and complete, so build this answer from filtered sources.
        answer = "Here are the matching companies:\n" + "\n".join(
            f"- {company}"
            for company in company_names
        )
    else:
        try:
            answer = ask_llm(
                context,
                request.question,
                # Source metadata is passed separately so the answer cannot omit returned companies.
                source_context
            )
        except Exception as exc:
            raise HTTPException(
                status_code=502,
                detail="Unable to get a response from Gemini. Check GEMINI_API_KEY.",
            ) from exc

    return {
        "answer": answer,
        "sources": sources
    }
