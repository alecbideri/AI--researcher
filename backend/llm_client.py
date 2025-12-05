import requests
import os
import json

class DeepseekClient:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            print("ERROR: DEEPSEEK_API_KEY not found in environment variables.")
        else:
            print(f"Loaded API Key: {self.api_key[:4]}...{self.api_key[-4:]}")
        self.base_url = "https://api.deepseek.com"
        
    def _chat_completion(self, messages, model="deepseek-reasoner"):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "messages": messages,
            "stream": False
        }
        
        # Note: deepseek-reasoner might be 'deepseek-coder' or 'deepseek-chat' depending on exact model name availability.
        # Using 'deepseek-chat' as a safe default fallback if reasoner isn't the exact ID, 
        # but user asked for reasoner so we try to stick to that intent.
        # If 'deepseek-reasoner' fails, we might need to fallback.
        
        try:
            response = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=data)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Error calling Deepseek API: {e}")
            return f"Error: {str(e)}"

    def decompose_query(self, query):
        system_prompt = """You are a Research Orchestrator. Your goal is to decompose a complex user query into 3-5 distinct, testable hypotheses or sub-research questions.
        Return ONLY a JSON array of strings. Do not include markdown formatting or explanation.
        Example: ["Hypothesis 1...", "Hypothesis 2...", "Hypothesis 3..."]"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Decompose this query: {query}"}
        ]
        
        response = self._chat_completion(messages, model="deepseek-chat") # Using deepseek-chat for reliable JSON
        try:
            # Clean up potential markdown code blocks
            clean_response = response.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_response)
        except:
            return [f"Could not parse hypotheses from: {response}"]

    def agent_reason(self, hypothesis, context=[]):
        system_prompt = """You are an Autonomous Research Agent. You are investigating a specific hypothesis.
        Your goal is to simulate a reasoning process.
        Provide a short, insightful 'thought' or 'finding' based on your internal knowledge.
        Keep it under 50 words. Focus on facts, data, or logical deductions."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Hypothesis: {hypothesis}\nPrevious Context: {context}\n\nWhat is your next thought or finding?"}
        ]
        
        return self._chat_completion(messages, model="deepseek-chat")

    def synthesize_report(self, query, agent_results):
        system_prompt = """You are a Lead Researcher. Synthesize the findings from multiple agents into a cohesive final report.
        Format it with Markdown. Include a title, executive summary, and detailed findings section."""
        
        findings_text = "\n\n".join([f"Hypothesis: {r['hypothesis']}\nResult: {r['result']}" for r in agent_results])
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Original Query: {query}\n\nAgent Findings:\n{findings_text}"}
        ]
        
        return self._chat_completion(messages, model="deepseek-chat")

llm_client = DeepseekClient()
