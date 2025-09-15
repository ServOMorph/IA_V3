from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from api.routes.sessions import chat_manager  # importer l’instance gérée par sessions.py

router = APIRouter(prefix="/chat", tags=["chat"])

class PromptRequest(BaseModel):
    prompt: str

class AnswerResponse(BaseModel):
    answer: str

@router.post("/", response_model=AnswerResponse)
def chat_endpoint(req: PromptRequest):
    if not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt vide")

    if not chat_manager:
        raise HTTPException(status_code=400, detail="Aucune session active")

    answer = chat_manager.process_prompt(req.prompt)
    return {"answer": answer}
