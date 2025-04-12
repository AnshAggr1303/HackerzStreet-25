'use client';

import { useState, useEffect } from 'react';
import { ArrowUpIcon, MicrophoneIcon } from '@heroicons/react/24/solid';

export default function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [isThinking, setIsThinking] = useState(false);
  const [inputPosition, setInputPosition] = useState("center");
  const [thinkingText, setThinkingText] = useState("Thinking");
  const [streamingText, setStreamingText] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);

  useEffect(() => {
    let interval;
    if (isThinking) {
      let dots = 0;
      interval = setInterval(() => {
        dots = (dots + 1) % 4;
        setThinkingText("Thinking" + ".".repeat(dots));
      }, 500);
    } else {
      setThinkingText("");
    }
    return () => clearInterval(interval);
  }, [isThinking]);

  const simulateStreaming = (text) => {
    setIsStreaming(true);
    let index = 0;
    setStreamingText("");

    const streamInterval = setInterval(() => {
      if (index < text.length) {
        setStreamingText((prev) => prev + text.charAt(index));
        index++;
      } else {
        clearInterval(streamInterval);
        setIsStreaming(false);
        setMessages(prev => [...prev, { sender: 'bot', text }]);
        setStreamingText("");
      }
    }, 10);
  };

  const handleKeyDown = async (e) => {
    if (e.key === "Enter" && inputValue.trim() !== "") {
      const userMessage = { sender: 'user', text: inputValue.trim() };
      setMessages(prev => [...prev, userMessage]);
      setInputValue("");

      if (inputPosition === 'center') {
        setInputPosition('bottom');
      }

      setIsThinking(true);
      try {
        const response = await fetch('http://127.0.0.1:8000/api/query', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ prompt: userMessage.text })
        });
        const data = await response.json();
        setIsThinking(false);
        simulateStreaming(data.response);
      } catch (error) {
        console.error('Error querying API:', error);
        setIsThinking(false);
        simulateStreaming("An error occurred while fetching response.");
      }
    }
  };

  const uploadAudio = async (chunks) => {
    try {
      const blob = new Blob(chunks, { type: 'audio/mp3' });
      const formData = new FormData();
      formData.append('file', blob, 'recording.mp3');

      const response = await fetch('http://127.0.0.1:8000/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const data = await response.json();

      const audioBlob = new Blob(
        [Uint8Array.from(atob(data.audio_content), c => c.charCodeAt(0))],
        { type: 'audio/mp3' }
      );
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      audio.play();

      return data;
    } catch (error) {
      console.error('Error uploading file:', error);
      throw error;
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      const chunks = [];

      recorder.ondataavailable = (e) => chunks.push(e.data);
      recorder.onstop = async () => {
        try {
          const data = await uploadAudio(chunks);
          if (inputPosition === 'center') setInputPosition('bottom');
          setMessages(prev => [...prev, { sender: 'user', text: data.question }]);
          simulateStreaming(data.llm_response);
        } catch (err) {
          console.error('Upload failed:', err);
        }
      };

      recorder.start();
      setMediaRecorder(recorder);
      setIsRecording(true);
    } catch (err) {
      console.error('Error recording audio:', err);
    }
  };

  const stopRecording = () => {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
      mediaRecorder.stop();
      mediaRecorder.stream.getTracks().forEach(track => track.stop());
      setIsRecording(false);
    }
  };

  return (
    <div className="relative min-h-screen bg-gradient-to-br from-[#0d1117] to-[#1e2a38] text-white">
      <div className="absolute inset-0 flex flex-col justify-center overflow-y-auto pt-8 pb-36 px-4">
        <div className="mx-auto w-full max-w-3xl space-y-3">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`px-4 py-3 rounded-2xl max-w-xl shadow-lg transition 
                ${msg.sender === 'user' 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-gray-800 text-gray-200'}`}
              >
                {msg.text}
              </div>
            </div>
          ))}

          {isThinking && (
            <div className="flex justify-start">
              <div className="max-w-xl px-4 py-2 rounded-2xl bg-gray-700 text-gray-300 italic shadow">
                {thinkingText}
              </div>
            </div>
          )}

          {isStreaming && (
            <div className="flex justify-start">
              <div className="max-w-xl px-4 py-2 rounded-2xl bg-gray-700 text-white shadow-lg">
                {streamingText}
                <span className="animate-pulse text-gray-400">▊</span>
              </div>
            </div>
          )}
        </div>
      </div>

      <div
        className={`absolute left-1/2 transform -translate-x-1/2 w-11/12 max-w-3xl transition-all duration-500 ease-in-out 
        ${inputPosition === 'center' ? 'top-1/2 -translate-y-1/2' : 'bottom-6'}`}
      >
        {(!messages.some(msg => msg.sender === 'user')) && (
          <div className="flex flex-col items-center justify-center mb-20">
            <h1 className="text-5xl font-bold text-white tracking-tight">Aarogya AI</h1>
            <p className="text-lg text-gray-300 mt-2">Your Health Assistant</p>
          </div>
        )}

        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleKeyDown({ key: 'Enter' });
          }}
          className="flex items-center gap-2 bg-[#1e293b] rounded-2xl px-4 py-3 shadow-lg"
        >
          <div className="relative w-full">
            <input
              type="text"
              placeholder="Type your prompt..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              className="w-full bg-transparent text-white placeholder-gray-400 focus:outline-none pr-12"
            />
            <button
              type="button"
              onClick={isRecording ? stopRecording : startRecording}
              className="absolute right-3 top-1/2 transform -translate-y-1/2 p-2 rounded-full bg-blue-600 hover:bg-blue-500 transition"
            >
              <MicrophoneIcon className="h-5 w-5 text-white" />
            </button>
          </div>
          <button
            type="submit"
            disabled={!inputValue.trim()}
            className="bg-gray-700 hover:bg-gray-600 p-3 rounded-full transition"
          >
            <ArrowUpIcon className="h-5 w-5 text-white" />
          </button>
        </form>
      </div>
    </div>
  );
}
