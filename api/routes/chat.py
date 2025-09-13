from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.chat_manager import ChatManager

router = APIRouter(prefix="/chat", tags=["chat"])

# Instance globale (à améliorer pour multi-utilisateurs plus tard)
chat_manager = ChatManager()

class PromptRequest(BaseModel):
    prompt: str

class AnswerResponse(BaseModel):
    answer: str

@router.post("/", response_model=AnswerResponse)
def chat_endpoint(req: PromptRequest):
    if not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt vide")
    answer = chat_manager.client.send_prompt(req.prompt)
    chat_manager.save_manager.save_md(chat_manager.client.history)
    return {"answer": answer}
