import React, { useState, useEffect, useRef } from 'react';
import './ChatWindow.css';

// Defina a URL do seu backend FastAPI
const API_URL = 'https://verzel-sdr-backend.onrender.com'; // <-- SUA URL DO RENDER AQUI
function ChatWindow() {
    // Estado para guardar as mensagens { role: 'user'/'assistant', content: '...' }
    const [messages, setMessages] = useState([]);
    const [inputText, setInputText] = useState('');
    const [isLoading, setIsLoading] = useState(false); // Para mostrar feedback visual

    // Estados para guardar os slots disponiveis
    const [availableSlots, setAvailableSlots] = useState([]); // Guarda os horarios recebidos
    const [currentLeadData, setCurrentLeadData] = useState(null); // Guarda os dados do lead para agendamento
    const [currentPipefyCardId, setCurrentPipefyCardId] = useState(null); // Guarda o ID do card para agendamento

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
      setAvailableSlots([]); // Limpa slots antigos ao enviar nova mensagem

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

        if (!response.ok) throw new Error(`Erro da API: ${response.statusText}`);
        const data = await response.json(); // A resposta do backend vem em { response: "..." }
        let apiContent = data.response;

        // 4. Processa a resposta da API (pode ser texto ou JSON de ação)
        let messageToAdd = null; // Prepara a mensagem a ser adicionada

        try {
          const jsonResponse = JSON.parse(apiContent);

          // É um JSON de ação? (Ex: show_slots)
          if (jsonResponse.action === 'show_slots') {
            // Formata os horários para exibição (simples por enquanto)
            const introMessage = "Ótimo! Aqui estão alguns horários disponíveis. Clique em um para agendar:";            // Guarda os dados para usar no agendamento
            setAvailableSlots(jsonResponse.slots || []);
            setCurrentLeadData(jsonResponse.lead_data || null);
            setCurrentPipefyCardId(jsonResponse.pipefy_card_id || null);
            messageToAdd = { role: 'assistant', content: introMessage }; // Adiciona so a intro

          } else if (jsonResponse.status === 'success') {
            // É a confirmação do /schedule ou do create_lead (agendamento ou lead sem interesse)
            let confirmationText = jsonResponse.message;
            if (jsonResponse.pipefy_card_url) confirmationText += `\nCard: ${jsonResponse.pipefy_card_url}`;
            if (jsonResponse.meeting_link) confirmationText += `\nLink da Reunião: ${jsonResponse.meeting_link}`;
            messageToAdd = { role: 'assistant', content: confirmationText };

          } else {
            // É um JSON, mas não um que conhecemos? Mostre como texto.
            messageToAdd = { role: 'assistant', content: apiContent };
          }

        } catch (e) {
          // Não era JSON, então é texto normal da IA
          messageToAdd = { role: 'assistant', content: apiContent };
        }

        // Adiciona a mensagem determinada (se houver) ao estado
        if (messageToAdd) {
          setMessages(prev => [...prev, messageToAdd]);
        }

      } catch (error) {
        console.error("Erro ao enviar mensagem:", error);
        // Adiciona uma mensagem de erro ao chat
        setMessages(prevMessages => [...prevMessages, { role: 'assistant', content: `Desculpe, ocorreu um erro: ${error.message}` }]);
      } finally {
          setIsLoading(false); // Libera o input
      }
    };
    
    //Funcao para agendamento
    const handleSchedule = async (slot) => {
      if (!currentLeadData || !currentPipefyCardId || isLoading) return;

      console.log("Agendando horário:", slot);
      setIsLoading(true);
      setAvailableSlots([]); // Remove os botoes de horerio

      // Adiciona uma mensagem de feedback
      setMessages(prev => [...prev, { role: 'assistant', content: `Ok, agendando para ${new Date(slot.start_time).toLocaleString()}...` }]);

      try {
        const response = await fetch(`${API_URL}/schedule`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            slot_info: slot,
            lead_data: currentLeadData,
            pipefy_card_id: currentPipefyCardId
          }),
        });

        if (!response.ok) throw new Error(`Erro ao agendar: ${response.statusText}`);
        const confirmationData = await response.json();

        // Adiciona a mensagem de confirmacao final
        let confirmationMessage = confirmationData.message || "Agendamento confirmado!";
        if(confirmationData.meeting_link) confirmationMessage += `\nLink: ${confirmationData.meeting_link}`;
        if(confirmationData.meeting_datetime) confirmationMessage += `\nData: ${new Date(confirmationData.meeting_datetime).toLocaleString()}`;

        setMessages(prev => [...prev, { role: 'assistant', content: confirmationMessage }]);

      } catch (error) {
        console.error("Erro ao agendar:", error);
        setMessages(prev => [...prev, { role: 'assistant', content: `Desculpe, erro ao agendar: ${error.message}` }]);
      } finally {
        setIsLoading(false);
        // Limpa os dados do lead atual para evitar reagendamento acidental
        setCurrentLeadData(null);
        setCurrentPipefyCardId(null);
      }
    };

return (
    <div className="chat-window">
      <div className="message-list">
        {messages.map((msg, index) => (
          // Mostra cada mensagem, com classe CSS diferente para user/assistant
          <div key={index} className={`message ${msg.role}`}>
            <p><strong>{msg.role === 'user' ? 'Você' : 'Agente'}:</strong></p>
            {/* Renderiza quebras de linha que vêm da IA ou dos slots */}
            {msg.content.split('\n').map((line, lineIndex) => (
              <p key={lineIndex} style={{ margin: '0 0 5px 0' }}>{line}</p>
              ))}
          </div>
        ))}
        {/* --- RENDERIZAÇÃO DOS BOTOES DE HORARIO --- */}
        {availableSlots.length > 0 && (
          <div className="message assistant slots-container">
             <p><strong>Agente:</strong> Escolha um horário:</p>
            {availableSlots.map((slot, index) => (
              <button
                key={index}
                className="slot-button"
                onClick={() => handleSchedule(slot)}
                disabled={isLoading}
              >
                {new Date(slot.start_time).toLocaleString()}
              </button>
            ))}
          </div>
        )}

        {/* Elemento invisivel para forcar a rolagem */}
        <div ref={messagesEndRef} />
      </div>

      <div className="input-area">
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder={isLoading ? "Aguarde..." : "Digite sua mensagem..."}
          onKeyPress={(e) => { if (e.key === 'Enter' && !isLoading) handleSendMessage(); }}
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
