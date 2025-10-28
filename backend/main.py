"""
Verzel AI SDR Agent API
Autor: Robert Emanuel
Descrição: Orquestrador principal da API do agente SDR com integração OpenAI, Pipefy e Calendly.
Versão: 1.0.0
Data: 27/10/2025
"""

# ======================================================
# 📦 IMPORTAÇÕES
# ======================================================

# Built-in
import json

# Terceiros
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Locais (seus modulos)
from services.openai_service import generate_response
from services.pipefy_service import create_pipefy_card, update_pipefy_card_meeting_info
from services.calendar_service import get_available_slots, create_meeting
from typing import List, Dict

# ======================================================
# 🚀 CONFIGURAÇÃO DA APLICAÇÃO FASTAPI
# ======================================================

# Criar a instancia principal da aplicacao
app = FastAPI(
    title="AI SDR Agent API",
    description="API para o agente SDR de IA",
    version="0.7.0"
)

# --- HABILITAR CORS ---
origins = [
    "http://localhost:5173", # A origem do seu frontend React/Vite
    "http://127.0.0.1:5173", # As vezes o navegador usa esse
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Lista de origens permitidas
    allow_credentials=True,
    allow_methods=["*"], # Permite todos os metodos (GET, POST, etc.)
    allow_headers=["*"], # Permite todos os cabecalhos
)

# ======================================================
# 🧩 MODELOS Pydantic
# ======================================================

# Definir como o corpo da requisicao /chat deve ser
class ChatRequest(BaseModel):
    # A API agora vai receber o historico da conversa
    # EXEMPLO: [{"role": "user", "content": "Oi"}, {"role": "assistant", "content": "Olá"}]
    history: List[Dict[str, str]]
    
# Definir como sera a resposta do /chat
class ChatResponse(BaseModel):
    response: str
    
# Modelo para o novo endpoint de agendamento
class ScheduleRequest(BaseModel):
    slot_info: Dict # Informacoes do horario escolhido [ex: {"start_time": "...", "scheduling_url": "..."}]
    lead_data: Dict # Dados do lead(name, email, company, need)
    pipefy_card_id: str # ID do card no Pipefy para atualizar


# ======================================================
# 🌐 ENDPOINTS DA API
# ======================================================
    
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
    Processa o histórico de mensagens do usuário e decide se e uma resposta de texto
    ou um gatilho de criação de lead.
    - Se for texto → responde normalmente.
    - Se for JSON com {"action": "create_lead"} → cria card no Pipefy e agenda.
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
            # 1. Criar o card no Pipefy
            card_info = create_pipefy_card(lead_data)
            pipefy_card_id = card_info.get("id")
            print(f"Informações do card: {card_info}")
            
            # 2. Verifica se o cliente tem interesse para agendar
            if lead_data.get("interest_confirmed") is True:
                print("Interesse confirmado, buscando horarios...")
                
                # 3. Buscar horarios disponiveis
                available_slots = get_available_slots() # chama o calendar_service
            
                # 4. Retorna os horarios para o frontend
                # O frontend vai precisar mostrar esses horarios e guardar os dados do lead e o card_id
                return ChatResponse(response=json.dumps({
                    "action": "show_slots",
                    "slots": available_slots,
                    "lead_data": lead_data, # Devolve os dados para o frontend usar no /schedule
                    "pipefy_card_id": pipefy_card_id # Devolve o ID para o frontend usar no /schedule
                }))
            else:
                print("Interesse não confirmado. Lead registrado no Pipefy.")
                return ChatResponse(response=json.dumps({
                    "status": "success",
                    "message": "Lead registrado (sem interesse).",
                    "pipefy_card_url": card_info.get("url") 
            }))
                
    except json.JSONDecodeError:
        # Se der erro, nao era um JSON. Era so texto normal.
        # Apenas retorna a resposta de texto da IA para continuar a conversa
        print("Resposta é texto normal, continuando a conversa.")
        pass
    
    # Se nao era um gatilho, retorna a resposta normal da IA
    return ChatResponse(response=ai_response)

# --- Endpoint para agendar a reuniao ---
@app.post("/schedule")
async def schedule_meeting(request: ScheduleRequest):
    """
    Recebe o horario escolhido pelo usuario e os dados do lead,
    cria o evento no calendly e atualiza o card no Pipefy.
    """
    print(f"Recebida solicitação de agendamento para: {request.lead_data.get('email')}")
    print(f"Slot escolhido: {request.slot_info}")
    
    # 1. Criar o evento no Calendly
    meeting_confirmation = create_meeting(request.slot_info, request.lead_data)
    
    if "error" in meeting_confirmation:
        raise HTTPException(status_code=500, detail=f"Erro ao criar evento no Calendly: {meeting_confirmation['error']}")
    meeting_link = meeting_confirmation.get("meeting_link")
    meeting_datetime = meeting_confirmation.get("meeting_datetime")
    
    print(f"Reunião agendada! Link: {meeting_link}, Horario: {meeting_datetime}")
    
    # 2. Atualizar o card no Pipefy com as informações da reuniao
    update_success = update_pipefy_card_meeting_info(
        card_id=request.pipefy_card_id,
        meeting_link=meeting_link,
        meeting_datetime=meeting_datetime
    )
    if not update_success:
        print(f"AVISO: Reunião agendada, mas falha ao atualizar o card {request.pipefy_card_id} no Pipefy.")
    # 3. Retornar a confirmação para o frontend
    return {
        "status": "success",
        "message": "Reunião agendada com sucesso!",
        "meeting_link": meeting_link,
        "meeting_datetime": meeting_datetime
    }
    
# ======================================================
# ▶️ EXECUÇÃO LOCAL
# ======================================================

# Permite rodar o app diretamente com python main.py
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)