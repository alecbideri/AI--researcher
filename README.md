# AI Researcher

An autonomous research assistant that decomposes complex queries into hypotheses, launches agents to investigate them using Deepseek Reasoner, and synthesizes a final report.

## Architecture

The system consists of two main parts:

1.  **Backend (FastAPI)**:
    -   **Orchestrator**: Breaks down the user's query into sub-tasks (hypotheses).
    -   **Agents**: Autonomous workers that "reason" about each hypothesis using the Deepseek API.
    -   **Deepseek Integration**: Uses the `deepseek-reasoner` (or compatible) model for high-level logic.
    -   **PDF Service**: Generates downloadable reports.

2.  **Frontend (React + Vite)**:
    -   **Live Dashboard**: Visualizes the agents' thinking process in real-time.
    -   **Technical Aesthetic**: Designed with a minimal, dark-mode "terminal" look.

## Quick Start

### Prerequisites
-   Python 3.8+
-   Node.js 16+
-   Deepseek API Key

### 1. Start the Backend
Navigate to the `backend` folder:
```bash
cd backend
pip install -r requirements.txt
# Create .env file with DEEPSEEK_API_KEY=...
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Start the Frontend
Navigate to the `frontend` folder:
```bash
cd frontend
npm install
npm run dev
```

### 3. Use the App
Open `http://localhost:5173` in your browser. Enter a research query (e.g., "The future of solid-state batteries") and watch the agents work.

## Features
-   **Deepseek Reasoner**: Powered by advanced reasoning models.
-   **Live Streaming**: See the AI's "thought process" as it happens.
-   **PDF Export**: Download a professionally formatted report of the findings.
