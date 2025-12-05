from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
import os
from dotenv import load_dotenv

# Load env vars before importing modules that might use them
load_dotenv()

from orchestrator import orchestrator
from pdf_generator import generate_pdf_report

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI Researcher Backend is running"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await orchestrator.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Expecting a JSON string with a query
            import json
            try:
                message = json.loads(data)
                if "query" in message:
                    await orchestrator.process_query(message["query"])
            except json.JSONDecodeError:
                pass
    except WebSocketDisconnect:
        orchestrator.disconnect(websocket)

@app.get("/generate_pdf")
async def get_pdf_report(content: str):
    # In a real app, content might be passed via POST or retrieved from state
    # For demo, we'll just generate a dummy one or use the query param
    filepath = generate_pdf_report(content)
    return FileResponse(filepath, media_type='application/pdf', filename="report.pdf")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
