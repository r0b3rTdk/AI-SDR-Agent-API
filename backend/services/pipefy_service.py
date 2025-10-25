import os
import requests
from dotenv import load_dotenv

# Carregar as variaveis do arquivo .env
load_dotenv()

# Pegar as senhas do Pipefy do arquivo .env
PIPEFY_API_KEY = os.getenv("PIPEFY_API_KEY")
PIPE_ID = os.getenv("PIPE_ID")
PHASE_ID = os.getenv("PHASE_ID")

# Pegar os IDs dos 7 campos do Pipefy do arquivo .env
FIELD_NAME = os.getenv("PIPEFY_FIELD_NAME")
FIELD_EMAIL = os.getenv("PIPEFY_FIELD_EMAIL")
FIELD_COMPANY = os.getenv("PIPEFY_FIELD_COMPANY")
FIELD_NEED = os.getenv("PIPEFY_FIELD_NEED")
FIELD_INTEREST = os.getenv("PIPEFY_FIELD_INTEREST")
FIELD_MEETING_LINK = os.getenv("PIPEFY_FIELD_MEETING_LINK")
FIELD_MEETING_TIME = os.getenv("PIPEFY_FIELD_MEETING_TIME")

# O "endereço" da API do Pipefy
PIPEFY_GRAPHQL_URL = "https://api.pipefy.com/graphql"

def create_pipefy_card(lead_data: dict) -> dict:
    """
    Cria um novo card no Pipefy com os dados do lead qualificado.
    """
    print(f"Iniciando criacao de card no Pipefy para: {lead_data.get('email')}")
    
    # Pegar os dados do JSON da IA
    # Utilizacao do .get() para evitar erros de campos inexistentes
    name = lead_data.get("name", "")
    email = lead_data.get("email", "")
    company = lead_data.get("company", "")
    need = lead_data.get("need", "")
    # Converter o booleano para "Sim" ou "Nao" para String 
    interest = str(lead_data.get("interest_confirmed", False)).lower()
    
    # Agora vamos dizer para o Pipefy criar o card com esses dados
    mutation = f"""
    mutation {{
      createCard(input: {{
        pipe_id: {PIPE_ID},
        phase_id: {PHASE_ID},
        fields_attributes: [
          {{field_id: "{FIELD_NAME}", field_value: "{name}"}},
          {{field_id: "{FIELD_EMAIL}", field_value: "{email}"}},
          {{field_id: "{FIELD_COMPANY}", field_value: "{company}"}},
          {{field_id: "{FIELD_NEED}", field_value: "{need}"}},
          {{field_id: "{FIELD_INTEREST}", field_value: "{interest}"}}
        ]
      }}) {{
        card {{
          id
          title
          url
        }}
      }}
    }}
    """
    
    # Preparar a "autorizacao"
    headers = {
        "Authorization": f"Bearer {PIPEFY_API_KEY}",
        "Content-Type": "application/json"     
    }       
    
    # Preparar os dados para envio
    payload = {
        "query": mutation
    }
    
    try:
        # Envia a requisicao para a API do Pipefy
        response = requests.post(PIPEFY_GRAPHQL_URL, json=payload, headers=headers) 
        
        # Levanta um erro se a requisicao falhar (ex: API Key invalida)
        response.raise_for_status()
        
        response_json = response.json()
        
        # Verifica se o *GraphQL* retornou algum erro (ex: PIPE_ID invalido)
        if "errors" in response_json:
            print(f"Erro do Pipefy ao criar card: {response_json['errors']}")
            return {"error": response_json["errors"]} 
        card_data = response_json.get("data", {}).get("createCard", {}).get("card", {})
        print(f"Card criado com sucesso no Pipefy! ID: {card_data.get('id')}")
        return card_data
    except requests.exceptions.HTTPError as http_err:
        print(f"Erro HTTP ao chamar API Pipefy: {http_err}")
        print(f"Resposta: {response.text}")
        return {"error": str(http_err)}
    except Exception as e:
        print(f"Erro inesperado no pipefy_service: {e}")
        return {"error": str(e)}