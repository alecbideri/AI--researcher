import asyncio
import json
from typing import List, Dict
from fastapi import WebSocket
from llm_client import llm_client

class Orchestrator:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

    async def process_query(self, query: str):
        await self.broadcast({"type": "status", "content": f"Orchestrator received query: {query}"})
        
        # 1. Decompose Query using Deepseek
        await self.broadcast({"type": "status", "content": "Decomposing query into hypotheses..."})
        hypotheses = await asyncio.to_thread(llm_client.decompose_query, query)
        
        if not isinstance(hypotheses, list):
            hypotheses = [f"Failed to decompose: {hypotheses}"]
            
        await self.broadcast({"type": "plan", "hypotheses": hypotheses})
        
        # 2. Dispatch Agents
        tasks = []
        for i, hyp in enumerate(hypotheses):
            tasks.append(self.run_agent(i, hyp))
            
        agent_results = await asyncio.gather(*tasks)
        
        # 3. Synthesize
        await self.broadcast({"type": "status", "content": "Synthesizing final report..."})
        final_report = await asyncio.to_thread(llm_client.synthesize_report, query, agent_results)
        
        await self.broadcast({"type": "complete", "report": final_report})
        return final_report

    async def run_agent(self, agent_id: int, hypothesis: str):
        await self.broadcast({"type": "agent_start", "agent_id": agent_id, "hypothesis": hypothesis})
        
        context = []
        # Simulate a few steps of reasoning
        for step_num in range(3):
            thought = await asyncio.to_thread(llm_client.agent_reason, hypothesis, context)
            context.append(thought)
            await self.broadcast({"type": "agent_thought", "agent_id": agent_id, "content": thought})
            await asyncio.sleep(1) # Small delay for visual pacing
            
        result = "\n".join(context)
        await self.broadcast({"type": "agent_complete", "agent_id": agent_id, "result": result})
        return {"hypothesis": hypothesis, "result": result}

orchestrator = Orchestrator()
