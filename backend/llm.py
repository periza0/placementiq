import os

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def ask_llm(context, question):

    prompt = f"""
You are PlacementIQ.

Answer ONLY using the context below.

If the answer is not present in the context,
say that you don't know.

Context:
{context}

Question:
{question}
"""

    response = model.generate_content(prompt)

    return response.text