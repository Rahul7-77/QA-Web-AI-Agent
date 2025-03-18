from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def setup_llm():
    """Initialize Groq client."""
    if not GROQ_API_KEY:
        raise ValueError("Groq API key not found in .env")
    return Groq(api_key=GROQ_API_KEY)

def generate_answer(query, search_results):
    """Generate answer using Groq API."""
    llm = setup_llm()
    if not search_results or search_results[0][0] is None:
        return "Sorry, I couldn’t find information about that in the website.", None
    context, url, _ = search_results[0]
    prompt = (
        f"Using the following context, answer the question concisely and clearly. If you dont know reply as 'Sorry, I couldn’t find information about that in the website.'\n"
        f"Context: {context[:4000]}\n"
        f"Question: {query}\n"
        f"Answer:"
    )
    response = llm.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.5
    )
    answer = response.choices[0].message.content.strip()
    return answer, url