from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from services.openai_service import generate_response
from typing import List, Dict
import json
from services.pipefy_service import create_pipefy_card

# Criar a instancia principal da aplicacao
app = FastAPI(
    title="AI SDR Agent API",
    description="API para o agente SDR de IA",
    version="0.4.0"
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

# --- Rotas da API ---
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
    Recebe um historico de mensagens, processa pela OpenIA e agora TAMBEM verifica
    se a resposta e um gatilho de acao (JSON) ou tex
    """
    # Logar apenas a ultima mensagem para nao poluir demais o console
    if request.history:
        print(f"Histórico recebido(ultima msg): {request.history[-1]['content']}")
    else:
        print("Histórico recebido vazio")
    
    # 1. Gerar a resposta da IA 
    ai_response = generate_response(request.history)
    print(f"Resposta da IA: {ai_response}")    
    
    # 2. O "MAESTRO" tenta ler a resposta como JSON
    try:
        # Tentar carregar a resposta da IA como um dicionario em python
        json_data = json.loads(ai_response)
        
        # Se der certo, verifica se e o gatilho que esperamos
        if json_data.get("action") == "create_lead":
            print("GATILHO DETECTADO: 'create_lead'")
            
            lead_data = json_data.get("data")
            print(f"Dados do Lead: {lead_data}")
            
            # Aqui chamamos o servico do Pipefy para criar o card
            card_info = create_pipefy_card(lead_data)
            print(f"Informações do card: {card_info}")
            
            # Retornar uma mensagem de sucesso para o usuario
            # E TAMBEM o JSON de gatilho
            return ChatResponse(response=json.dumps({
                "status": "success",
                "message": "Lead sendo processado...",
                "lead_data": lead_data,
                "pipefy_card": card_info.get("url")
            }))
    except json.JSONDecodeError:
        # Se der erro, nao era um JSON. Era so texto normal.
        # Apenas retorna a resposta de texto da IA para continuar a conversa
        print("Resposta é texto normal, continuando a conversa.")
        pass
    
    # Se nao era um gatilho, retorna a resposta normal da IA
    return ChatResponse(response=ai_response)
    
# Permite rodar o app diretamente com python main.py
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)