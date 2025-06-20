from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from document_processor import DocumentProcessor
from rule_based import RuleBasedHandler
import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

load_dotenv()

class HybridChatbot:
    def __init__(self):
        # Initialize OpenAI client with correct parameters
        self.llm = ChatOpenAI(
            model_name="gpt-4o-mini",
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
        # self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 1})
        system_prompt = "คุณคือผู้ช่วยตอบคำถามเกี่ยวกับเอกสารการเรียน กรุณาตอบอย่างสุภาพและเน้นข้อมูลจากเอกสารที่มี"
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