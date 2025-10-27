import React, { useState, useEffect, useRef } from 'react';
import './ChatWindow.css';

// Defina a URL do seu backend FastAPI
const API_URL = 'http://localhost:8000';

function ChatWindow() {
    // Estado para guardar as mensagens { role: 'user'/'assistant', content: '...' }
    const [messages, setMessages] = useState([]);
    const [inputText, setInputText] = useState('');
    const [isLoading, setIsLoading] = useState(false); // Para mostrar feedback visual

    // Referencia para rolar a lista de mensagens para baixo
    const messagesEndRef = useRef(null);
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    // Rola para baixo sempre que novas mensagens chegam
    useEffect(scrollToBottom, [messages]);

    // Funcao para quando o usuario envia uma mensagem
    const handleSendMessage = async () => {
        const userMessage = inputText.trim();
        if (userMessage === '' || isLoading) return;

    // 1. Adiciona a mensagem do usuário à lista
    const newUserMessage = { role: 'user', content: userMessage };
    const updatedMessages = [...messages, newUserMessage];
    setMessages(updatedMessages);
    setInputText('');
    setIsLoading(true);

    try {
        // 2. Monta o histórico para enviar à API
        // O backend espera [{"role": "user", "content": "..."}, ...]
        const historyForAPI = updatedMessages.map(({ role, content }) => ({ role, content }));

        // 3. Chama a API do backend
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            },
            body: JSON.stringify({ history: historyForAPI }),
        });

        if (!response.ok) {
            throw new Error(`Erro da API: ${response.statusText}`);
        }

        const data = await response.json(); // A resposta do backend vem em { response: "..." }
        let apiContent = data.response;

        // 4. Processa a resposta da API (pode ser texto ou JSON de ação)
        let assistantMessageContent = '';
        try {
            const jsonResponse = JSON.parse(apiContent);
            // É um JSON de ação? (Ex: show_slots)
            if (jsonResponse.action === 'show_slots') {
            // Formata os horários para exibição (simples por enquanto)
            assistantMessageContent = "Ótimo! Aqui estão alguns horários disponíveis:\n";
            jsonResponse.slots.forEach(slot => {
                assistantMessageContent += `- ${new Date(slot.start_time).toLocaleString()}\n`;
            });
            assistantMessageContent += "\nQual horário funciona para você?";
            // TODO DIA 7: Guardar o lead_data e pipefy_card_id para usar no /schedule
            // TODO DIA 7: Implementar a lógica para o usuário clicar em um horário e chamar /schedule
            } else if (jsonResponse.status === 'success') {
            // É a confirmação do /schedule ou do create_lead (sem interesse)
            assistantMessageContent = jsonResponse.message;
            if (jsonResponse.pipefy_card_url) {
                assistantMessageContent += `\nCard: ${jsonResponse.pipefy_card_url}`;
            }
            if (jsonResponse.meeting_link) {
                assistantMessageContent += `\nLink da Reunião: ${jsonResponse.meeting_link}`;
            }
            }
            else {
            // É um JSON, mas não um que conhecemos? Mostre como texto.
            assistantMessageContent = apiContent;
            }
        } catch (e) {
            // Não era JSON, então é texto normal da IA
            assistantMessageContent = apiContent;
        }

        // 5. Adiciona a resposta do assistente à lista
        setMessages(prevMessages => [...prevMessages, { role: 'assistant', content: assistantMessageContent }]);

        } catch (error) {
        console.error("Erro ao enviar mensagem:", error);
        // Adiciona uma mensagem de erro ao chat
        setMessages(prevMessages => [...prevMessages, { role: 'assistant', content: `Desculpe, ocorreu um erro: ${error.message}` }]);
        } finally {
        setIsLoading(false); // Libera o input
        }
    };

return (
    <div className="chat-window">
      <div className="message-list">
        {messages.map((msg, index) => (
          // Mostra cada mensagem, com classe CSS diferente para user/assistant
          <div key={index} className={`message ${msg.role}`}>
            <p><strong>{msg.role === 'user' ? 'Você' : 'Agente'}:</strong> {msg.content}</p>
          </div>
        ))}
        {/* Elemento invisível para forçar a rolagem */}
        <div ref={messagesEndRef} />
      </div>

      <div className="input-area">
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder={isLoading ? "Aguarde..." : "Digite sua mensagem..."}
          onKeyPress={(e) => { if (e.key === 'Enter') handleSendMessage(); }}
          disabled={isLoading} // Desabilita input enquanto espera resposta
        />
        <button onClick={handleSendMessage} disabled={isLoading}>
          {isLoading ? 'Enviando...' : 'Enviar'}
        </button>
      </div>
    </div>
  );
}

export default ChatWindow;
