from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

class DocumentProcessor:
    def __init__(self, documents_dir="documents"):
        self.documents_dir = documents_dir
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
    def process_documents(self):
        """Process all PDF documents in the documents directory"""
        if not os.path.exists(self.documents_dir):
            os.makedirs(self.documents_dir)
            print(f"Created documents directory: {self.documents_dir}")
            
        documents = []
        pdf_files = [f for f in os.listdir(self.documents_dir) if f.endswith('.pdf')]
        
        if not pdf_files:
            print("No PDF files found in documents directory")
            return None
            
        print(f"Found {len(pdf_files)} PDF files")
        
        for filename in pdf_files:
            file_path = os.path.join(self.documents_dir, filename)
            print(f"Processing file: {filename}")
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())
        
        if not documents:
            print("No documents were loaded")
            return None
            
        print(f"Loaded {len(documents)} document chunks")
        
        # Split documents into chunks
        splits = self.text_splitter.split_documents(documents)
        print(f"Split into {len(splits)} chunks")
        
        # Create and persist vector store
        print("Creating vector store...")
        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings,
            persist_directory="chroma_db"
        )
        vectorstore.persist()
        print("Vector store created and persisted")
        return vectorstore
    
    def get_retriever(self):
        """Get the retriever for the vector store"""
        if not os.path.exists("chroma_db"):
            print("No existing vector store found")
            return None
            
        print("Loading existing vector store")
        vectorstore = Chroma(
            persist_directory="chroma_db",
            embedding_function=self.embeddings
        )
        return vectorstore.as_retriever(search_kwargs={"k": 3}) 