# Ramayana AI

A local question-answering app for the Valmiki Ramayana. It uses FastAPI, a Chroma vector index, Ollama (`qwen3:4b`), and Piper speech synthesis.

## Requirements

- Python 3.11 (64-bit)
- [Ollama](https://ollama.com/download), with the `qwen3:4b` model
- Internet access the first time the embedding model (`BAAI/bge-m3`) is downloaded

## Windows setup

From the repository root in PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r Backend\requirements.txt
ollama pull qwen3:4b
python Backend\embeddings\vector_store.py
python -m uvicorn api.main:app --app-dir Backend --host 127.0.0.1 --port 8000
```

Open <http://127.0.0.1:8000>. Keep Ollama running while using the app. The first vector-index build downloads the embedding model and can take several minutes. The index is stored under `Database/chroma_db/`; rerun the vector-store command to update it.

## API

- `GET /health` reports whether the assistant finished loading.
- `POST /chat` accepts `{"question":"Who is Hanuman?","language":"en"}`. Use `"hi"` for Hindi.
- `GET /docs` provides interactive API documentation.

The Piper voice models the app uses are included in `Models/Piper/`. Generated speech and the vector database are local runtime files and are ignored by Git.
