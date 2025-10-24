from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

# Criar a instancia principal da aplicacao
app = FastAPI(
    title="AI SDR Agent API",
    description="API para o agente SDR de IA",
    version="0.1.0"
)

# --- Modelo de Dados (Pydantic) ---
# Definir como o corpo da requisicao /chat deve ser
class ChatRequest(BaseModel):
    message: str
# Definir como sera a resposta do /chat
class ChatResponse(BaseModel):
    response: str

# Define uma rota raiz (GET)
@app.get("/")
def read_root():
    """Rota raiz que verifica se a API esta online"""
    return {"message": "AI SDR Agent API - online"}

# --- Endpoint de chat (POST) ---
# O endpoint principal que o frontend vai usar
@app.post("/chat", response_model=ChatResponse)
def handle_chat(request: ChatRequest):
    """
    Recebe uma mensagem do usuario e retorna uma resposta do agente
    (simulado por enquanto).
    """
    print(f"Mensagem recebida: {request.message}")
    # TODO: Substituir este mock por uma chamada real à OpenAI
    mock_response = f"Resposta simulada para: {request.message}"
    
    return ChatResponse(response=mock_response)
    
# Permite rodar o app diretamente com python main.py
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)