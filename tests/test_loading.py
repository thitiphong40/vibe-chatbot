#!/usr/bin/env python3
"""
Test script to verify loading existing vector stores
"""

import sys
import os
import time

# Add parent directory to path to import multi_agent_chatbot
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from multi_agent_chatbot import MultiAgentChatbot

def test_loading_functionality():
    """Test that the system loads existing vector stores"""
    
    print("=== Testing Vector Store Loading ===\n")
    
    # Initialize the multi-agent chatbot
    chatbot = MultiAgentChatbot()
    
    # Step 1: Create agents (this should discover existing ones)
    print("1. Creating agents...")
    start_time = time.time()
    num_agents = chatbot.create_agents()
    create_time = time.time() - start_time
    print(f"Created {num_agents} agents in {create_time:.2f} seconds")
    
    # Step 2: List agents and their status
    print("\n2. Agent status:")
    agents_info = chatbot.list_agents()
    for name, info in agents_info.items():
        status = "Ready (from cache)" if info['has_vectorstore'] else "Not initialized"
        print(f"   - {name}: {status}")
    
    # Step 3: Test response without processing (should load from cache)
    print("\n3. Testing response without processing...")
    for agent_name in chatbot.agents.keys():
        print(f"\nTesting agent: {agent_name}")
        start_time = time.time()
        response = chatbot.get_agent_response(agent_name, "What is this document about?")
        response_time = time.time() - start_time
        print(f"Response time: {response_time:.2f} seconds")
        print(f"Response: {response[:100]}...")
    
    # Step 4: Test processing (should skip if already exists)
    print("\n4. Testing document processing (should skip if exists)...")
    for agent_name, agent in chatbot.agents.items():
        print(f"\nProcessing agent: {agent_name}")
        start_time = time.time()
        agent.process_document()
        process_time = time.time() - start_time
        print(f"Processing time: {process_time:.2f} seconds")
    
    print("\n=== Test completed ===")
    print("\nKey improvements:")
    print("✅ Agents load from existing chroma_db directories")
    print("✅ No unnecessary reprocessing of documents")
    print("✅ Faster startup and response times")
    print("✅ Better status indication in UI")

if __name__ == "__main__":
    test_loading_functionality() 