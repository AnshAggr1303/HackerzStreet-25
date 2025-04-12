# app/services/llm_service.py
import requests

# class LlamaService:
    
        
        
#     async def generate_response(self, prompt: str, context: str) -> str:
#         full_prompt = f"""Context: {context}\n\nQuestion: {prompt}\n\nAnswer:"""
        
#         response = requests.post(
#             self.api_url,
#             json={
#                 "model": "llama2",
#                 "prompt": full_prompt,
#                 "stream": False
#             }
#         )
#         return response.json()['response']
    
import os
import json
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import nest_asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
import pickle
import atexit
from ollama import chat
from ollama import ChatResponse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Apply nest_asyncio if needed
nest_asyncio.apply()

app = FastAPI()

# ----------------------------
# Custom Conversation Memory
# ----------------------------
class SimpleMessage:
    """
    A simple message object to hold a role ('human' for user, 'ai' for assistant)
    and its content.
    """
    def __init__(self, role: str, content: str):
        self.type = role  # "human" for user messages, "ai" for assistant messages
        self.content = content

class SimpleConversationBufferMemory:
    """
    A basic conversation memory that stores the last 'k' messages.
    """
    def __init__(self, k: int = 5, memory_key: str = 'chat_history'):
        self.memory_key = memory_key
        self.k = k
        self.messages = []  # List to store SimpleMessage objects

    def load_memory_variables(self, inputs: dict):
        """
        Return the last 'k' messages stored in memory.
        """
        return {self.memory_key: self.messages[-self.k:]}

    def save_context(self, inputs: dict, outputs: dict):
        """
        Save the user's question and the assistant's answer into memory.
        """
        user_input = inputs.get("input")
        assistant_output = outputs.get("output")
        if user_input:
            self.messages.append(SimpleMessage("human", user_input))
        if assistant_output:
            self.messages.append(SimpleMessage("ai", assistant_output))


# ----------------------------
# Global Variables and Storage
# ----------------------------
user_memories = {}
memory_file_path = 'user_memories.pkl'
file_path = 'user_prompts.json'  # Ensure this is defined before usage

def load_user_memories():
    global user_memories
    if os.path.exists(memory_file_path):
        with open(memory_file_path, 'rb') as f:
            user_memories = pickle.load(f)
            logging.info("User memories loaded from disk.")
    else:
        user_memories = {}
        logging.info("No existing user memories found. Starting fresh.")

def save_user_memories():
    with open(memory_file_path, 'wb') as f:
        pickle.dump(user_memories, f)
        logging.info("User memories saved to disk.")

# Load user memories at startup
load_user_memories()

# Save user memories on shutdown
atexit.register(save_user_memories)

# ----------------------------
# Response Generation Function
# ----------------------------

class LlamaService:
    async def generate_response(self, question: str, context: str) -> str:
        """
        Generate a response using Gemini's GenerativeModel with the relevant context and user memory.
        """
        user_id = "a"
        # Retrieve or initialize user memory using our custom SimpleConversationBufferMemory
        if user_id not in user_memories:
            user_memories[user_id] = SimpleConversationBufferMemory(memory_key='chat_history', k=5)
        
        memory = user_memories[user_id]
        
        # Retrieve conversation history
        chat_history = memory.load_memory_variables({"input": question})
        messages = chat_history.get('chat_history', [])
        
        # Format the conversation history into a readable text block
        history_text = ""
        for msg in messages:
            if msg.type == "human":
                history_text += f"User: {msg.content}\n"
            elif msg.type == "ai":
                history_text += f"Assistant: {msg.content}\n"
        
        # Retrieve relevant context from your vector store (or other source)
        # Here, we're using a hard-coded example
        # context = "Quark is the technical fest of BITS Goa. It will happen on 7th Feb."
        logging.info(f"Retrieved context for user {user_id}: {context}")
        
        # Construct the prompt using the context and conversation history
        prompt = f"""
    You are an assistant for answering questions based on the context provided.
    Answer based on the context provided.
    Do not mention the word context in the answer.

    Context:
    {context}

    Conversation History:
    {history_text}

    User: {question}

    Assistant:
    """
        print(prompt)
        
        try:
            # Generate the response using ollama's chat function
            response: ChatResponse = chat(model='llama3', messages=[
                {
                    'role': 'user',
                    'content': prompt,
                },
            ])
            answer = response['message']['content']
        except Exception as e:
            logging.error(f"Error generating response with Llama: {e}")
            raise e
        
        # Update conversation memory with the latest interaction
        memory.save_context({"input": question}, {"output": answer})
        
        return answer

# ----------------------------
# Data Loading and Saving
# ----------------------------
def load_data():
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            for user_id in data:
                date_str, count = data[user_id]
                data[user_id] = (datetime.strptime(date_str, '%Y-%m-%d').date(), count)
            return data
    except FileNotFoundError:
        return {}  # Return an empty dictionary if file doesn't exist

def save_data(data):
    # Convert the date object to a string for JSON serialization
    data_to_save = {user_id: (date.strftime('%Y-%m-%d'), count) for user_id, (date, count) in data.items()}
    with open(file_path, 'w') as f:
        json.dump(data_to_save, f)

user_prompts = load_data()
