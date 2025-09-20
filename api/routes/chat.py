from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from api.routes import sessions  # pour accéder à chat_managers

router = APIRouter(prefix="/chat", tags=["chat"])

class PromptRequest(BaseModel):
    prompt: str

class AnswerResponse(BaseModel):
    answer: str
    session: str  # nouveau champ

@router.post("/{session_name}", response_model=AnswerResponse)
def chat_endpoint(session_name: str, req: PromptRequest):
    print("=== DEBUG chat_endpoint appelé ===")
    if not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt vide")

    cm = sessions.chat_managers.get(session_name)
    if not cm:
        raise HTTPException(status_code=404, detail="Session introuvable")

    answer = cm.process_prompt(req.prompt)

    # Vérifier si le nom de session a changé après auto-titler
    current_name = cm.save_manager.session_name
    if session_name != current_name:
        # mettre à jour le dictionnaire global
        sessions.chat_managers[current_name] = sessions.chat_managers.pop(session_name)
        session_name = current_name

    return {"answer": answer, "session": session_name}
