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


def ask_llm(context, question, source_context=""):

    prompt = f"""
You are PlacementIQ.

Answer ONLY using the context and source list below.

If the user asks for companies, list every relevant company from the source list.
Do not omit a company that appears in the source list.
Keep the answer direct and easy to scan.
If the answer is not present in the context or source list,
say that you don't know.

Source list:
{source_context}

Context:
{context}

Question:
{question}
"""

    response = model.generate_content(prompt)

    return response.text