from typing import Dict, List, Optional
import re

class GreenCodingChatbot:
    """AI-powered chatbot for green coding advice"""
    
    def __init__(self):
        self.knowledge_base = self._initialize_knowledge_base()
    
    def _initialize_knowledge_base(self) -> Dict[str, List[str]]:
        """Initialize knowledge base with green coding patterns and answers"""
        return {
            "loop_optimization": [
                "Use list comprehensions instead of loops when possible. They're more efficient and readable.",
                "Avoid nested loops when you can use built-in functions like map(), filter(), or reduce().",
                "Consider using generators for large datasets to save memory.",
                "Use enumerate() instead of range(len()) for better performance."
            ],
            "data_structures": [
                "Use sets for membership testing (O(1) vs O(n) for lists).",
                "Use dictionaries for key-value lookups instead of nested lists.",
                "Choose the right data structure: lists for ordered data, sets for unique items, dicts for mappings.",
                "Avoid creating unnecessary copies of data structures."
            ],
            "memory_usage": [
                "Use generators instead of lists for large datasets to save memory.",
                "Delete variables when they're no longer needed using del.",
                "Use __slots__ in classes to reduce memory footprint.",
                "Avoid global variables when possible."
            ],
            "algorithm_complexity": [
                "Choose algorithms with better time complexity (O(n log n) vs O(n²)).",
                "Use hash tables (dictionaries) for O(1) lookups.",
                "Consider using binary search for sorted data (O(log n) vs O(n)).",
                "Avoid unnecessary iterations over data."
            ],
            "io_operations": [
                "Use context managers (with statements) for file operations.",
                "Read files in chunks for large files instead of loading everything into memory.",
                "Use buffered I/O for better performance.",
                "Close files and connections promptly."
            ],
            "general": [
                "Write efficient code that minimizes CPU and memory usage.",
                "Use built-in functions which are optimized in C.",
                "Profile your code to identify bottlenecks.",
                "Consider using libraries like NumPy for numerical computations.",
                "Avoid premature optimization - measure first, then optimize.",
                "Use appropriate algorithms for your use case.",
                "Cache results when computations are expensive and results are reused.",
                "Minimize database queries and API calls when possible."
            ]
        }
    
    def _extract_keywords(self, message: str) -> List[str]:
        """Extract keywords from user message"""
        message_lower = message.lower()
        keywords = []
        
        # Common patterns
        if any(word in message_lower for word in ["loop", "for", "while", "iterate", "iteration"]):
            keywords.append("loop_optimization")
        if any(word in message_lower for word in ["list", "dict", "set", "array", "data structure", "structure"]):
            keywords.append("data_structures")
        if any(word in message_lower for word in ["memory", "ram", "space", "storage"]):
            keywords.append("memory_usage")
        if any(word in message_lower for word in ["complexity", "algorithm", "big o", "performance", "speed", "fast", "slow"]):
            keywords.append("algorithm_complexity")
        if any(word in message_lower for word in ["file", "read", "write", "io", "input", "output"]):
            keywords.append("io_operations")
        
        return keywords if keywords else ["general"]
    
    def _generate_response(self, message: str, context: Optional[Dict] = None) -> str:
        """Generate a response based on the message and context"""
        keywords = self._extract_keywords(message)
        message_lower = message.lower()
        
        # Specific question patterns
        if "why" in message_lower and "inefficient" in message_lower:
            return "Inefficient code typically uses more CPU cycles and memory. Common issues include: nested loops (O(n²) complexity), unnecessary data copying, using lists instead of sets for lookups, and not leveraging built-in optimized functions. Would you like specific advice on any of these?"
        
        if "which" in message_lower and "data structure" in message_lower:
            return "Choose data structures based on your needs: Use lists for ordered, indexed data. Use sets for unique items and fast membership testing. Use dictionaries for key-value mappings and fast lookups. Use tuples for immutable sequences. Consider memory usage and access patterns when choosing."
        
        if "how" in message_lower and "optimize" in message_lower:
            return "To optimize code: 1) Profile first to find bottlenecks, 2) Use appropriate algorithms (better time complexity), 3) Choose efficient data structures, 4) Leverage built-in functions, 5) Use generators for large datasets, 6) Minimize I/O operations, 7) Cache expensive computations. What specific area would you like to optimize?"
        
        if "list comprehension" in message_lower or "comprehension" in message_lower:
            return "List comprehensions are more efficient than loops because they're optimized in C and avoid Python's function call overhead. Example: [x*2 for x in range(10)] is faster than: result = []; for x in range(10): result.append(x*2). They also use less memory and are more readable."
        
        if "range(len" in message_lower or "index" in message_lower:
            return "Avoid using range(len()) for iteration. Instead, use: 'for item in items:' for direct iteration, or 'for i, item in enumerate(items):' if you need the index. This is more efficient and Pythonic."
        
        # Get relevant answers from knowledge base
        answers = []
        for keyword in keywords:
            answers.extend(self.knowledge_base.get(keyword, []))
        
        if answers:
            # Return the most relevant answer
            return answers[0]
        
        return "I can help you with green coding practices including: loop optimization, data structure selection, memory usage, algorithm complexity, and I/O operations. What specific question do you have?"
    
    def _get_suggestions(self, message: str) -> List[str]:
        """Get related topic suggestions"""
        message_lower = message.lower()
        suggestions = []
        
        if "loop" in message_lower:
            suggestions.append("How to optimize nested loops?")
            suggestions.append("When to use list comprehensions?")
        elif "memory" in message_lower:
            suggestions.append("How to reduce memory usage?")
            suggestions.append("When to use generators?")
        elif "data structure" in message_lower:
            suggestions.append("Which data structure to use?")
            suggestions.append("Sets vs lists for lookups?")
        else:
            suggestions.append("How to optimize loops?")
            suggestions.append("Which data structure is most efficient?")
            suggestions.append("How to reduce memory usage?")
        
        return suggestions[:3]
    
    def answer(self, message: str, context: Optional[Dict] = None) -> Dict[str, any]:
        """Answer a user question"""
        response = self._generate_response(message, context)
        suggestions = self._get_suggestions(message)
        
        # Extract related topics
        keywords = self._extract_keywords(message)
        related_topics = list(set(keywords))
        
        return {
            "answer": response,
            "suggestions": suggestions,
            "related_topics": related_topics
        }


# Global chatbot instance
green_chatbot = GreenCodingChatbot()

