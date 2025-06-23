#!/usr/bin/env python3
"""
Test script for the Multi-Agent PDF Chatbot system
"""

import sys
import os

# Add parent directory to path to import multi_agent_chatbot
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from multi_agent_chatbot import MultiAgentChatbot

def test_multi_agent_system():
    """Test the multi-agent system functionality"""
    
    print("=== Multi-Agent PDF Chatbot Test ===\n")
    
    # Initialize the multi-agent chatbot
    chatbot = MultiAgentChatbot()
    
    # Step 1: Discover PDFs
    print("1. Discovering PDF files...")
    pdf_files = chatbot.discover_pdfs()
    print(f"Found {len(pdf_files)} PDF files")
    for pdf in pdf_files:
        print(f"   - {os.path.basename(pdf)}")
    print()
    
    # Step 2: Create agents
    print("2. Creating agents...")
    num_agents = chatbot.create_agents()
    print(f"Created {num_agents} agents")
    print()
    
    # Step 3: List agents
    print("3. Agent information:")
    agents_info = chatbot.list_agents()
    for name, info in agents_info.items():
        print(f"   - {name}: {'Initialized' if info['is_initialized'] else 'Not initialized'}")
    print()
    
    # Step 4: Process documents (this will take some time)
    print("4. Processing documents for all agents...")
    print("(This may take a few minutes depending on PDF sizes)")
    chatbot.process_all_documents()
    print()
    
    # Step 5: Test responses
    print("5. Testing agent responses...")
    
    # Test general query
    print("\nTesting general query:")
    response = chatbot.get_response("Hello, how are you?")
    print(f"Response: {response}")
    
    # Test specific agent queries
    for agent_name in chatbot.agents.keys():
        print(f"\nTesting agent '{agent_name}':")
        response = chatbot.get_agent_response(agent_name, "What is this document about?")
        print(f"Response: {response[:200]}...")  # Show first 200 characters
    
    print("\n=== Test completed ===")

if __name__ == "__main__":
    test_multi_agent_system() 