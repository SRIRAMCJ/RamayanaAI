"""FastAPI application for the Ramayana AI assistant."""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from rag.rag_pipeline import RAGPipeline
from tts.tts_service import PiperTTS
from translator.qwen_translator import QwenTranslator


BACKEND_DIR = Path(__file__).resolve().parents[1]
FRONTEND_DIR = BACKEND_DIR / "frontend"
AUDIO_DIR = BACKEND_DIR / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="Ramayana AI",
    version="1.0.0",
    description="Ask questions about the Valmiki Ramayana in English or Hindi.",
)

app.mount("/audio", StaticFiles(directory=AUDIO_DIR), name="audio")
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

rag: RAGPipeline | None = None
tts: PiperTTS | None = None
translator: QwenTranslator | None = None


@app.on_event("startup")
def initialize_services() -> None:
    """Load local services after the app starts so setup errors are actionable."""
    global rag, tts, translator
    rag = RAGPipeline()
    tts = PiperTTS()
    translator = QwenTranslator()


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    language: str = "en"


@app.get("/")
def home():
    from fastapi.responses import FileResponse

    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/health")
def health():
    return {"status": "ok", "ready": rag is not None and tts is not None}


@app.post("/chat")
def chat(request: ChatRequest):
    if rag is None or tts is None or translator is None:
        raise HTTPException(status_code=503, detail="The assistant is still starting.")

    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=422, detail="Question cannot be empty.")

    language = request.language.lower()
    if language not in {"en", "hi"}:
        raise HTTPException(status_code=422, detail="Language must be 'en' or 'hi'.")

    try:
        if language == "hi":
            question_for_rag = translator.hindi_to_english(question)
        else:
            question_for_rag = question

        answer = rag.ask(question=question_for_rag, language="en")
        if answer.startswith("Error:"):
            raise RuntimeError(answer.removeprefix("Error:").strip())
        if language == "hi":
            answer = translator.english_to_hindi(answer)

        audio_filename = tts.generate(answer, language)
        answer_lower = answer.lower()
        characters = (
            "rama", "sita", "hanuman", "ravana", "lakshmana", "bharata",
            "shatrughna", "dasharatha", "kaikeyi", "janaka", "vibhishana",
            "kumbhakarna", "indrajit", "sugriva", "vali",
        )
        character = next((name for name in characters if name in answer_lower), "default")

        return {
            "success": True,
            "question": request.question,
            "language": language,
            "answer": answer,
            "character": character,
            "audio": {
                "file": audio_filename,
                "url": f"/audio/{audio_filename}",
                "voice": "hi_IN-pratham-medium" if language == "hi" else "en_IN-medium",
            },
        }
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Could not answer the question: {exc}") from exc
