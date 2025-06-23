from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from rule_based import RuleBasedHandler
import os
from dotenv import load_dotenv
import glob

load_dotenv()

class PDFAgent:
    """Individual agent specialized for a specific PDF document"""
    
    def __init__(self, pdf_path, agent_name=None, vector_stores_dir="vector_stores"):
        self.pdf_path = pdf_path
        self.agent_name = agent_name or os.path.splitext(os.path.basename(pdf_path))[0]
        self.vector_stores_dir = vector_stores_dir
        self.llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0.7,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.vectorstore = None
        self.qa_chain = None
        self.retriever = None
        
        # Ensure vector stores directory exists
        if not os.path.exists(self.vector_stores_dir):
            os.makedirs(self.vector_stores_dir)
        
    def get_vectorstore_path(self):
        """Get the path for this agent's vector store"""
        return os.path.join(self.vector_stores_dir, f"chroma_db_{self.agent_name.replace(' ', '_').replace('-', '_')}")
        
    def load_existing_vectorstore(self):
        """Load existing vector store if it exists"""
        vectorstore_path = self.get_vectorstore_path()
        if os.path.exists(vectorstore_path):
            print(f"Loading existing vector store for agent '{self.agent_name}': {vectorstore_path}")
            try:
                self.vectorstore = Chroma(
                    persist_directory=vectorstore_path,
                    embedding_function=self.embeddings
                )
                self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
                self._initialize_qa_chain()
                print(f"Successfully loaded existing vector store for agent '{self.agent_name}'")
                return True
            except Exception as e:
                print(f"Error loading vector store for agent '{self.agent_name}': {str(e)}")
                return False
        return False
        
    def _initialize_qa_chain(self):
        """Initialize the QA chain with the current retriever"""
        # Create specialized system prompt for this agent
        system_prompt = f"""คุณคือผู้ช่วยตอบคำถามเกี่ยวกับเอกสาร: {self.agent_name}
        
คุณมีความเชี่ยวชาญเฉพาะในเนื้อหาของเอกสารนี้เท่านั้น กรุณาตอบคำถามโดยอ้างอิงจากข้อมูลในเอกสารนี้เท่านั้น
หากคำถามไม่เกี่ยวข้องกับเอกสารนี้ กรุณาแจ้งให้ทราบว่าคุณไม่สามารถตอบได้

เอกสารที่คุณเชี่ยวชาญ: {self.agent_name}"""

        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template("Context:\n{context}\n\nQuestion: {question}")
        ])

        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            memory=self.memory,
            combine_docs_chain_kwargs={"prompt": prompt}
        )
        
    def process_document(self):
        """Process the specific PDF document for this agent"""
        # First try to load existing vector store
        if self.load_existing_vectorstore():
            print(f"Agent '{self.agent_name}' initialized from existing vector store")
            return self.vectorstore
            
        print(f"Processing document for agent '{self.agent_name}': {self.pdf_path}")
        
        # Load the specific PDF
        loader = PyPDFLoader(self.pdf_path)
        documents = loader.load()
        
        if not documents:
            print(f"No documents were loaded from {self.pdf_path}")
            return None
            
        print(f"Loaded {len(documents)} document chunks from {self.pdf_path}")
        
        # Split documents into chunks
        splits = self.text_splitter.split_documents(documents)
        print(f"Split into {len(splits)} chunks")
        
        # Create vector store with unique name for this agent
        vectorstore_path = self.get_vectorstore_path()
        print(f"Creating vector store: {vectorstore_path}")
        
        self.vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings,
            persist_directory=vectorstore_path
        )
        self.vectorstore.persist()
        
        # Initialize retriever and QA chain
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
        self._initialize_qa_chain()
        
        print(f"Agent '{self.agent_name}' initialized successfully")
        return self.vectorstore
        
    def get_response(self, query):
        """Get response from this specific agent"""
        if not self.qa_chain:
            # Try to load existing vector store before giving up
            if not self.load_existing_vectorstore():
                return f"Agent '{self.agent_name}' has not been initialized. Please process the document first."
            
        try:
            response = self.qa_chain({"question": query})
            return response["answer"]
        except Exception as e:
            print(f"Error in agent '{self.agent_name}': {str(e)}")
            return f"I apologize, but I encountered an error: {str(e)}"
            
    def get_agent_info(self):
        """Get information about this agent"""
        vectorstore_path = self.get_vectorstore_path()
        is_initialized = self.qa_chain is not None or os.path.exists(vectorstore_path)
        
        return {
            "name": self.agent_name,
            "pdf_path": self.pdf_path,
            "is_initialized": is_initialized,
            "vectorstore_path": vectorstore_path,
            "has_vectorstore": os.path.exists(vectorstore_path)
        }

class MultiAgentChatbot:
    """Main chatbot that manages multiple PDF agents"""
    
    def __init__(self, documents_dir="documents", vector_stores_dir="vector_stores"):
        self.documents_dir = documents_dir
        self.vector_stores_dir = vector_stores_dir
        self.agents = {}
        self.rule_handler = RuleBasedHandler()
        
        # Ensure directories exist
        if not os.path.exists(self.vector_stores_dir):
            os.makedirs(self.vector_stores_dir)
        
    def discover_pdfs(self):
        """Discover all PDF files in the documents directory"""
        if not os.path.exists(self.documents_dir):
            print(f"Documents directory not found: {self.documents_dir}")
            return []
            
        pdf_files = glob.glob(os.path.join(self.documents_dir, "*.pdf"))
        print(f"Found {len(pdf_files)} PDF files: {[os.path.basename(f) for f in pdf_files]}")
        return pdf_files
        
    def discover_existing_agents(self):
        """Discover agents from existing vector stores"""
        existing_agents = {}
        chroma_pattern = os.path.join(self.vector_stores_dir, "chroma_db_*")
        chroma_dirs = glob.glob(chroma_pattern)
        
        for chroma_dir in chroma_dirs:
            # Extract agent name from directory name
            dir_name = os.path.basename(chroma_dir)
            agent_name = dir_name.replace("chroma_db_", "").replace("_", " ")
            
            # Try to find corresponding PDF file
            pdf_files = self.discover_pdfs()
            pdf_path = None
            
            for pdf_file in pdf_files:
                pdf_name = os.path.splitext(os.path.basename(pdf_file))[0]
                if pdf_name.replace(" ", "_").replace("-", "_") == agent_name.replace(" ", "_").replace("-", "_"):
                    pdf_path = pdf_file
                    break
            
            if pdf_path:
                existing_agents[agent_name] = PDFAgent(pdf_path, agent_name, self.vector_stores_dir)
                print(f"Discovered existing agent: {agent_name}")
                
        return existing_agents
        
    def create_agents(self):
        """Create agents for all discovered PDF files"""
        pdf_files = self.discover_pdfs()
        
        # First, try to load existing agents from vector stores
        existing_agents = self.discover_existing_agents()
        self.agents.update(existing_agents)
        
        # Then create new agents for PDFs that don't have existing vector stores
        for pdf_path in pdf_files:
            agent_name = os.path.splitext(os.path.basename(pdf_path))[0]
            if agent_name not in self.agents:
                self.agents[agent_name] = PDFAgent(pdf_path, agent_name, self.vector_stores_dir)
                print(f"Created new agent: {agent_name}")
            
        return len(self.agents)
        
    def process_all_documents(self):
        """Process documents for all agents"""
        print("Processing documents for all agents...")
        
        for agent_name, agent in self.agents.items():
            print(f"\n--- Processing agent: {agent_name} ---")
            agent.process_document()
            
        print(f"\nAll {len(self.agents)} agents have been processed")
        
    def get_response(self, query):
        """Get response using hybrid approach with agent selection"""
        # First, try rule-based response
        rule_response = self.rule_handler.get_response(query)
        if rule_response:
            return rule_response
            
        # If no rule matches, try to determine which agent should handle the query
        # For now, we'll use a simple approach - ask the user to specify the agent
        # In a more sophisticated system, you could use an LLM to route queries
        
        if not self.agents:
            return "No agents available. Please create agents first."
            
        # Check if query mentions a specific agent
        for agent_name in self.agents.keys():
            if agent_name.lower() in query.lower():
                agent = self.agents[agent_name]
                return agent.get_response(query)
                
        # If no specific agent mentioned, return list of available agents
        available_agents = list(self.agents.keys())
        return f"""I found multiple specialized agents. Please specify which document you're asking about:

Available agents: {', '.join(available_agents)}

You can mention the agent name in your question, or ask about a specific document."""
        
    def get_agent_response(self, agent_name, query):
        """Get response from a specific agent"""
        if agent_name not in self.agents:
            return f"Agent '{agent_name}' not found. Available agents: {list(self.agents.keys())}"
            
        return self.agents[agent_name].get_response(query)
        
    def list_agents(self):
        """List all available agents and their status"""
        agent_info = {}
        for agent_name, agent in self.agents.items():
            agent_info[agent_name] = agent.get_agent_info()
        return agent_info
        
    def get_agent_status(self, agent_name):
        """Get status of a specific agent"""
        if agent_name not in self.agents:
            return {"error": f"Agent '{agent_name}' not found"}
        return self.agents[agent_name].get_agent_info() 