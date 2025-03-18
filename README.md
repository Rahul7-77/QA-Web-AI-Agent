# QA-Web-AI-Agent

An AI agents which scrapes websites, perform semantic search, and answer questions. It uses recursive crawling, semantic search, and natural language processing.

## Setup Instructions
1. **Clone Repository**: 
  * git clone https://github.com/Rahul7-77/QA-Web-AI-Agent.git 
  * cd QA-Web-AI-Agent
    
2. **Install Dependencies**:
  * pip install -r requirements.txt

3. **Configure Environment**:
- Create a `.env` file in the root directory:
- HF_TOKEN=your_hugging_face_token
- GROQ_API_KEY=your_groq_api_key
- Obtain tokens from [Hugging Face](https://hf.co/settings/tokens) and [Groq](https://console.groq.com).

4. **Run the Application**:
- `python app.py`

## Dependencies
- `huggingface_hub`: Embeds text via Hugging Face API (`all-MiniLM-L6-v2`).
- `groq`: Generates answers using Groq API (`mixtral-8x7b-32768`).
- `faiss-cpu`: Indexes embeddings for semantic search.
- `numpy`: Handles numerical operations for embeddings.
- `requests`: Fetches web content.
- `beautifulsoup4`: Parses HTML for scraping.
- `validators`: Validates URLs.
- `python-dotenv`: Loads environment variables from `.env`.

## Usage Examples
1. Launch the app:
2. Enter a help website URL: `https://python.langchain.com/docs`
3. Ask questions:
- **Input**: `What is LangChain?`
  - **Output**: "LangChain is a framework for developing applications powered by language models."
  - **Source**: `https://python.langchain.com/docs`
- **Input**: `what integrations are available??`
  - **Output**: " LangChain integrates with a variety of providers, including OpenAI, Anthropic, Azure, Google, Vertex, AWS, Groq, Cohere, NVIDIA, Fireworks AI, Mistral AI, IBM watsonx, Databricks, and xAI."
  - **Source**: `https://python.langchain.com/docs`
- **Input**: `how to use chat models?`
  - **Output**: "Chat models, in the context of LangChain, are components of the framework that power conversational capabilities in applications."
  - **Source**: `https://python.langchain.com/docs`

## Design Decisions
- **API-Based Embeddings**: Chose Hugging Face API over local models to avoid downloads, aligning with development preferences while meeting semantic search requirements.
- **Semantic Search**: Implemented FAISS with cosine similarity (`IndexFlatIP`) and a 0.1 threshold to ensure high recall, tuned after testing to catch straightforward queries like "What is LangChain?".
- **Text Generation**: Selected Groq’s `mixtral-8x7b-32768` for its speed (~500 tokens/s) and free tier, delivering concise answers within a 150-token limit(token limit can be increased).
- **Scraping Strategy**: Recursive crawler limited to 12 pages of max depth 3 with broad tag selection (`p`, `h1-h6`, `li`, `td`, `th`) to maximize content capture.
- **Modularity**: Split into `scrape_web`, `embed_text`, `store_vectors`, `semantic_search`, and `question_answer` modules for maintainability and testing.

  ## Known Limitations
- **API Reliability**: Dependent on Hugging Face API. Sometimes API might generate uptime—503 error (Retry after few seconds when 503 error occurs)
- **Scraping Depth**: Caps at 12 pages of max depth 3, potentially missing deeper documentation; `time.sleep(1)` slows scraping (~5-10s total).
- **Similarity Threshold**: 0.1 is permissive, risking low-relevance results for vague queries (e.g., `dist = 0.15` might be noise).
- **Context Truncation**: Limits context to 4000 characters for Groq, potentially cutting off longer explanations.
- **Single Result**: Returns only the top FAISS match (`k=1`).
