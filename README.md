# Law Study Buddy 🏛️

An AI-powered legal research assistant using Retrieval Augmented Generation (RAG) technology.

## Features

- **Legal Document Analysis**: Process and analyze PDF legal documents
- **AI-Powered Q&A**: Get detailed legal answers with citations
- **Source Referencing**: All answers include source documents and confidence scores
- **FastAPI Backend**: Robust REST API for legal queries
- **Streamlit Frontend**: User-friendly web interface

## Tech Stack

- **Backend**: FastAPI, Python
- **AI/ML**: LangChain, Groq LLM, Sentence Transformers
- **Vector Database**: ChromaDB
- **Frontend**: Streamlit
- **Document Processing**: PyMuPDF

## Quick Start

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in `.env`
4. Run FastAPI: `uvicorn app.main:app --reload`
5. Run Streamlit: `streamlit run app/streamlit_app.py`

## API Documentation

Once running, visit:
- FastAPI Docs: http://localhost:8000/docs
- Streamlit App: http://localhost:8501

## License

MIT License