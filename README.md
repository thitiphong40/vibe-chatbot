# Hybrid Chatbot with Rule-Based, LLM, and RAG

This chatbot combines three approaches:
1. Rule-based responses for specific queries
2. LLM (Large Language Model) for general conversation
3. RAG (Retrieval Augmented Generation) for answering questions based on local PDF documents

## Features

- Web-based chat interface
- PDF document processing
- Rule-based responses for common queries
- RAG-based responses using document context
- Conversation memory
- Real-time chat updates
- Error handling and status messages
- Docker support for easy deployment

## Setup

### Local Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

4. Place your PDF documents in the `documents` folder

### Docker Setup

1. Make sure Docker and Docker Compose are installed on your system

2. Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

3. Build and run the container:
```bash
docker-compose up --build
```

## Running the Chatbot

### Local Run

1. Generate a sample PDF (optional):
```bash
python generate_pdf.py
```

2. Start the chatbot server:
```bash
python main.py
```

3. Open your web browser and navigate to:
```
http://127.0.0.1:8000
```

### Docker Run

1. Generate a sample PDF (optional):
```bash
python generate_pdf.py
```

2. Start the container:
```bash
docker-compose up
```

3. Open your web browser and navigate to:
```
http://localhost:8000
```

## Web Interface

The web interface provides:
- A clean, modern chat interface
- Real-time message updates
- Automatic document processing
- Status messages for operations
- Support for Enter key to send messages
- Responsive design for both desktop and mobile

## API Endpoints

- `GET /`: Web interface
- `POST /chat`: Send a message to the chatbot
  ```json
  {
    "text": "Your message here"
  }
  ```
- `POST /process-documents`: Process PDF documents in the documents folder

## Troubleshooting

1. Port 8000 is already in use:
   - Close other applications using port 8000
   - Or modify the port in docker-compose.yml

2. Document Processing Issues:
   - Ensure PDF files are in the `documents` directory
   - Check file permissions
   - Verify PDF files are not corrupted

3. API Key Issues:
   - Verify your OpenAI API key in the `.env` file
   - Check your internet connection
   - Ensure you have sufficient API credits

4. Docker Issues:
   - Ensure Docker daemon is running
   - Check container logs: `docker-compose logs`
   - Verify volume mounts are working
   - Check container status: `docker-compose ps`

## Project Structure

```
├── main.py              # FastAPI server and routes
├── chatbot.py           # Main chatbot implementation
├── document_processor.py # PDF processing and RAG
├── rule_based.py        # Rule-based response handling
├── generate_pdf.py      # PDF generation utility
├── requirements.txt     # Project dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose configuration
├── .env                # Environment variables
├── documents/          # PDF document storage
│   └── alphabet_numbers.pdf
└── templates/          # Web interface templates
    └── index.html
```

## Dependencies

- FastAPI: Web framework
- LangChain: LLM and RAG implementation
- OpenAI: Language model and embeddings
- PyPDF: PDF processing
- ChromaDB: Vector storage
- Jinja2: Template rendering
- Uvicorn: ASGI server
- Docker: Containerization

## Customizing System Prompt

You can customize the chatbot's behavior by adding a system prompt, which is especially useful if your documents are related to education or you want the assistant to have a specific tone.

To add a system prompt, update the `process_documents` method in `chatbot.py` as follows:

```python
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

system_prompt = "คุณคือผู้ช่วยตอบคำถามเกี่ยวกับเอกสารการเรียน กรุณาตอบอย่างสุภาพและเน้นข้อมูลจากเอกสารที่มี"
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_prompt),
    HumanMessagePromptTemplate.from_template("ข้อมูลจากเอกสาร:\n{context}\n\nคำถาม: {question}")
])

self.qa_chain = ConversationalRetrievalChain.from_llm(
    llm=self.llm,
    retriever=self.retriever,
    memory=self.memory,
    combine_docs_chain_kwargs={"prompt": prompt}
)
```

**Important:**
- The prompt must include both `{context}` and `{question}` variables.
- Adjust the `system_prompt` string as needed for your use case.
- Make sure you have the necessary imports from `langchain.prompts`.

## Contributing

Feel free to submit issues and enhancement requests! 
