from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chatbot import HybridChatbot
import uvicorn

app = FastAPI(title="Hybrid Chatbot API")
chatbot = HybridChatbot()

class Query(BaseModel):
    text: str

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

# if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=8000) 