#!/usr/bin/env python3
"""
Test runner for multi-agent chatbot tests
"""

import sys
import os
import subprocess

def run_test(test_file):
    """Run a specific test file"""
    print(f"\n{'='*50}")
    print(f"Running: {test_file}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=False, 
                              text=True, 
                              cwd=os.path.dirname(os.path.abspath(__file__)))
        if result.returncode == 0:
            print(f"✅ {test_file} completed successfully")
        else:
            print(f"❌ {test_file} failed")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running {test_file}: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Multi-Agent Chatbot Test Suite")
    print("="*50)
    
    # List of test files to run
    test_files = [
        "test_multi_agent.py",
        "test_loading.py",
        "debug_agents.py"
    ]
    
    success_count = 0
    total_count = len(test_files)
    
    for test_file in test_files:
        if run_test(test_file):
            success_count += 1
    
    print(f"\n{'='*50}")
    print(f"Test Results: {success_count}/{total_count} tests passed")
    print(f"{'='*50}")
    
    if success_count == total_count:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 