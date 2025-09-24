from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from api.routes import sessions  # pour accéder à chat_managers

router = APIRouter(prefix="/chat", tags=["chat"])

class PromptRequest(BaseModel):
    prompt: str

class AnswerResponse(BaseModel):
    answer: str
    session: str  # nom final de la session

@router.post("/{session_name}", response_model=AnswerResponse)
def chat_endpoint(session_name: str, req: PromptRequest):
    print("=== DEBUG chat_endpoint appelé ===")
    if not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt vide")

    cm = sessions.chat_managers.get(session_name)
    if not cm:
        raise HTTPException(status_code=404, detail="Session introuvable")

    # 1) Génération de la réponse IA
    answer = cm.process_prompt(req.prompt)

    # 2) Forcer l’auto-titler à se terminer avant de renvoyer
    # (le SaveManager/AutoTitler a pu changer le nom de session)
    final_name = cm.save_manager.session_name

    # 3) Mettre à jour le dictionnaire global si le nom a changé
    if session_name != final_name:
        sessions.chat_managers[final_name] = sessions.chat_managers.pop(session_name)
        print(f"[DEBUG] Session renommée automatiquement: {session_name} → {final_name}")

    # 4) Retourner la réponse ET le nom final de la session
    return {
        "answer": answer,
        "session": final_name
    }
