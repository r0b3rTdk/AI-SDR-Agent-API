import os
from openai import OpenAI
from dotenv import load_dotenv

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

def generate_response(user_message: str) -> str:
    """
    Envia a mensagem do usuario para a OpenAI e retorna a resposta da IA
    """
    
    # Aqui fica o "Prompt do Sistema", onde defini a personalidade e objetivos da IA
    system_prompt = """
    Você é um agente SDR (Sales Development Representative) da Verzel, 
    uma empresa de tecnologia e inovação.
    
    Seu objetivo principal é conversar naturalmente com o cliente, 
    qualificá-lo e agendar uma reunião.
    
    Para qualificar, você precisa coletar 4 informações:
    1. Nome
    2. E-mail
    3. Nome da Empresa
    4. A necessidade ou desafio que o cliente enfrenta (o "interesse").
    
    Seja sempre amigável, profissional e direto ao ponto. 
    Não invente informações sobre a Verzel.
    Comece a conversa se apresentando brevemente.
    """
    
    try:
        # Aqui e a chamada real
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7 # Controla a criatividade (0.0 = robotico, 1.0 = criativo)
        )
    
        # Extrair e retorna de texto da IA
        ai_response = response.choices[0].message.content
        return ai_response
    except Exception as e:
        print(f"Erro ao gerar resposta da OpenAI: {e}")
        return "Desculpe, ocorreu um erro ao processar sua solicitação."