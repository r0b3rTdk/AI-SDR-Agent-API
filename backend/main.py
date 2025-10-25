from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from services.openai_service import generate_response
from typing import List, Dict

# Criar a instancia principal da aplicacao
app = FastAPI(
    title="AI SDR Agent API",
    description="API para o agente SDR de IA",
    version="0.3.0"
)

# --- Modelo de Dados (Pydantic) ---
# Definir como o corpo da requisicao /chat deve ser
class ChatRequest(BaseModel):
    # A API agora vai receber o historico da conversa
    # EXEMPLO: [{"role": "user", "content": "Oi"}, {"role": "assistant", "content": "Olá"}]
    history: List[Dict[str, str]]
    
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
    Recebe um HISTORICO de mensagens, processa pela OpenIA e retorna uma resposta
    """
    # Logar apenas a ultima mensagem para nao poluir demais o console
    if request.history:
        print(f"Histórico recebido(ultima msg): {request.history[-1]['content']}")
    else:
        print("Histórico recebido vazio")
    
    # Passar o historico para a funcao de gerar resposta  
    ai_response = generate_response(request.history)
    
    print(f"Resposta da IA: {ai_response}")    
    return ChatResponse(response=ai_response)
    
# Permite rodar o app diretamente com python main.py
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)