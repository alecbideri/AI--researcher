import React, { useEffect, useRef } from 'react';

const AgentCard = ({ agentId, hypothesis, logs, status }) => {
  const logEndRef = useRef(null);

  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [logs]);

  return (
    <div className="bg-black rounded-none border border-gray-800 p-0 flex flex-col h-80 font-mono shadow-2xl relative overflow-hidden group">
      {/* Header */}
      <div className="flex justify-between items-center p-3 border-b border-gray-800 bg-black z-10">
        <div className="flex items-center gap-2">
          <span className="text-xs font-bold tracking-widest text-gray-400">AGENT {agentId}</span>
          <span className="text-xs text-gray-600">|</span>
          <span className="text-xs text-gray-500">T4</span>
        </div>
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${status === 'completed' ? 'bg-green-500' : 'bg-blue-500 animate-pulse'}`}></div>
          <span className="text-xs font-bold tracking-widest text-gray-400">{status.toUpperCase()}</span>
        </div>
      </div>

      {/* Objective / Hypothesis */}
      <div className="p-4 border-b border-gray-800 bg-black z-10">
        <h4 className="text-xs font-bold text-gray-500 mb-2 tracking-widest">OBJECTIVE</h4>
        <p className="text-sm text-gray-300 leading-relaxed line-clamp-3">
          {hypothesis}
        </p>
      </div>

      {/* Thinking Stream */}
      <div className="flex-1 overflow-y-auto p-4 bg-black relative">
        <div className="absolute top-0 left-0 w-full h-full bg-[radial-gradient(#222_1px,transparent_1px)] [background-size:16px_16px] opacity-20 pointer-events-none"></div>
        <h4 className="text-xs font-bold text-gray-500 mb-3 tracking-widest flex items-center gap-2">
          <span className="text-blue-500">●</span> THINKING
        </h4>
        <div className="space-y-4">
          {logs.map((log, index) => (
            <div key={index} className="animate-fadeIn">
              <p className="text-sm text-gray-300 leading-relaxed font-sans">
                {log}
              </p>
            </div>
          ))}
          <div ref={logEndRef} />
        </div>
      </div>
    </div>
  );
};

export default AgentCard;
