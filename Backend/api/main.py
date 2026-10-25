"""
=====================================================
Ramayana AI API
=====================================================
"""
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from rag.rag_pipeline import RAGPipeline
from tts.tts_service import PiperTTS
from translator.qwen_translator import QwenTranslator


# =====================================================
# FASTAPI APP
# =====================================================

app = FastAPI(
    title="Ramayana AI",
    version="1.0.0",
    description="Offline AI-powered Ramayana Assistant with RAG + Ollama + Piper TTS"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# STATIC FILES
# =====================================================

# Generated Audio
app.mount(
    "/audio",
    StaticFiles(directory="audio"),
    name="audio"
)

# Frontend
app.mount(
    "/frontend",
    StaticFiles(directory="frontend"),
    name="frontend"
)


# =====================================================
# INITIALIZE COMPONENTS
# =====================================================

print("\nInitializing Ramayana AI...\n")

rag = RAGPipeline()
tts = PiperTTS()
translator = QwenTranslator()

print("\nRamayana AI Ready!\n")


# =====================================================
# REQUEST MODEL
# =====================================================

class ChatRequest(BaseModel):
    question: str
    language: str = "en"


# =====================================================
# HOME PAGE
# =====================================================

@app.get("/")
def home():
    return FileResponse("frontend/index.html")


# =====================================================
# CHAT API
# =====================================================

@app.post("/chat")
def chat(request: ChatRequest):

    try:

        print("\n" + "=" * 80)
        print("Generating Answer...")
        print("=" * 80)

        question = request.question.strip()
        language = (request.language or "en").lower()
        start_time = time.time()
        if not question:
            return {
                "success": False,
                "error": "Question cannot be empty."
                }

        print(f"\nOriginal Question : {question}")
        print(f"Language          : {language}")

        # --------------------------------------------------
        # Hindi -> English
        # --------------------------------------------------

        if language == "hi":

            print("\nTranslating Hindi -> English...\n")

            question = translator.hindi_to_english(question)

            print(f"Translated Question : {question}")

        # --------------------------------------------------
        # Ask RAG
        # --------------------------------------------------

        print("\nSearching Knowledge Base...\n")

        answer = rag.ask(
            question=question,
            language=language,
            )

        print("\nEnglish Answer:\n")
        print(answer)

        # =====================================================
        # DETECT MAIN CHARACTER
        # =====================================================

        answer_lower = answer.lower()

        character = "default"

        characters = [
            "rama",
            "sita",
            "hanuman",
            "ravana",
            "lakshmana",
            "bharata",
            "shatrughna",
            "dasharatha",
            "kaikeyi",
            "janaka",
            "vibhishana",
            "kumbhakarna",
            "indrajit",
            "sugriva",
            "vali",
        ]

        for name in characters:
            if name in answer_lower:
                character = name
                break

        print(f"\nDetected Character : {character}")

        # --------------------------------------------------
        # English -> Hindi
        # --------------------------------------------------

        if language == "hi":

            print("\nTranslating English -> Hindi...\n")

            answer = translator.english_to_hindi(answer)

            print("\nHindi Answer:\n")
            print(answer)

        # --------------------------------------------------
        # Generate Speech
        # --------------------------------------------------

        print("\nGenerating Speech...\n")

        audio_filename = tts.generate(
            answer,
            language
        )

        voice = (
            "hi_IN-pratham-medium"
            if language == "hi"
            else "en_IN-medium"
            )

        print("\nDone.\n")

        return {

            "success": True,

            "question": request.question,

            "language": language,

            "answer": answer,

            "character": character,

            "audio": {

                "file": audio_filename,

                "url": f"/audio/{audio_filename}",

                "voice": voice

            }

        }

    except Exception as e:

        print("\nERROR\n")
        print(str(e))

        return {

            "success": False,

            "error": str(e)

        }