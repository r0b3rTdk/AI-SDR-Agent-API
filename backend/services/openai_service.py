import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict

# Carregar as variaveis do arquivo .env
load_dotenv()

# Pegar a chave de API do arquivo .env
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    # Garantir que o app falhe se a chave nao for encontrada
    raise ValueError("OPENAI_API_KEY nao encontrada no arquivo .env")

# Inicializar o cliente da OpenAI com a sua chave
client = OpenAI(api_key=api_key)

# Pegar o modelo do .env, ou usa um padrao se nao for definido
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

def generate_response(history: List[Dict[str, str]]) -> str:
    """
    Envia o HISTORICO da conversa para a OpenAI e retorna a resposta da IA.
    """
    
    # Aqui fica o "Prompt do Sistema", onde defini a personalidade e objetivos da IA
    system_prompt = {
        "role": "system",
        "content": """
        Você é um agente SDR (Sales Development Representative) da Verzel, 
        uma empresa de tecnologia e inovação.
        Seu objetivo é conversar naturalmente e coletar 4 informações:
        1. Nome
        2. E-mail
        3. Nome da Empresa
        4. A necessidade ou desafio que o cliente enfrenta (need/dor).
        
        Seja sempre amigável, profissional. Siga o script:
        1. Apresente-se e ao serviço.
        2. Faça perguntas de descoberta para coletar as 4 informações.
        3. Faça a "pergunta direta" (ex: "Você gostaria de seguir com uma conversa...?") 
        
        IMPORTANTE: Assim que você tiver coletado com sucesso TODAS as 4 informações (nome, e-mail, empresa, necessidade),
        E o cliente confirmar interesse na "pergunta direta", você DEVE responder APENAS com
        um JSON valido, e nada mais.
        
        O JSON deve ter o seguinte formato:
        {
            "action": "create_lead",
            "data": {
                "name": "Nome coletado",
                "email": "email@coletado.com",
                "company": "Empresa Coletada",
                "need": "Necessidade coletada",
                interest_confirmed: true
            }
        }
        
        Se o cliente NAO confirmar interesse na "pergunta direta", responda educadamente,
        agradeca e retorne um JSON similar com "interest_confirmed": false.
        
        Enquanto voce nao tiver os 4 dados E a resposta da "pergunta direta",
        continue a conversa normalmente,
        """
    }
    
    # Montar a lista de mensagens, comecando pelo prompt do sistema
    messages_to_send = [system_prompt] + history
    
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages_to_send,
            temperature=0.7 # Controla a criatividade (0.0 = robotico, 1.0 = criativo)
        )
    
        # Extrair e retorna de texto da IA
        ai_response = response.choices[0].message.content
        return ai_response
    except Exception as e:
        print(f"Erro ao gerar resposta da OpenAI: {e}")
        return "Desculpe, ocorreu um erro ao processar sua solicitação."