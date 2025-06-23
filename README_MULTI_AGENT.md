# Multi-Agent PDF Chatbot System

This system creates specialized AI agents, each dedicated to a specific PDF document. Each agent has its own knowledge base, memory, and conversation context, allowing for more focused and accurate responses about specific documents.

## Features

- **Multi-Agent Architecture**: Each PDF gets its own specialized agent
- **Individual Vector Stores**: Each agent maintains its own document embeddings
- **Agent-Specific Memory**: Each agent remembers conversation context independently
- **Smart Routing**: Automatic or manual selection of appropriate agents
- **Persistent Storage**: Vector stores are saved and reloaded automatically
- **Fast Loading**: No reprocessing of previously processed documents
- **Web Interface**: Modern UI for managing and chatting with agents
- **REST API**: Full API for programmatic access

## Architecture

```
MultiAgentChatbot
├── PDFAgent 1 (Document A)
│   ├── Vector Store A (chroma_db_agent_1)
│   ├── Memory A
│   └── LLM Chain A
├── PDFAgent 2 (Document B)
│   ├── Vector Store B (chroma_db_agent_2)
│   ├── Memory B
│   └── LLM Chain B
└── ...
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

3. Place your PDF files in the `documents/` directory

## Usage

### Web Interface

1. Start the server:
```bash
python main_multi_agent.py
```

2. Open your browser to `http://localhost:8000`

3. Use the interface to:
   - Create agents for all PDFs (discovers existing ones automatically)
   - Process documents (only for new documents)
   - Select specific agents
   - Chat with agents

### API Endpoints

#### Agent Management
- `POST /create-agents` - Create agents for all PDFs (discovers existing ones)
- `GET /agents` - List all agents and their status
- `GET /agents/{agent_name}` - Get specific agent status

#### Document Processing
- `POST /process-documents` - Process all documents (skips existing ones)
- `POST /process-agent/{agent_name}` - Process specific agent's document

#### Chat
- `POST /chat` - Chat with automatic agent routing
- `POST /chat/{agent_name}` - Chat with specific agent

### Programmatic Usage

```python
from multi_agent_chatbot import MultiAgentChatbot

# Initialize
chatbot = MultiAgentChatbot()

# Create agents for all PDFs (automatically discovers existing ones)
chatbot.create_agents()

# Process all documents (only processes new ones)
chatbot.process_all_documents()

# Chat with specific agent (loads from cache if available)
response = chatbot.get_agent_response("document_name", "What is this about?")

# Chat with automatic routing
response = chatbot.get_response("Tell me about the internship document")
```

## File Structure

```
vibe-chatbot/
├── multi_agent_chatbot.py      # Core multi-agent system
├── main_multi_agent.py         # FastAPI server
├── templates/
│   └── multi_agent_index.html  # Web interface
├── tests/                      # Test files directory
│   ├── test_multi_agent.py     # Basic functionality test
│   ├── test_loading.py         # Vector store loading test
│   ├── debug_agents.py         # Agent debugging script
│   └── run_tests.py            # Test runner
├── documents/                  # PDF files directory
├── vector_stores/              # Vector store directories (auto-created)
│   └── chroma_db_*/           # Individual agent vector stores
└── README_MULTI_AGENT.md       # This documentation
```

## Key Components

### PDFAgent Class
- **Purpose**: Individual agent for a specific PDF
- **Features**:
  - Dedicated vector store with persistent storage
  - Independent conversation memory
  - Specialized system prompts
  - Document-specific knowledge
  - Automatic loading from existing vector stores

### MultiAgentChatbot Class
- **Purpose**: Orchestrates multiple agents
- **Features**:
  - Agent discovery and creation
  - Automatic discovery of existing vector stores
  - Document processing management
  - Query routing
  - Agent status monitoring

## Agent Specialization

Each agent is specialized for its document through:

1. **Unique Vector Store**: Separate embeddings for each document
2. **Persistent Storage**: Vector stores saved as `chroma_db_[agent_name]`
3. **Specialized Prompts**: Context-aware system prompts
4. **Independent Memory**: Separate conversation history
5. **Document-Specific Knowledge**: Focused on single document content

## Performance Features

### Vector Store Persistence
- **Automatic Saving**: Vector stores are automatically saved after processing
- **Fast Loading**: Existing vector stores load instantly on restart
- **No Reprocessing**: Previously processed documents are not reprocessed
- **Smart Discovery**: Automatically finds existing agents from vector store directories

### Status Indicators
- **Ready (from cache)**: Agent loaded from existing vector store
- **Ready**: Agent initialized from fresh processing
- **Not initialized**: Agent needs document processing

## Benefits

1. **Better Accuracy**: Agents focus on specific documents
2. **Reduced Confusion**: No cross-document contamination
3. **Scalability**: Easy to add new documents
4. **Performance**: Smaller, focused vector stores
5. **Flexibility**: Can query specific or general knowledge
6. **Persistence**: No need to reprocess documents on restart
7. **Fast Startup**: Existing agents load instantly

## Example Workflow

1. **Setup**: Place PDFs in `documents/` directory
2. **Create Agents**: System automatically creates agents for each PDF
3. **Process Documents**: Each agent processes its assigned document (creates vector stores)
4. **Restart**: On restart, agents automatically load from existing vector stores
5. **Chat**: 
   - Select specific agent for focused questions
   - Use general chat for automatic routing
   - Ask about specific documents by name

## Testing

### Run All Tests
```bash
# Run all tests from the tests directory
python tests/run_tests.py
```

### Individual Tests

#### Basic Functionality Test
```bash
python tests/test_multi_agent.py
```

#### Vector Store Loading Test
```bash
python tests/test_loading.py
```

#### Debug Script
```bash
python tests/debug_agents.py
```

This script provides detailed information about:
- PDF files discovered
- Vector stores found
- Agents created
- Orphaned stores
- Cleanup recommendations

#### Manual Debugging
```bash
# Check PDF files
ls -la documents/*.pdf

# Check vector stores
ls -la vector_stores/chroma_db_*

# Check agent creation
python -c "
from multi_agent_chatbot import MultiAgentChatbot
chatbot = MultiAgentChatbot()
print(f'PDFs: {len(chatbot.discover_pdfs())}')
print(f'Agents: {len(chatbot.create_agents())}')
"
```

This test verifies that:
- Existing vector stores are discovered automatically
- Agents load from cache without reprocessing
- Response times are faster with cached data
- Status indicators work correctly

## Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key
- `DOCUMENTS_DIR`: Directory containing PDF files (default: "documents")

### Agent Configuration
- **Chunk Size**: 1000 characters (configurable in PDFAgent)
- **Chunk Overlap**: 200 characters
- **Retrieval**: Top 3 most relevant chunks
- **Model**: GPT-4o-mini (configurable)
- **Vector Store**: Chroma with persistent storage

## Troubleshooting

### Common Issues

1. **No agents created**: Check if PDFs exist in documents directory
2. **Processing fails**: Verify OpenAI API key and internet connection
3. **Memory issues**: Large PDFs may require more RAM
4. **Slow processing**: Consider reducing chunk size for large documents
5. **Vector store not loading**: Check if `chroma_db_*` directories exist and have proper permissions

### Performance Tips

1. **Document Size**: Keep PDFs under 50MB for optimal performance
2. **Chunk Size**: Adjust based on document complexity
3. **Vector Store**: Each agent creates its own store for better isolation
4. **Memory**: Monitor RAM usage with many large documents
5. **Caching**: Vector stores are automatically cached for faster subsequent loads

### Vector Store Management

- **Location**: Vector stores are saved in `vector_stores/chroma_db_[agent_name]` directories
- **Backup**: You can backup the `vector_stores/` directory to preserve processed data
- **Cleanup**: Delete `vector_stores/chroma_db_*` directories to force reprocessing
- **Migration**: Vector stores are portable between installations
- **Orphaned Stores**: Vector stores without corresponding PDF files can cause agent count mismatches

## Advanced Features

### Agent Discovery
The system automatically discovers existing agents by:
1. Scanning for `chroma_db_*` directories
2. Matching directory names to PDF files
3. Creating agent instances for found matches
4. Loading existing vector stores

### Smart Processing
- **Skip Existing**: Agents with existing vector stores are not reprocessed
- **Load on Demand**: Vector stores are loaded when first accessed
- **Error Recovery**: Failed loads fall back to reprocessing
- **Status Tracking**: Real-time status updates in the UI

## Future Enhancements

- **Smart Routing**: LLM-based query routing to appropriate agents
- **Agent Collaboration**: Multi-agent conversations
- **Document Updates**: Incremental document processing
- **Advanced UI**: Drag-and-drop document management
- **Export/Import**: Agent configuration persistence
- **Vector Store Optimization**: Compression and indexing improvements
- **Multi-language Support**: Support for documents in different languages 

#### Quick Fix
```bash
# List all vector store directories
ls -la vector_stores/chroma_db_*

# Remove orphaned vector stores (replace with actual directory names)
rm -rf vector_stores/chroma_db_orphaned_agent_name

# Or remove all vector stores to start fresh
rm -rf vector_stores/chroma_db_*
```

#### Debug the Issue
```bash
# Run the debug script to identify the problem
python tests/debug_agents.py
``` 