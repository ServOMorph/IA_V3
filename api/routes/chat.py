from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from api.routes.sessions import chat_managers

router = APIRouter(prefix="/chat", tags=["chat"])

class PromptRequest(BaseModel):
    prompt: str

class AnswerResponse(BaseModel):
    answer: str

@router.post("/{session_name}", response_model=AnswerResponse)
def chat_endpoint(session_name: str, req: PromptRequest):
    if not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt vide")

    cm = chat_managers.get(session_name)
    if not cm:
        raise HTTPException(status_code=404, detail="Session introuvable")

    answer = cm.process_prompt(req.prompt)
    return {"answer": answer}
