from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from chatbot import HybridChatbot
import uvicorn
import os
import socket

app = FastAPI(title="Hybrid Chatbot API")

# Create templates directory if it doesn't exist
if not os.path.exists("templates"):
    os.makedirs("templates")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Initialize chatbot
chatbot = HybridChatbot()

class Query(BaseModel):
    text: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(query: Query):
    print("input",query)
    try:
        response = chatbot.get_response(query.text)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-documents")
async def process_documents():
    try:
        chatbot.process_documents()
        return {"message": "Documents processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print(f"Starting server on port 8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)