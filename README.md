# 🤖 Verzel AI SDR Agent API

API Backend para o **Agente SDR com Inteligência Artificial**, desenvolvida como parte do desafio técnico **Verzel**.  
O objetivo é criar um agente SDR capaz de interagir com potenciais clientes, qualificar leads e automatizar o início do funil de vendas, integrando futuramente com a **OpenAI API** e ferramentas como **Pipefy** e **Calendly**.

---

## 🚀 Status do Projeto

Fase atual: **Backend com IA Real (v0.2.0)**  
Próximo passo: Adicionar lógica de qualificação de leads (memória e gatilho).

### Funcionalidades Implementadas

- Servidor web utilizando FastAPI.
- Endpoint raiz (/) para verificação de status.
- Endpoint /chat (POST) para envio e retorno de mensagens simuladas.
- Integração real com a API da OpenAI para gerar respostas inteligentes.
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
Recebe uma **única mensagem** e retorna uma **resposta real** e inteligente da IA.

Exemplo de resposta:
Mensagem: **“Olá! Tudo bem? Eu sou [seu nome], da Verzel. [...] Me conta, qual o seu nome...?”**
Acesse o endereço `http://127.0.0.1:8000/docs` para abrir a documentação interativa e testar os endpoints diretamente pelo navegador.

## 📂 Arquivos Importantes

- **main.py:** Arquivo principal da aplicação que define os endpoints e a inicialização do servidor.  
- **.env.example:** Modelo para variáveis de ambiente.  
- **.gitignore:** Define os arquivos e pastas ignorados pelo controle de versão.
- **services/openai_service.py:** Módulo que contém a lógica de "cérebro" e a comunicação com a API da OpenAI.  
- **requirements.txt:** Lista das dependências necessárias para rodar o projeto.  

---

## 🔮 Próximos Passos

- Adicionar lógica de qualificação de leads.  
- Criar endpoint /lead e integração com Pipefy API.  
- Conectar com ferramenta de agendamento (Google/Calendly).  
- Criar frontend web em React.  
- Realizar o deploy completo (Render + Vercel).

---

## 👨‍💻 Autor

**Robert Emanuel**  
Backend Developer | C, Python, FastAPI, SQL  
LinkedIn: [linkedin](https://www.linkedin.com/in/robert-emanuel/)  
GitHub: [github](https://github.com/r0b3rTdk)

---
