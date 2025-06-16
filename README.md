# Hybrid Chatbot with Rule-Based, LLM, and RAG

This chatbot combines three approaches:
1. Rule-based responses for specific queries
2. LLM (Large Language Model) for general conversation
3. RAG (Retrieval Augmented Generation) for answering questions based on local PDF documents

## Setup

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

## Running the Chatbot

Start the chatbot server:
```bash
python main.py
```

The chatbot will be available at `http://localhost:8000` 