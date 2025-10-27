# 🤖 Verzel AI SDR Agent API

API Backend para o **Agente SDR com Inteligência Artificial**, desenvolvida como parte do desafio técnico **Verzel**.  
O objetivo é criar um agente SDR capaz de interagir com potenciais clientes, qualificar leads e automatizar o início do funil de vendas, integrando futuramente com a **OpenAI API** e ferramentas como **Pipefy** e **Calendly**.

---

## 🚀 Status do Projeto

Fase atual: **Backend com Agendamento (v0.6.0)**  
Próximo passo: Realizar o deploy completo (Render + Vercel).

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
- Frontend (Webchat) básico criado com React + Vite.
- Interface de chat funcional: exibe histórico, permite envio de mensagens.
- Conexão Frontend <-> Backend: O chat envia o histórico para a API /chat e exibe a resposta da IA.
- Tratamento Básico de Respostas JSON: Frontend exibe os horários (show_slots) formatados.
- CORS configurado no backend para permitir a comunicação com o frontend local.
- Estrutura de ambiente virtual (venv) configurada.
- Arquivo .env.example para gerenciamento de chaves e variáveis de ambiente.
- Documentação interativa gerada automaticamente em /docs (Swagger UI).

---

## 🧱 Estrutura do Projeto

O projeto é organizado em duas pastas principais para facilitar manutenção e escalabilidade:
- `backend/`: Contém a API RESTful desenvolvida com Python e FastAPI, responsável pela orquestração dos serviços (IA, Pipefy, Calendly).
- `frontend/`: Contém a interface do Webchat desenvolvida com React e Vite, responsável pela interação com o usuário.

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
- **React** — Biblioteca JavaScript para construir a interface do usuário.
- **Vite** — Ferramenta de build rápida para o frontend.
- **CSS** — Para estilização do chat.
- **Fetch API** — Para comunicação do frontend com o backend.

---

## ⚙️ Configuração e Execução Local

Siga estas instruções para configurar e rodar o projeto completo na sua máquina.

**Backend (API FastAPI):**

1.  Acesse a pasta `backend/`.
2.  Crie e ative um ambiente virtual Python:
    ```bash
    py -m venv venv
    .\venv\Scripts\activate
    ```
3.  Instale as dependências Python:
    ```bash
    pip install -r requirements.txt
    ```
4.  Crie o arquivo `.env` copiando o `.env.example`.
5.  Preencha o `.env` com suas chaves de API (OpenAI, Pipefy, Calendly) e os IDs do Pipefy (Pipe, Fase, Campos).
6.  Execute o servidor backend:
    ```bash
    uvicorn main:app --reload
    ```
    A API estará disponível em `http://localhost:8000`.

**Frontend (Webchat React):**

1.  Acesse a pasta `frontend/`.
2.  Instale as dependências JavaScript:
    ```bash
    npm install
    ```
3.  Execute o servidor de desenvolvimento do frontend:
    ```bash
    npm run dev
    ```
4.  Acesse o chat no seu navegador no endereço fornecido (geralmente `http://localhost:5173`).

---

## 🧪 Testando a Aplicação Completa

Com o **Backend** (`uvicorn`) e o **Frontend** (`npm run dev`) rodando simultaneamente:

1.  Acesse o Webchat no navegador (ex: `http://localhost:5173`).
2.  Inicie uma conversa digitando uma mensagem (ex: "Olá") e clicando em "Enviar".
3.  Siga o fluxo de qualificação respondendo às perguntas do agente (nome, e-mail, empresa, necessidade).
4.  Confirme o interesse quando o agente perguntar ("Sim").
5.  O chat deve exibir os horários disponíveis (simulados) retornados pelo backend.
6.  **Validação Backend:** Verifique no terminal do `uvicorn` se o gatilho da IA foi detectado (`GATILHO DETECTADO...`) e se o card foi criado no Pipefy (`Card criado com sucesso...`).
7.  **Validação Frontend:** Verifique se a conversa flui corretamente no chat, exibindo suas mensagens e as respostas do agente, incluindo a lista de horários no final.


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

**Backend (`backend/`):**

-   `main.py`: Arquivo principal da API FastAPI, orquestra as chamadas aos serviços.
-   `services/openai_service.py`: Módulo para interação com a API da OpenAI (cérebro da IA).
-   `services/pipefy_service.py`: Módulo para criar e atualizar cards no Pipefy via GraphQL.
-   `services/calendar_service.py`: Módulo para buscar horários e agendar reuniões (simulado) com Calendly.
-   `.env`: Arquivo (ignorado pelo Git) com todas as chaves de API e IDs.
-   `.env.example`: Modelo do arquivo `.env`.
-   `requirements.txt`: Lista de dependências Python (`fastapi`, `openai`, `requests`, etc.).

**Frontend (`frontend/`):**

-   `src/App.jsx`: Componente raiz da aplicação React.
-   `src/components/ChatWindow.jsx`: Componente principal que implementa a interface e a lógica do chat.
-   `src/components/ChatWindow.css`: Arquivo de estilização para o componente de chat.
-   `package.json`: Arquivo que define o projeto Node.js e suas dependências JavaScript (`react`, `vite`).
-   `vite.config.js`: Arquivo de configuração do Vite (geralmente não precisa mexer).

---

## 🔮 Próximos Passos

- **(Próximo Passo)** Implementar a seleção de horário e chamada ao `/schedule` no frontend.
- Realizar o deploy completo (Render + Vercel).

---

## 👨‍💻 Autor

**Robert Emanuel**  
Backend Developer | C, Python, FastAPI, SQL  
LinkedIn: [linkedin](https://www.linkedin.com/in/robert-emanuel/)  
GitHub: [github](https://github.com/r0b3rTdk)

---
