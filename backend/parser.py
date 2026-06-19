import os
import zipfile
import fitz  # PyMuPDF
from docx import Document
from striprtf.striprtf import rtf_to_text

RAW_FOLDER = "data"
OUTPUT_FOLDER = "data/extracted"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def extract_pdf(path):
    doc = fitz.open(path)

    text = ""

    for page in doc:
        text += page.get_text()

    return text


def extract_docx(path):

    doc = Document(path)

    return "\n".join(
        paragraph.text
        for paragraph in doc.paragraphs
    )


def extract_rtf(path):

    with open(path, "r", encoding="utf-8", errors="ignore") as f:

        return rtf_to_text(f.read())


def save_text(text, original_file):

    filename = os.path.splitext(
        os.path.basename(original_file)
    )[0]

    output = os.path.join(
        OUTPUT_FOLDER,
        filename + ".txt"
    )

    with open(output, "w", encoding="utf-8") as f:
        f.write(text)


def extract_zip(path):

    folder = os.path.splitext(path)[0]

    os.makedirs(folder, exist_ok=True)

    with zipfile.ZipFile(path, "r") as zip_ref:
        zip_ref.extractall(folder)

    print(f"📦 Extracted {path}")


def process_file(path):

    try:

        if path.endswith(".pdf"):

            text = extract_pdf(path)

            save_text(text, path)

            print("✅ PDF", path)

        elif path.endswith(".docx"):

            text = extract_docx(path)

            save_text(text, path)

            print("✅ DOCX", path)

        elif path.endswith(".rtf"):

            text = extract_rtf(path)

            save_text(text, path)

            print("✅ RTF", path)

        elif path.endswith(".zip"):

            extract_zip(path)

    except Exception as e:

        print("❌", path)

        print(e)


def walk(folder):

    for root, dirs, files in os.walk(folder):

        for file in files:

            process_file(
                os.path.join(root, file)
            )


if __name__ == "__main__":

    walk(RAW_FOLDER)

    print("\n Parsing Complete")