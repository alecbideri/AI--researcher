import React, { useState, useEffect, useRef } from 'react';
import AgentCard from './components/AgentCard';
import ResearchReport from './components/ResearchReport';

function App() {
  const [query, setQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const [agents, setAgents] = useState({});
  const [report, setReport] = useState(null);
  const ws = useRef(null);

  useEffect(() => {
    ws.current = new WebSocket('ws://localhost:8000/ws');

    ws.current.onopen = () => {
      console.log('Connected to WebSocket');
    };

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      handleWebSocketMessage(data);
    };

    return () => {
      ws.current.close();
    };
  }, []);

  const handleWebSocketMessage = (data) => {
    switch (data.type) {
      case 'status':
        console.log("Status:", data.content);
        break;
      case 'plan':
        // Initialize agents based on hypotheses
        const newAgents = {};
        data.hypotheses.forEach((hyp, index) => {
          newAgents[index] = {
            id: index,
            hypothesis: hyp,
            logs: [],
            status: 'working'
          };
        });
        setAgents(newAgents);
        break;
      case 'agent_start':
        // Agent started (already handled by plan, but could update status)
        break;
      case 'agent_thought':
        setAgents(prev => ({
          ...prev,
          [data.agent_id]: {
            ...prev[data.agent_id],
            logs: [...prev[data.agent_id].logs, data.content]
          }
        }));
        break;
      case 'agent_complete':
        setAgents(prev => ({
          ...prev,
          [data.agent_id]: {
            ...prev[data.agent_id],
            status: 'completed',
            logs: [...prev[data.agent_id].logs, `Result: ${data.result}`]
          }
        }));
        break;
      case 'complete':
        setReport(data.report);
        setIsSearching(false);
        break;
      default:
        break;
    }
  };

  const handleSearch = () => {
    if (!query.trim()) return;
    setIsSearching(true);
    setAgents({});
    setReport(null);
    ws.current.send(JSON.stringify({ query }));
  };

  return (
    <div className="min-h-screen bg-transparent text-white p-8 font-sans selection:bg-blue-500 selection:text-white">
      <div className="max-w-7xl mx-auto">
        <header className="mb-16 pt-8">
          <div className="flex items-center gap-4 mb-2">
            <div className="w-3 h-3 bg-blue-500 rounded-full animate-pulse"></div>
            <h1 className="text-sm font-bold tracking-[0.2em] text-gray-400 uppercase">
              AI Researcher // v1.0
            </h1>
          </div>
          <p className="text-4xl md:text-6xl font-bold text-white tracking-tight max-w-3xl">
            Autonomous investigation <br />
            <span className="text-gray-600">into the unknown.</span>
          </p>
        </header>

        <div className="mb-20">
          <div className="relative w-full max-w-3xl group">
            <div className="absolute -inset-0.5 bg-gradient-to-r from-gray-700 to-gray-800 rounded-none opacity-50 group-hover:opacity-100 transition duration-500 blur"></div>
            <div className="relative flex flex-col bg-black border border-gray-800 p-2">
              <textarea
                className="w-full bg-black text-white text-lg p-4 focus:outline-none resize-none placeholder-gray-600 font-mono"
                rows="3"
                placeholder="> Describe your scientific query..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                disabled={isSearching}
                spellCheck="false"
              />
              <div className="flex justify-end p-2 border-t border-gray-900">
                <button
                  onClick={handleSearch}
                  disabled={isSearching}
                  className={`bg-white text-black hover:bg-gray-200 font-bold py-3 px-8 text-xs tracking-widest uppercase transition ${isSearching ? 'opacity-50 cursor-not-allowed' : ''}`}
                >
                  {isSearching ? 'INITIALIZING...' : 'START RESEARCH'}
                </button>
              </div>
            </div>
          </div>
        </div>

        {Object.keys(agents).length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-12">
            {Object.values(agents).map(agent => (
              <AgentCard
                key={agent.id}
                agentId={agent.id}
                hypothesis={agent.hypothesis}
                logs={agent.logs}
                status={agent.status}
              />
            ))}
          </div>
        )}

        {report && <ResearchReport report={report} />}
      </div>
    </div>
  );
}

export default App;
