# AI Researcher - Backend

This directory contains the FastAPI backend for the AI Researcher application. It acts as the orchestrator, managing WebSocket connections, interfacing with the Deepseek API, and generating PDF reports.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Environment Variables**:
    Create a `.env` file in this directory with your Deepseek API key:
    ```env
    DEEPSEEK_API_KEY=your_api_key_here
    ```

3.  **Run the Server**:
    ```bash
    python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```
    The server will start on `http://localhost:8000`.

## Key Files

-   **`main.py`**: Entry point. Sets up FastAPI, CORS, and WebSocket endpoints.
-   **`orchestrator.py`**: Manages the research lifecycle. Decomposes queries, dispatches agents, and broadcasts updates via WebSockets.
-   **`llm_client.py`**: Handles communication with the Deepseek API (Reasoning and Chat models).
-   **`pdf_generator.py`**: Generates the final PDF report using ReportLab Platypus.
-   **`agents.py`** (Conceptual): Logic for individual agents is currently handled dynamically within the Orchestrator and LLM Client.

## API Endpoints

-   `GET /`: Health check.
-   `WS /ws`: WebSocket endpoint for real-time communication. Expects JSON `{ "query": "..." }`.
-   `GET /generate_pdf`: Generates and returns a PDF report.
