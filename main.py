import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai

# 1. Création de l'application (Le serveur)
app = FastAPI()

# 2. Autorisation de ton interface HTML (CORS)
# Cela permet à ta page web de parler à ce script en toute sécurité
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Configuration de l'IA (Gemini)
# On laisse la clé vide pour l'instant, on la configurera sur le serveur
api_key = os.environ.get("GEMINI_API_KEY", "")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# 4. Modèle de données (Ce que l'élève envoie)
class Message(BaseModel):
    text: str
    level: str = "B1"

# 5. La route "Coach" (L'endroit où on envoie les questions)
@app.post("/coach")
async def ask_coach(msg: Message):
    try:
        # Le "Prompt" : Les instructions données au prof IA
        prompt = f"""
        You are Peter's English Coach. 
        The student (level: {msg.level}) said: "{msg.text}"
        
        Please:
        1. Correct any grammar mistakes.
        2. Explain why you made the correction in simple English.
        3. Give a more natural alternative used by native speakers.
        4. Always end with an encouraging sentence.
        """
        
        response = model.generate_content(prompt)
        return {"reply": response.text}
        
    except Exception as e:
        return {"reply": "Sorry, I'm having trouble connecting to my brain right now."}

if __name__ == "__main__":
    import uvicorn
    # Lancement du serveur sur le port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
