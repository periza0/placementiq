import os
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
# FREE embeddings
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

TEXT_FOLDER = "data/extracted"
CHROMA_PATH = "data/chroma"

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

documents = []
seen_chunks = set()

print("Reading text files...\n")

for file in os.listdir(TEXT_FOLDER):

    if not file.endswith(".txt"):
        continue

    path = os.path.join(TEXT_FOLDER, file)

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    chunks = splitter.split_text(text)

    for chunk in chunks:

        key = chunk.strip()

        if len(key) < 30:
            continue

        if key in seen_chunks:
            continue

        seen_chunks.add(key)

        documents.append(
            Document(
                page_content=chunk,
                metadata={
                    "source": file
                }
            )
        )

print(f"Total unique chunks : {len(documents)}")

print("\nCreating Chroma Database...\n")

db = Chroma.from_documents(
    documents,
    embedding_model,
    persist_directory=CHROMA_PATH
)

print("\n✅ ChromaDB Created Successfully!")