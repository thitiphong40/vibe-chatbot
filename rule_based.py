class RuleBasedHandler:
    def __init__(self):
        self.rules = {
            "hello": "Hello! How can I help you today?",
            "hi": "Hi there! What can I do for you?",
            "bye": "Goodbye! Have a great day!",
            "thanks": "You're welcome!",
            "help": "I can help you with:\n1. Answering questions about documents\n2. General conversation\n3. Specific queries based on rules",
        }
        
    def get_response(self, query):
        """Get response based on rules"""
        query = query.lower().strip()
        
        # Check for exact matches
        if query in self.rules:
            return self.rules[query]
            
        # Check for partial matches
        for key, response in self.rules.items():
            if key in query:
                return response
                
        return None  # No rule matched 