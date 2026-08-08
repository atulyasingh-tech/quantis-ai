from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Quantis AI Backend")

# Request schema for chat requests
class ChatRequest(BaseModel):
    message: str

# HTML/JS Chat Interface rendered directly on the root URL
CHAT_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quantis AI - Chat</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
        body { background-color: #0f172a; color: #f8fafc; display: flex; flex-direction: column; height: 100vh; justify-content: center; align-items: center; }
        .chat-container { width: 100%; max-width: 600px; height: 80vh; background: #1e293b; border-radius: 12px; display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
        .chat-header { background: #334155; padding: 16px; font-weight: bold; font-size: 1.2rem; text-align: center; border-bottom: 1px solid #475569; }
        .chat-messages { flex: 1; padding: 16px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; }
        .message { max-width: 80%; padding: 10px 14px; border-radius: 8px; font-size: 0.95rem; line-height: 1.4; }
        .user-message { background: #2563eb; color: white; align-self: flex-end; }
        .agent-message { background: #334155; color: #f1f5f9; align-self: flex-start; }
        .chat-input { display: flex; padding: 12px; background: #0f172a; gap: 8px; border-top: 1px solid #334155; }
        input[type="text"] { flex: 1; background: #1e293b; border: 1px solid #475569; color: white; padding: 10px 14px; border-radius: 6px; outline: none; }
        button { background: #2563eb; color: white; border: none; padding: 10px 18px; border-radius: 6px; cursor: pointer; font-weight: bold; }
        button:hover { background: #1d4ed8; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">Quantis AI Agent</div>
        <div class="chat-messages" id="messages">
            <div class="message agent-message">Hello! I am Quantis AI. How can I assist you today?</div>
        </div>
        <form class="chat-input" id="chatForm">
            <input type="text" id="userInput" placeholder="Type your message..." required autocomplete="off">
            <button type="submit">Send</button>
        </form>
    </div>

    <script>
        const chatForm = document.getElementById('chatForm');
        const userInput = document.getElementById('userInput');
        const messages = document.getElementById('messages');

        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const text = userInput.value.trim();
            if (!text) return;

            // Display user message in chat UI
            addMessage(text, 'user-message');
            userInput.value = '';

            try {
                // Send query to the backend agent chat endpoint
                const res = await fetch('/api/agent/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });
                
                const data = await res.json();
                addMessage(data.response || 'Agent processed your query.', 'agent-message');
            } catch (err) {
                addMessage('Error connecting to backend.', 'agent-message');
            }
        });

        function addMessage(text, className) {
            const div = document.createElement('div');
            div.className = `message ${className}`;
            div.textContent = text;
            messages.appendChild(div);
            messages.scrollTop = messages.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def root():
    """Serves the interactive chat UI directly on the root endpoint."""
    return CHAT_HTML

@app.get("/api/agent/status")
def get_status():
    """Endpoint for checking API status."""
    return {"status": "online", "message": "Quantis AI Backend is running smoothly"}

@app.post("/api/agent/chat")
def chat_with_agent(req: ChatRequest):
    """Chat endpoint that receives user input and generates AI responses."""
    user_msg = req.message
    
    # Place your actual agent call / logic here
    reply = f"Quantis AI received: '{user_msg}'"
    
    return {"response": reply}
