from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
import os

from database import get_db, Conversation, FAQ
from models.intent_classifier import IntentClassifier, MultilingualTranslator

# Initialize app
app = FastAPI(title="College Chatbot API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize models
intent_classifier = IntentClassifier()
translator = MultilingualTranslator()

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    user_id: str = "anonymous"
    language: str = "en"

class ChatResponse(BaseModel):
    response: str
    detected_language: str
    intent: str
    confidence: float

def get_faq_response(intent: str, language: str, db: Session):
    faq = db.query(FAQ).filter(FAQ.intent == intent).first()
    if faq:
        answer_column = f"answer_{language}"
        if hasattr(faq, answer_column):
            answer = getattr(faq, answer_column)
            if answer and answer.strip():
                return answer
        return faq.answer_en
    return None

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        # Detect language
        detected_lang = translator.detect_language(request.message)
        
        # Classify intent
        intent, confidence = intent_classifier.classify_intent(request.message)
        
        # Get response from FAQ database
        response = get_faq_response(intent, request.language, db)
        
        if not response:
            response = "I'm not sure about that. Please contact the college administration."
        
        # Log conversation
        conversation = Conversation(
            user_id=request.user_id,
            user_message=request.message,
            bot_response=response,
            detected_language=detected_lang,
            intent=intent,
            confidence=confidence,
            source="web"
        )
        db.add(conversation)
        db.commit()
        
        return ChatResponse(
            response=response,
            detected_language=detected_lang,
            intent=intent,
            confidence=confidence
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def read_index():
    return FileResponse('frontend/index.html')

# Serve static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)