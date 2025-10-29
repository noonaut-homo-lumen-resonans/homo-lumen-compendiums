import React, { useState, useRef, useEffect, useCallback } from 'react';
import { ChatMessage, ChatbotState } from '../types';
import { GEMINI_API_MODEL_TEXT, AI_DISCLAIMER } from '../constants';
import { sendMessageToGeminiChat } from '../services/geminiService';
import Button from '../components/common/Button';
import { PaperAirplaneIcon, UserCircleIcon, ChatBubbleLeftEllipsisIcon, InformationCircleIcon } from '../components/icons';
import LoadingSpinner from '../components/common/LoadingSpinner';


const ChatbotPage: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState<string>('');
  const [pageState, setPageState] = useState<ChatbotState>(ChatbotState.IDLE);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);
  
  const initialMessage = useCallback(() => {
     setMessages([
      {
        id: 'initial-bot-message',
        text: 'Hei, jeg er Lira. Jeg kan forklare begreper, foreslå neste steg og peke deg til riktige skjema. Jeg gir ikke juridiske råd, men jeg gjør det enklere å forstå valgene dine.',
        sender: 'bot',
        timestamp: Date.now(),
      }
    ]);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  },[]);

  useEffect(() => {
    initialMessage();
  }, [initialMessage]);


  const handleSend = async (predefinedMessage?: string) => {
    const messageToSend = predefinedMessage || input;
    if (!messageToSend.trim()) return;

    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      text: messageToSend,
      sender: 'user',
      timestamp: Date.now(),
    };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setPageState(ChatbotState.LOADING);

    const botLoadingMessage: ChatMessage = {
      id: `bot-loading-${Date.now()}`,
      text: '',
      sender: 'bot',
      timestamp: Date.now(),
      isLoading: true,
    };
    setMessages(prev => [...prev, botLoadingMessage]);

    try {
      // Construct history for Gemini chat
      // `messages` state already includes the latest userMessage
      const historyForApi = messages
        .filter(msg => !msg.isLoading && msg.id !== userMessage.id) // Exclude previous loading and current user message
        .map(msg => ({
          role: msg.sender === 'user' ? 'user' : 'model',
          parts: [{ text: msg.text }],
        }));
      
      const systemInstruction = `
        Du er en hjelpsom og vennlig AI-chatbot for applikasjonen NAV-Losen, kalt Lira. Ditt formål er å svare på spørsmål relatert til NAV (Norges Arbeids- og Velferdsetat), 
        inkludert ytelser, søknadsprosesser, rettigheter og plikter. Svar på norsk.
        Vær tydelig, konsis og bruk et enkelt språk. Unngå å gi personlig rådgivning eller garantere utfall. 
        Henvis brukeren til nav.no eller direkte kontakt med NAV for offisiell informasjon og individuelle saker.
        Inkluder alltid en ansvarsfraskrivelse om at du er en AI og at informasjonen bør verifiseres.
        Hvis du bruker informasjon fra Google Search (om aktuelt), list opp kilder tydelig.
      `;

      // Pass current input (userMessage.text) and the prepared history
      const result = await sendMessageToGeminiChat(userMessage.text, historyForApi, systemInstruction);

      setMessages(prev => prev.filter(msg => msg.id !== botLoadingMessage.id)); // Remove loading
      const botMessage: ChatMessage = {
        id: `bot-${Date.now()}`,
        text: result.text,
        sender: 'bot',
        timestamp: Date.now(),
        sources: result.sources,
      };
      setMessages(prev => [...prev, botMessage]);
      setPageState(ChatbotState.IDLE);

    } catch (err: any) {
      console.error("Error sending message:", err);
      setMessages(prev => prev.filter(msg => msg.id !== botLoadingMessage.id)); // Remove loading
      const errorMessage: ChatMessage = {
        id: `bot-error-${Date.now()}`,
        text: 'Noe gikk galt. Prøv igjen, eller trykk "Snakk med veileder" for andre alternativer.',
        sender: 'bot',
        timestamp: Date.now(),
        error: err.message || 'Ukjent feil',
      };
      setMessages(prev => [...prev, errorMessage]);
      setPageState(ChatbotState.ERROR);
    }
  };
  
  const quickActionButtons = [
      "Forklar 'vedtak' i klarspråk",
      "Hva gjør jeg nå?",
      "Finn skjema for dagpenger",
      "Hvordan kontakter jeg en menneskelig veileder?",
  ];

  return (
    <div className="flex flex-col h-[calc(100vh-10rem)] bg-white rounded-lg shadow">
      <header className="p-4 border-b flex items-center">
        <ChatBubbleLeftEllipsisIcon className="w-6 h-6 text-primary mr-2" />
        <h2 className="text-lg font-semibold text-darkgray">Lira - NAV-Losen Chatbot</h2>
      </header>

      <div className="flex-1 p-4 space-y-4 overflow-y-auto">
        {messages.map((msg) => (
          <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`flex items-end max-w-lg ${msg.sender === 'user' ? 'flex-row-reverse' : ''}`}>
              {msg.sender === 'bot' && <ChatBubbleLeftEllipsisIcon className="w-8 h-8 text-secondary mr-2 mb-1 self-start flex-shrink-0" />}
              {msg.sender === 'user' && <UserCircleIcon className="w-8 h-8 text-primary ml-2 mb-1 self-start flex-shrink-0" />}
              <div
                className={`p-3 rounded-xl ${
                  msg.sender === 'user' ? 'bg-primary text-white' : 'bg-lightgray text-darkgray'
                } ${msg.error ? 'bg-red-100 text-red-700 border border-red-300' : ''}`}
              >
                {msg.isLoading ? (
                  <LoadingSpinner size="sm" color={msg.sender === 'user' ? 'text-white' : 'text-primary'} />
                ) : (
                  <p className="whitespace-pre-wrap">{msg.text}</p>
                )}
                {msg.error && <p className="text-xs mt-1">Feil: {msg.error}</p>}
                {msg.sources && msg.sources.length > 0 && (
                   <div className="mt-2 pt-2 border-t border-gray-300">
                     <p className="text-xs font-semibold mb-1">Kilder:</p>
                     <ul className="list-disc list-inside text-xs">
                       {msg.sources.map((source, idx) => (
                         <li key={idx}>
                           <a href={source.uri} target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">
                             {source.title || source.uri}
                           </a>
                         </li>
                       ))}
                     </ul>
                   </div>
                 )}
              </div>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      
      <div className="p-4 border-t bg-white">
        <div className="flex flex-wrap gap-2 mb-2">
            {quickActionButtons.map(text => (
                <button key={text} onClick={() => handleSend(text)} className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm hover:bg-gray-200 transition-colors">
                    {text}
                </button>
            ))}
        </div>
        <div className="flex items-center space-x-2">
          <input
            type="text"
            className="flex-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            placeholder="Skriv meldingen din her..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            disabled={pageState === ChatbotState.LOADING}
          />
          <Button onClick={() => handleSend()} isLoading={pageState === ChatbotState.LOADING} disabled={pageState === ChatbotState.LOADING || !input.trim()}>
            <PaperAirplaneIcon className="w-5 h-5" />
            <span className="sr-only">Send</span>
          </Button>
        </div>
         <div className="mt-3 p-3 bg-blue-50 border-l-4 border-primary text-primary-dark rounded-lg text-xs">
          <div className="flex items-start">
            <InformationCircleIcon className="w-5 h-5 mr-2 flex-shrink-0" />
            <p>{AI_DISCLAIMER} Husk at jeg er en AI og kan gjøre feil. For personlig rådgivning og endelige svar, kontakt NAV direkte eller sjekk nav.no.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatbotPage;