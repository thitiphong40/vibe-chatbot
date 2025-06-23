#!/usr/bin/env python3
"""
Debug script to identify agent creation issues
"""

import os
import glob
from multi_agent_chatbot import MultiAgentChatbot

def debug_agent_creation():
    """Debug why there are more agents than PDF files"""
    
    print("=== Agent Creation Debug ===\n")
    
    # Check documents directory
    print("1. Checking documents directory:")
    documents_dir = "documents"
    if os.path.exists(documents_dir):
        pdf_files = glob.glob(os.path.join(documents_dir, "*.pdf"))
        print(f"   Found {len(pdf_files)} PDF files:")
        for pdf in pdf_files:
            print(f"   - {os.path.basename(pdf)}")
    else:
        print(f"   Documents directory '{documents_dir}' not found")
    print()
    
    # Check existing vector stores
    print("2. Checking existing vector stores:")
    chroma_dirs = glob.glob("chroma_db_*")
    print(f"   Found {len(chroma_dirs)} vector store directories:")
    for chroma_dir in chroma_dirs:
        print(f"   - {chroma_dir}")
    print()
    
    # Check what agents would be created
    print("3. Testing agent creation:")
    chatbot = MultiAgentChatbot()
    
    # Discover PDFs
    pdf_files = chatbot.discover_pdfs()
    print(f"   PDF files discovered: {len(pdf_files)}")
    
    # Discover existing agents
    existing_agents = chatbot.discover_existing_agents()
    print(f"   Existing agents discovered: {len(existing_agents)}")
    for name in existing_agents.keys():
        print(f"   - {name}")
    
    # Create agents
    num_agents = chatbot.create_agents()
    print(f"   Total agents created: {num_agents}")
    print()
    
    # List all agents
    print("4. All agents:")
    agents_info = chatbot.list_agents()
    for name, info in agents_info.items():
        status = "Ready (from cache)" if info['has_vectorstore'] else "Not initialized"
        print(f"   - {name}: {status}")
        print(f"     PDF: {os.path.basename(info['pdf_path'])}")
        print(f"     Vector store: {info['vectorstore_path']}")
    print()
    
    # Check for orphaned vector stores
    print("5. Checking for orphaned vector stores:")
    orphaned_stores = []
    for chroma_dir in chroma_dirs:
        agent_name = chroma_dir.replace("chroma_db_", "").replace("_", " ")
        if agent_name not in agents_info:
            orphaned_stores.append(chroma_dir)
    
    if orphaned_stores:
        print(f"   Found {len(orphaned_stores)} orphaned vector stores:")
        for store in orphaned_stores:
            print(f"   - {store}")
        print("   These stores don't have corresponding PDF files.")
    else:
        print("   No orphaned vector stores found.")
    print()
    
    # Summary
    print("=== Summary ===")
    print(f"PDF files: {len(pdf_files)}")
    print(f"Vector stores: {len(chroma_dirs)}")
    print(f"Total agents: {num_agents}")
    print(f"Orphaned stores: {len(orphaned_stores)}")
    
    if num_agents > len(pdf_files):
        print(f"\n⚠️  ISSUE: More agents ({num_agents}) than PDF files ({len(pdf_files)})")
        if orphaned_stores:
            print("   This is likely due to orphaned vector stores from previous tests.")
            print("   Solution: Delete orphaned vector store directories:")
            for store in orphaned_stores:
                print(f"   rm -rf {store}")
    else:
        print(f"\n✅ All good: {num_agents} agents for {len(pdf_files)} PDF files")

if __name__ == "__main__":
    debug_agent_creation() 