from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from document_processor import DocumentProcessor
from rule_based import RuleBasedHandler
import os
from dotenv import load_dotenv

load_dotenv()

class HybridChatbot:
    def __init__(self):
        # Initialize OpenAI client with correct parameters
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.7,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.document_processor = DocumentProcessor()
        self.rule_handler = RuleBasedHandler()
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Initialize RAG components
        self.vectorstore = None
        self.qa_chain = None
        
    def process_documents(self):
        """Process all documents in the documents directory"""
        print("Processing documents...")
        self.vectorstore = self.document_processor.process_documents()
        print("Documents processed successfully")
        
        # Initialize QA chain after processing documents
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            memory=self.memory,
        )
        print("QA chain initialized with processed documents")
        return self.vectorstore
        
    def get_response(self, query):
        """Get response using the hybrid approach"""
        # First, try rule-based response
        rule_response = self.rule_handler.get_response(query)
        print("rule_response", rule_response)
        if rule_response:
            return rule_response
            
        # If no rule matches, use RAG + LLM
        try:
            if not self.qa_chain:
                return "Please process documents first using the /process-documents endpoint"
                
            response = self.qa_chain({"question": query})
            print("RAG response:", response["answer"])
            return response["answer"]
        except Exception as e:
            print(f"Error in RAG response: {str(e)}")
            return f"I apologize, but I encountered an error: {str(e)}" 