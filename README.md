# 🤖 Verzel AI SDR Agent API

API Backend para o **Agente SDR com Inteligência Artificial**, desenvolvida como parte do desafio técnico **Verzel**.  
O objetivo é criar um agente SDR capaz de interagir com potenciais clientes, qualificar leads e automatizar o início do funil de vendas, integrando futuramente com a **OpenAI API** e ferramentas como **Pipefy** e **Calendly**.

---

## 🚀 Status do Projeto

Fase atual: **Backend com Agendamento (v0.5.0)**  
Próximo passo: Criar frontend web em React.

### Funcionalidades Implementadas

- Servidor web utilizando FastAPI.
- Endpoint raiz (/) para verificação de status.
- Endpoint /chat (POST) para envio e retorno de mensagens.
- Integração real com a API da OpenAI para gerar respostas inteligentes.
- Implementação de memória de conversa (o backend agora lida com um histórico).
- Lógica de "gatilho" de qualificação (IA retorna um JSON com os dados do lead).
- Integração real com a API GraphQL do Pipefy.
- Criação automática de cards no funil de "Pré-vendas" ao detectar o gatilho da IA.
- Integração (simulada) com a API do Calendly para buscar horários disponíveis.
- Novo endpoint /schedule para receber a escolha do usuário.
- Agendamento (simulado) de reunião via calendar_service.
- Atualização automática do card no Pipefy com o link e data/hora da reunião agendada.
- Estrutura de ambiente virtual (venv) configurada.
- Arquivo .env.example para gerenciamento de chaves e variáveis de ambiente.
- Documentação interativa gerada automaticamente em /docs (Swagger UI).

---

## 🧱 Estrutura do Projeto

O projeto é organizado em uma estrutura simples e modular para facilitar manutenção e escalabilidade.  
Na pasta backend ficam todos os arquivos principais do servidor, incluindo o arquivo principal `main.py`, variáveis de ambiente e dependências.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.x** — Linguagem principal do backend.  
- **FastAPI** — Framework web rápido e moderno.  
- **Uvicorn** — Servidor ASGI para execução do FastAPI.  
- **Pydantic** — Modelagem e validação de dados.  
- **python-dotenv** — Leitura de variáveis de ambiente.  
- **Swagger UI** — Interface interativa de teste de endpoints.
- **OpenAI** — Para geração de respostas do agente de IA.
- **Requests** — Para realizar chamadas HTTP para a API GraphQL do Pipefy.

---

## ⚙️ Configuração e Execução Local

1. Clone o repositório do projeto e acesse a pasta backend.  
2. Crie e ative um ambiente virtual (venv).  
3. Instale as dependências principais (FastAPI, Uvicorn e python-dotenv).  
4. Crie o arquivo `.env` com base no `.env.example` e adicione sua chave da OpenAI.  
5. Execute o servidor com o comando para inicialização e acesse no navegador em `http://127.0.0.1:8000`.

Após iniciado, o terminal exibirá a mensagem indicando que a API está online.

---

## 🧪 Testando a API

A API conta com dois endpoints principais que podem ser testados via Swagger UI.

### Endpoint Raiz (/)
Verifica se o servidor está online.  
O retorno esperado é uma mensagem confirmando o status ativo da API.

Exemplo de resposta:  
Mensagem: **“AI SDR Agent API - online”**

### Endpoint de Chat (/chat)
Recebe um **histórico de mensagens** e, ao final da qualificação:
1. Cria o card no Pipefy
2. Se o interesse for confirmado, busca e retorna os horários disponíveis (via calendar_service).

Exemplo de resposta (se interesse confirmado): 
Mensagem: `{"action": "show_slots", "slots": [...], "lead_data": {...}, "pipefy_card_id": "..."}`

### Endpoint de Agendamento (/schedule)
Recebe o **slot_info** (horário escolhido pelo usuário), os **lead_data** (dados do lead coletados) e o **pipefy_card_id** (ID do card criado no Pipefy).
1. Chama o calendar_service para agendar (simular) a reunião no Calendly.
2. Chama o pipefy_service para **atualizar o card correspondente no Pipefy** com o link (`meeting_link`) e a data/hora (`meeting_datetime`) da reunião agendada.

Exemplo de resposta (em caso de sucesso):
Mensagem: `{"status": "success", "message": "Reunião agendada com sucesso!", "meeting_link": "https://calendly.com/...", "meeting_datetime": "2025-10-27T..."}`

Acesse o endereço `http://127.0.0.1:8000/docs` para abrir a documentação interativa e testar os endpoints diretamente pelo navegador.

---

## 📂 Arquivos Importantes

- **main.py:** Arquivo principal da aplicação que define os endpoints, a inicialização do servidor e **orquestra as chamadas** para os serviços de IA, Pipefy e Calendly.
- **.env.example:** Modelo para variáveis de ambiente, **incluindo chaves da OpenAI, Pipefy e Calendly, além dos IDs do Pipefy**.
- **.gitignore:** Define os arquivos e pastas ignorados pelo controle de versão.
- **services/openai_service.py:** Módulo que contém a lógica de "cérebro", o prompt de qualificação e a lógica do "gatilho" JSON.
- **services/pipefy_service.py:** Módulo que gerencia a autenticação e as queries GraphQL para **criar e atualizar cards** no Pipefy.
- **services/calendar_service.py:** **Novo módulo** que gerencia a busca de horários e o agendamento (simulado) via API do Calendly.
- **requirements.txt:** Lista das dependências necessárias (**incluindo `fastapi`, `openai`, `requests`**).

---

## 🔮 Próximos Passos

- Criar frontend web em React.  
- Realizar o deploy completo (Render + Vercel).

---

## 👨‍💻 Autor

**Robert Emanuel**  
Backend Developer | C, Python, FastAPI, SQL  
LinkedIn: [linkedin](https://www.linkedin.com/in/robert-emanuel/)  
GitHub: [github](https://github.com/r0b3rTdk)

---
