# AI Researcher - Frontend

This directory contains the React frontend for the AI Researcher application. It provides a modern, dark-mode interface for users to input queries and visualize the research process in real-time.

## Setup

1.  **Install Dependencies**:
    ```bash
    npm install
    ```

2.  **Run Development Server**:
    ```bash
    npm run dev
    ```
    The app will start on `http://localhost:5173`.

## Tech Stack

-   **React**: UI Library.
-   **Vite**: Build tool.
-   **Tailwind CSS**: Styling (configured for Dark Mode).

## Key Components

-   **`App.jsx`**: Main application logic. Handles WebSocket connection, state management (agents, report), and layout.
-   **`components/AgentCard.jsx`**: Displays the status and "thinking process" of an individual research agent. Styled with a technical, minimal aesthetic.
-   **`components/ResearchReport.jsx`**: Renders the final synthesized report and provides a button to download it as a PDF.

## Features

-   **Real-time Updates**: Uses WebSockets to show agent progress live.
-   **Dark Mode**: "Dot pattern" background and high-contrast UI.
-   **Responsive Design**: Grid layout adapts to screen size.
