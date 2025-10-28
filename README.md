# 🤖 Verzel AI SDR Agent API

API Backend para o **Agente SDR com Inteligência Artificial**, desenvolvida como parte do desafio técnico **Verzel**.  
O objetivo é criar um agente SDR capaz de interagir com potenciais clientes, qualificar leads e automatizar o início do funil de vendas, integrando futuramente com a **OpenAI API** e ferramentas como **Pipefy** e **Calendly**.

---

## 🚀 Aplicação Online (Deploy)

A aplicação completa está disponível publicamente nos seguintes links:

* **Webchat (Frontend - Vercel):** [https://ai-sdr-agent-api.vercel.app/](https://ai-sdr-agent-api.vercel.app/)
* **API (Backend - Render):** [https://verzel-sdr-backend.onrender.com/](https://verzel-sdr-backend.onrender.com/)

*(**Nota:** O plano gratuito do Render pode colocar o backend para "dormir" após inatividade. O primeiro acesso pode levar alguns segundos extras para "acordar" o servidor.)*

---

## 🚀 Status do Projeto

Fase atual: **Aplicação Completa e Deployada (v1.0.0)**

### Funcionalidades Implementadas

- Servidor web utilizando FastAPI.
- Frontend (Webchat) interativo criado com React + Vite.
- Endpoint raiz (`/`) para verificação de status da API
- Endpoint `/chat` (POST) que processa um histórico de mensagens via OpenAI.- Implementação de memória de conversa (o backend agora lida com um histórico).
- Implementação de memória de conversa no agente.
- Lógica de "gatilho" de qualificação (IA retorna um JSON com os dados do lead).
- Integração real com a API GraphQL do Pipefy.
- Criação automática de cards no funil de "Pré-vendas" ao detectar o gatilho da IA.
- Integração com a API do Calendly **(simulada devido a limitações da API gratuita para busca/criação programática)**
- Endpoint `/schedule` (POST) para receber a escolha de horário do usuário.
- Agendamento **(simulado)** de reunião via `calendar_service`
- Atualização automática do card no Pipefy com o link e data/hora da reunião agendada.
- Interface de chat funcional: exibe histórico, permite envio de mensagens, mostra botões de horário
- Conexão Frontend <-> Backend configurada com CORS para produção
- Lógica completa de agendamento no Frontend
- Estrutura de ambiente virtual (`venv`) para o backend.
- Gerenciamento seguro de chaves com arquivos `.env`
- Documentação interativa da API via Swagger UI (`/docs`).
- Deploy do Backend no Render e Frontend no Vercel

---

## 🧱 Estrutura do Projeto

O projeto é organizado em duas pastas principais para facilitar manutenção e escalabilidade:
- `backend/`: Contém a API RESTful desenvolvida com Python e FastAPI, responsável pela orquestração dos serviços (IA, Pipefy, Calendly).
- `frontend/`: Contém a interface do Webchat desenvolvida com React e Vite, responsável pela interação com o usuário.
- `docs/`: Contém a documentação detalhada (Estudo de Caso) e imagens.

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3.x, FastAPI, Uvicorn, Pydantic, python-dotenv, OpenAI, Requests.
* **Frontend:** React, Vite, CSS, Fetch API.
* **Infraestrutura:** Render (Backend), Vercel (Frontend), GitHub (Versionamento).
* **Ferramentas Externas:** Pipefy (CRM), Calendly (Agenda - Simulado).

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

1.  **Acesse o Webchat:** Abra seu navegador no endereço fornecido pelo `npm run dev` (geralmente `http://localhost:5173`).
2.  **Inicie a Conversa:** Digite uma mensagem inicial (ex: "Olá") e clique em "Enviar".
3.  **Siga o Fluxo de Qualificação:** Responda às perguntas do agente (nome, e-mail, empresa, necessidade).
4.  **Confirme o Interesse:** Quando o agente fizer a "pergunta direta", responda positivamente (ex: "Sim", "Tenho interesse").
5.  **Verifique os Horários:** O chat deve exibir a mensagem "Escolha um horário:" seguida por **botões clicáveis** com as datas/horas disponíveis (simuladas).
    * *Validação (Backend):* Neste ponto, verifique no terminal do `uvicorn` se o gatilho `create_lead` foi detectado e se o card inicial foi criado no Pipefy (`Card criado com sucesso...`).
6.  **Clique em um Horário:** Selecione um dos botões de horário disponíveis.
7.  **Verifique a Confirmação:** O chat deve exibir a mensagem "Ok, agendando..." seguida pela confirmação final com o link da reunião (simulado) e a data/hora escolhida.
8.  **Validações Finais:**
    * **Backend:** Verifique no terminal do `uvicorn` se o endpoint `/schedule` foi chamado com sucesso e se o log indica que o card no Pipefy foi atualizado (`Card ... atualizado com sucesso...`).
    * **Frontend:** Confirme que todo o fluxo da conversa, desde o início até a confirmação do agendamento, foi exibido corretamente na interface do chat.
    * **Pipefy:** Abra o card correspondente no seu funil do Pipefy (pelo ID ou pelo título) e verifique se os campos `meeting_link` e `meeting_datetime` foram preenchidos corretamente.


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
-   `src/components/ChatWindow.jsx`: Componente principal que implementa a interface, a lógica do chat, a exibição dos horários e a chamada para o agendamento (/schedule).
-   `src/components/ChatWindow.css`: Arquivo de estilização para o componente de chat.
-   `package.json`: Arquivo que define o projeto Node.js e suas dependências JavaScript (`react`, `vite`).
-   `vite.config.js`: Arquivo de configuração do Vite (geralmente não precisa mexer).

**Documentação (`docs/`):**

* `ESTUDO_DE_CASO.md`: Documentação detalhada do projeto (ou `Verzel_AI_SDR_Agent_Case.md`).
* Arquivos de imagem dos diagramas e prints.

---

## 🔮 Próximos Passos

*(Melhorias futuras poderiam incluir: integração real com Calendly API se viável, tratamento mais robusto de erros, testes automatizados, interface de usuário mais elaborada).*

---

## 👨‍💻 Autor

**Robert Emanuel**  
Backend Developer | C, Python, FastAPI, SQL  
LinkedIn: [linkedin](https://www.linkedin.com/in/robert-emanuel/)  
GitHub: [github](https://github.com/r0b3rTdk)

---
