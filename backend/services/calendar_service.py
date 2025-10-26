import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import List, Dict

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

CALENDLY_API_KEY = os.getenv("CALENDLY_API_KEY")
CALENDLY_API_URL = "https://api.calendly.com"

# --- Funcoes Auxiliares ----

def _get_calendly_headers():
    """Retorna os cabeçalhos de autorização para a API do Calendly."""
    return {
        "Authorization": f"Bearer {CALENDLY_API_KEY}",
        "Content-Type": "application/json"
    }

def _get_user_url():
    """Obtém a URL do usuário atual no Calendly."""
    try:
        response = requests.get(f"{CALENDLY_API_URL}/users/me", headers=_get_calendly_headers())
        response.raise_for_status() # Lança um erro se a requisição falhar
        return response.json()["resource"]["uri"]
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter URL do usuário no Calendly: {e}")
        return None
    
def _get_event_type_uri(user_uri: str):
    """Obtém o URI do primeiro tipo de evento ativo do usuário."""
    if not user_uri:
        return None
    try:
        # Busca por tipos de evento ativos do usuário, limitando a 1 resultado
        params = {"user": user_uri, "active": "true", "count": 1}
        response = requests.get(f"{CALENDLY_API_URL}/event_types", headers=_get_calendly_headers(), params=params)
        response.raise_for_status()    
        event_types = response.json()["collection"]
        if event_types:
            return event_types[0]["uri"]
        else:
            print("Nenhum tipo de evento ativo encontrado no Calendly.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter tipos de evento no Calendly: {e}")
        return None
    
# --- Funcoes Principais do Servico ---

def get_available_slots() -> List:
    """
    Busca horários disponíveis no Calendly para os proximos 7 dias.
    """
    print("Buscando horários disponíveis no Calendly...")
    user_uri = _get_user_url()
    event_type_uri = _get_event_type_uri(user_uri)

    if not event_type_uri:
        return {"error": "Não foi possível obter o tipo de evento no Calendly."}
    
    # Definir o intervalo de tempo: de agora ate 7 dias no futuro
    start_time = datetime.utcnow().isoformat() + "Z"
    end_time = (datetime.utcnow() + timedelta(days=7)).isoformat() + "Z"
    
    # NOTA IMPORTANTE SOBRE A API DO CALENDLY:
    # A API gratuita do Calendly ao qual estou usando, NAO permite buscar horarios disponiveis diretamente.
    # Vou SIMULAR a busca de horarios por enquanto.
    
    # SIMULAÇÃO:
    print("Simulando busca de horarios (API do Calendly tem limitacoes no plano gratuito)...")
    mock_slots = [
        {"start_time": (datetime.utcnow() + timedelta(days=1, hours=14)).isoformat() + "Z", "schedulable_url": f"{CALENDLY_API_URL}/scheduled_links/simulado1"},
        {"start_time": (datetime.utcnow() + timedelta(days=1, hours=15)).isoformat() + "Z", "schedulable_url": f"{CALENDLY_API_URL}/scheduled_links/simulado2"},
        {"start_time": (datetime.utcnow() + timedelta(days=2, hours=10)).isoformat() + "Z", "schedulable_url": f"{CALENDLY_API_URL}/scheduled_links/simulado3"}
    ]
    
    # Em um cenário real, chamaria um endpoint como:
    # params = {"event_type": event_type_uri, "start_time": start_time, "end_time": end_time}
    # response = requests.get(f"{CALENDLY_API_URL}/user_availability_schedules?user={user_uri}", headers=_get_calendly_headers(), params=params)
    # slots = response.json().get("collection", [])
    
    print(f"Horários simulados encontrados: {len(mock_slots)}")
    return mock_slots

def create_meeting(slot_info: dict, lead_data: dict) -> dict:
    """
    Agenda uma reunião usando a API do Calendly.
    Requer nome e e-mail do lead.
    """
    name = lead_data.get("name", "Lead Interessado")
    email = lead_data.get("email")
    
    if not email:
        return {"error": "E-mail é obrigatório para agendar a reunião."}
    
    # Em um cenário real, usariamos a informacao do slot escolhido e os dados do lead para chamar o endpoint
    scheduling_url = slot_info.get("schedulable_url") # assumimos que o slot tem 
    start_time_str = slot_info.get("start_time")
    
    # SIMULAÇÃO:
    print(f"Simulando agendamento para {name} ({email}) no horário {start_time_str}...")
    mock_meeting_link = f"https://calendly.com/seu-usuario/reuniao-agendada-{os.urandom(4).hex()}"
    mock_confirmation = {
        "event_uri": f"calendly:event:simulado_{os.urandom(4).hex()}",  # ID ficticio do evento
        "meeting_link": mock_meeting_link,                              # Link fictico
        "meeting_datetime": start_time_str                             # Data/Hora do agendamento
    }
    
    # A chamada real seria algo como:
    # event_type_uri_real = _get_event_type_uri(_get_user_uri())
    # payload = {
    #     "scheduling_link": scheduling_url, # Ou o ID do slot
    #     "invitee_email": email,
    #     "invitee_name": name,
    #     "start_time": start_time_str
    # }
    # response = requests.post(f"{CALENDLY_API_URL}/scheduled_events", headers=_get_calendly_headers(), json=payload)
    # confirmation_data = response.json().get("resource", {})
    
    print(f"Agendamento simulado criado. Link da reunião: {mock_meeting_link}")
    return mock_confirmation