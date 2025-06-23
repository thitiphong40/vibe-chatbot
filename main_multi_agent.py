from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from multi_agent_chatbot import MultiAgentChatbot
import uvicorn
import os
import socket

app = FastAPI(title="Multi-Agent PDF Chatbot API")

# Create templates directory if it doesn't exist
if not os.path.exists("templates"):
    os.makedirs("templates")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Initialize multi-agent chatbot
multi_agent_chatbot = MultiAgentChatbot()

class Query(BaseModel):
    text: str

class AgentQuery(BaseModel):
    agent_name: str
    text: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("multi_agent_index.html", {"request": request})

@app.post("/chat")
async def chat(query: Query):
    """Chat with the multi-agent system - it will try to route to the appropriate agent"""
    try:
        response = multi_agent_chatbot.get_response(query.text)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/{agent_name}")
async def chat_with_agent(agent_name: str, query: Query):
    """Chat with a specific agent"""
    try:
        response = multi_agent_chatbot.get_agent_response(agent_name, query.text)
        return {"response": response, "agent": agent_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/create-agents")
async def create_agents():
    """Create agents for all PDF files in the documents directory"""
    try:
        num_agents = multi_agent_chatbot.create_agents()
        return {"message": f"Created {num_agents} agents", "agents": multi_agent_chatbot.list_agents()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-documents")
async def process_documents():
    """Process documents for all agents"""
    try:
        multi_agent_chatbot.process_all_documents()
        return {"message": "All documents processed successfully", "agents": multi_agent_chatbot.list_agents()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents")
async def list_agents():
    """List all available agents and their status"""
    try:
        agents = multi_agent_chatbot.list_agents()
        return {"agents": agents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents/{agent_name}")
async def get_agent_status(agent_name: str):
    """Get status of a specific agent"""
    try:
        status = multi_agent_chatbot.get_agent_status(agent_name)
        return {"agent": status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-agent/{agent_name}")
async def process_agent_document(agent_name: str):
    """Process document for a specific agent"""
    try:
        if agent_name not in multi_agent_chatbot.agents:
            raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")
        
        agent = multi_agent_chatbot.agents[agent_name]
        agent.process_document()
        return {"message": f"Document processed for agent '{agent_name}'", "agent": agent.get_agent_info()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print(f"Starting Multi-Agent Chatbot server on port 8000")
    uvicorn.run(app, host="127.0.0.1", port=8000) 