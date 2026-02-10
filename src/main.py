"""
CareCall - Main FastAPI Application
Voice Assistant for Elderly Care
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="CareCall API",
    description="Voice Assistant for Elderly Care - DeveloperWeek 2026",
    version="0.1.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active connections (for real-time updates)
active_connections: list[WebSocket] = []

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "app": "CareCall",
        "version": "0.1.0",
        "message": "Voice Assistant for Elderly Care 💙"
    }

@app.get("/demo", response_class=HTMLResponse)
async def demo():
    """Simple demo page to test voice agent"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>CareCall Demo</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .container {
                background: rgba(255, 255, 255, 0.95);
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                color: #333;
            }
            h1 {
                color: #667eea;
                text-align: center;
                margin-bottom: 10px;
            }
            .subtitle {
                text-align: center;
                color: #666;
                margin-bottom: 30px;
            }
            .status {
                padding: 20px;
                background: #f0f0f0;
                border-radius: 10px;
                margin: 20px 0;
            }
            .status.success {
                background: #d4edda;
                border-left: 4px solid #28a745;
            }
            button {
                background: #667eea;
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
                width: 100%;
                margin: 10px 0;
                transition: all 0.3s;
            }
            button:hover {
                background: #5568d3;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }
            button:active {
                transform: translateY(0);
            }
            .feature-list {
                list-style: none;
                padding: 0;
            }
            .feature-list li {
                padding: 10px;
                margin: 5px 0;
                background: #f8f9fa;
                border-radius: 5px;
                border-left: 3px solid #667eea;
            }
            .emoji {
                font-size: 24px;
                margin-right: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🩺 CareCall</h1>
            <p class="subtitle">Voice Assistant for Elderly Care</p>

            <div class="status success">
                <strong>✅ Backend is running!</strong>
                <p>API server is live and ready to connect to Deepgram.</p>
            </div>

            <h2>📋 Setup Checklist</h2>
            <ul class="feature-list">
                <li><span class="emoji">✅</span> FastAPI server running</li>
                <li><span class="emoji">⏳</span> Get Deepgram API key</li>
                <li><span class="emoji">⏳</span> Run test_deepgram.py</li>
                <li><span class="emoji">⏳</span> Build voice agent</li>
                <li><span class="emoji">⏳</span> Add medication tracking</li>
                <li><span class="emoji">⏳</span> Add emergency detection</li>
                <li><span class="emoji">⏳</span> Build family dashboard</li>
            </ul>

            <h2>🚀 Next Steps</h2>
            <ol>
                <li>Get your Deepgram API key from <a href="https://console.deepgram.com/signup" target="_blank">console.deepgram.com</a></li>
                <li>Add it to your <code>.env</code> file</li>
                <li>Run <code>python test_deepgram.py</code></li>
                <li>Start building voice features!</li>
            </ol>

            <h2>💡 Core Features</h2>
            <ul class="feature-list">
                <li><span class="emoji">💊</span> Medication reminders & tracking</li>
                <li><span class="emoji">🚨</span> Emergency detection & alerts</li>
                <li><span class="emoji">📞</span> Voice-controlled calling</li>
                <li><span class="emoji">💬</span> Daily companion conversation</li>
                <li><span class="emoji">📊</span> Family monitoring dashboard</li>
            </ul>

            <button onclick="window.location.href='/'">View API Status</button>
            <button onclick="alert('Voice agent coming soon! Get your Deepgram API key first.')">Test Voice Agent (Coming Soon)</button>
        </div>
    </body>
    </html>
    """

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time voice communication"""
    await websocket.accept()
    active_connections.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            # Echo back for now - will integrate Deepgram Voice Agent here
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        active_connections.remove(websocket)

# API Routes (to be implemented)

@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    deepgram_configured = bool(os.getenv('DEEPGRAM_API_KEY'))

    return {
        "status": "healthy",
        "deepgram_configured": deepgram_configured,
        "active_connections": len(active_connections),
        "features": {
            "voice_agent": deepgram_configured,
            "medication_tracking": False,  # TODO
            "emergency_detection": False,  # TODO
            "family_dashboard": False,     # TODO
        }
    }

@app.post("/api/test-voice")
async def test_voice():
    """Test voice processing"""
    # TODO: Implement Deepgram Voice Agent test
    return {"message": "Voice agent test endpoint - coming soon!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
