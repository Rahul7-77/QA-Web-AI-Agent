# Documentation

## How It Works
This AI agent scrapes help websites, searches for info using semantic search and answers questions.

- **Main Parts**:
  - **Scraper**: Gets text from websites (like `https://python.langchain.com/docs`).
  - **Embedding**: Turns text into embeddings with Hugging Face API. Stores embeddings in FAISS.
  - **Search**: Finds the best match using FAISS based on cosine similarity criteria.
  - **Answer**: Passes best match and question as prompt to groq LLM. groq LLM gives clear answer.
- **Steps**:
  1. Type a website URL—it grabs up to 12 pages of max depth 3.
  2. Saves the text in a way the computer can search.
  3. Ask a question—it finds the answer and shows where it came from.

## How We Built It
- **Easy Setup**: Split into files like `scrape_web.py` and `question_answer.py` so it’s not messy.
- **APIs**: Used Hugging Face for embeddings and Groq for answers—no big files to download.
- **Search Trick**: Set a low match level (0.1) of cosine similarity, so it finds answers even if they’re not exact.

## Ideas to Improve
- **Backup**: Use a local version if the internet APIs stop working.
- **More Text**: Grab more than 12 pages without slowing down.
- **Better Answers**: Look at more matches, not just one, for fuller answers.
- **Local Caching**: Use Local Caching for frequent type questions
- **Containerization** Use docker to containerize whole ai agent.

## Testing
- **What We Did**: Wrote 3 tests in `tests/test_agent.py` to check:
  - Scraping gets text.
  - Embedding makes numbers.
  - The whole thing answers "What is LangChain?" right.
- **How**: Used `pytest`—ran it, got 3 passes (takes ~7-10 seconds).
- **Speed**: Setup is ~10-15 seconds, answers come in ~1-3 seconds.
