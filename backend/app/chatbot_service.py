import logging
import subprocess
import sys
import os
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


# ── Built-in Green Coding Knowledge Base ──────────────────────────────────────
# Used as fallback when Ollama is not available
GREEN_CODING_KB: Dict[str, Dict[str, str]] = {
    "loop": {
        "answer": """**Loop Optimization for Green Coding**

Loops are one of the biggest energy consumers in software. Here are key optimizations:

1. **Avoid index-based iteration** — Use direct iteration instead of `range(len())`:
```python
# ❌ Inefficient
for i in range(len(items)):
    process(items[i])

# ✅ Efficient
for item in items:
    process(item)
```

2. **Use list comprehensions** (Python) or array methods (JS):
```python
# ❌ Loop with append
result = []
for x in data:
    result.append(x * 2)

# ✅ List comprehension
result = [x * 2 for x in data]
```

3. **Avoid I/O inside loops** — batch operations instead.

**🌿 Green Impact:** Optimized loops can reduce CPU cycles by 30-60%, directly lowering energy consumption and carbon emissions.""",
        "topics": ["loop_optimization", "algorithm_complexity"]
    },
    "memory": {
        "answer": """**Memory Optimization for Sustainable Code**

Efficient memory usage reduces both RAM consumption and energy:

1. **Use generators** instead of lists for large datasets:
```python
# ❌ Creates full list in memory
squares = [x**2 for x in range(1000000)]

# ✅ Generator — lazy evaluation
squares = (x**2 for x in range(1000000))
```

2. **Close resources promptly** with context managers:
```python
with open('file.txt') as f:
    data = f.read()
```

3. **Avoid unnecessary copies** — use in-place operations when safe.

**🌿 Green Impact:** Lower memory usage means less RAM power draw, reducing energy by 10-25%.""",
        "topics": ["memory_usage"]
    },
    "complexity": {
        "answer": """**Algorithm Complexity & Energy Impact**

Big-O complexity directly correlates with energy consumption:

| Complexity | Energy Impact | Example |
|-----------|--------------|---------|
| O(1) | Minimal | Hash lookup |
| O(log n) | Low | Binary search |
| O(n) | Moderate | Linear scan |
| O(n²) | High | Nested loops |
| O(2ⁿ) | Extreme | Brute force |

**Key Principles:**
- Choose O(n log n) sorting over O(n²) — saves ~40% energy
- Use hash sets for lookups instead of lists — O(1) vs O(n)
- Prefer iterative over recursive solutions to reduce stack usage

**🌿 Green Impact:** Reducing complexity from O(n²) to O(n log n) can cut energy usage by 50%+ for large datasets.""",
        "topics": ["algorithm_complexity"]
    },
    "string": {
        "answer": """**String Optimization Techniques**

String operations are often hidden energy wasters:

**Python:**
```python
# ❌ String concatenation in loop (creates new object each time)
result = ""
for item in items:
    result += str(item)

# ✅ Use join()
result = "".join(str(item) for item in items)
```

**Java:**
```java
// ❌ String += in loop
String result = "";
for (String s : items) result += s;

// ✅ StringBuilder
StringBuilder sb = new StringBuilder();
for (String s : items) sb.append(s);
```

**🌿 Green Impact:** join()/StringBuilder are 10-100x faster for large concatenations, saving significant CPU cycles.""",
        "topics": ["loop_optimization", "memory_usage"]
    },
    "async": {
        "answer": """**Async/Parallel Patterns for Green Coding**

Sequential I/O wastes time and energy. Use parallel execution:

**JavaScript:**
```javascript
// ❌ Sequential — slow & energy-wasteful
for (const url of urls) {
    const data = await fetch(url);
}

// ✅ Parallel — fast & efficient
const results = await Promise.all(
    urls.map(url => fetch(url))
);
```

**Python:**
```python
# ✅ Use asyncio.gather for parallel I/O
results = await asyncio.gather(*[fetch(url) for url in urls])
```

**🌿 Green Impact:** Parallel I/O can reduce wall-clock time by 80%+, meaning less idle CPU power draw.""",
        "topics": ["loop_optimization"]
    },
    "data_structure": {
        "answer": """**Choosing Energy-Efficient Data Structures**

The right data structure can dramatically reduce energy:

| Operation | List | Set/Dict | Impact |
|----------|------|----------|--------|
| Lookup | O(n) | O(1) | 100x faster |
| Insert | O(1)* | O(1) | Similar |
| Sort | O(n log n) | N/A | Use sorted containers |

**Guidelines:**
- Use `set` for membership testing instead of `list`
- Use `dict` for key-value lookups
- Use `deque` for queue operations (not list)
- In Java, prefer `HashMap` over `TreeMap` for most lookups

**🌿 Green Impact:** Using O(1) lookups vs O(n) can reduce energy by 90%+ for large datasets.""",
        "topics": ["data_structures"]
    },
    "green": {
        "answer": """**What is Green Coding?**

Green coding is the practice of writing software that minimizes:
- **Energy consumption** (CPU cycles, memory usage)
- **Carbon footprint** (CO₂ emissions from computation)
- **Resource waste** (unnecessary I/O, network calls)

**Core Principles:**
1. ⚡ **Efficiency First** — Optimize algorithms and data structures
2. 🔄 **Reduce Redundancy** — Cache results, batch operations
3. 📦 **Minimize Resources** — Use generators, close connections
4. 🌍 **Measure Impact** — Track energy and CO₂ metrics

**Quick Wins:**
- Replace nested loops with built-in functions
- Use list comprehensions instead of loops with append
- Batch I/O operations
- Choose efficient data structures (set/dict over list)

**🌿 Green Impact:** Following these practices can reduce code energy consumption by 30-70%.""",
        "topics": ["carbon_tracking"]
    },
    "language": {
        "answer": """**Most Energy-Efficient Programming Languages**

According to research (SLE 2017 study), languages ranked by energy efficiency:

1. 🥇 **C** — Most efficient (baseline)
2. 🥈 **Rust** — ~1.03x C
3. 🥉 **C++** — ~1.34x C
4. **Java** — ~1.98x C
5. **Go** — ~3.23x C
6. **C#** — ~3.14x C
7. **JavaScript** — ~4.45x C
8. **TypeScript** — ~4.45x C (compiled to JS)
9. **Python** — ~75.88x C

**Key Takeaway:** Python is great for prototyping but consider compiled languages for production-critical, high-frequency code paths.

**🌿 Green Impact:** Choosing the right language for the right task can reduce energy by 10-70x.""",
        "topics": ["carbon_tracking"]
    },
}


def _find_kb_answer(message: str) -> Optional[Dict]:
    """Find the best matching answer from the knowledge base."""
    message_lower = message.lower()
    
    # Score each topic by keyword matches
    best_score = 0
    best_key = None
    
    keyword_map = {
        "loop": ["loop", "for", "while", "iteration", "iterate", "nested", "range(len"],
        "memory": ["memory", "ram", "generator", "heap", "stack", "leak", "garbage"],
        "complexity": ["complexity", "big o", "big-o", "algorithm", "o(n", "time complexity", "performance"],
        "string": ["string", "concatenat", "concat", "join", "stringbuilder", "+="],
        "async": ["async", "await", "parallel", "promise", "concurrent", "batch"],
        "data_structure": ["data structure", "set", "dict", "hash", "array", "list", "map", "queue", "deque"],
        "green": ["green coding", "green code", "sustainable", "what is green", "energy efficient", "carbon", "eco"],
        "language": ["language", "efficient language", "best language", "python vs", "c vs", "fastest"],
    }
    
    for key, keywords in keyword_map.items():
        score = sum(1 for kw in keywords if kw in message_lower)
        if score > best_score:
            best_score = score
            best_key = key
    
    if best_key and best_score > 0:
        kb_entry = GREEN_CODING_KB[best_key]
        return {
            "answer": kb_entry["answer"],
            "topics": kb_entry.get("topics", []),
        }
    
    return None


class GreenCodingChatbot:
    """AI-powered chatbot using LLaMA-2 via Ollama with built-in fallback"""
    
    SYSTEM_PROMPT = """
You are the **Green Coding Architect**, an advanced AI assistant powered by LLaMA-2, dedicated to sustainable software engineering.
Your goal is to guide developers in writing code that reduces energy consumption, carbon footprint, and computational overhead.

**Your Core Principles:**
1. **Efficiency First**: Always prioritize algorithms with lower Time and Space complexity (Big-O).
2. **Resource Awareness**: Highlight memory usage, CPU cycles, and network bandwidth.
3. **Sustainable Syntax**: Recommend language-specific features that are optimized (e.g., list comprehensions in Python, avoiding unnecessary copies).
4. **Hardware Empathy**: Explain how code decisions affect underlying hardware (battery life, heat generation).

**Response Guidelines:**
- Be concise but educational.
- **Always** provide a brief code example if applicable.
- Conclude with a "Green Impact" statement explaining *why* your advice saves energy.
- Use a professional, encouraging tone.

If the user asks about non-coding topics, politely redirect them to sustainable technology.
"""

    def __init__(self, model_name: str = "llama2"):
        self.model_name = model_name
        self._ollama_available = None  # Cached availability check

    def _check_ollama_available(self) -> bool:
        """Check if Ollama is running and accessible."""
        if self._ollama_available is not None:
            return self._ollama_available
        
        try:
            import ollama
            ollama.list()
            self._ollama_available = True
            logger.info("Ollama is available and connected")
            return True
        except Exception as e:
            self._ollama_available = False
            logger.info(f"Ollama not available: {e}. Using built-in knowledge base.")
            return False

    def answer(self, message: str, context: Optional[Dict] = None) -> Dict[str, any]:
        """Generate a response — tries Ollama first, falls back to KB"""
        
        # Try Ollama first
        if self._check_ollama_available():
            try:
                import ollama
                response = ollama.chat(model=self.model_name, messages=[
                    {'role': 'system', 'content': self.SYSTEM_PROMPT},
                    {'role': 'user', 'content': message},
                ])
                
                answer_text = response['message']['content']
                topics = self._extract_topics(answer_text + " " + message)
                
                return {
                    "answer": answer_text,
                    "suggestions": self._generate_suggestions(answer_text),
                    "related_topics": topics
                }
            except Exception as e:
                logger.warning(f"Ollama call failed: {e}. Falling back to KB.")
                # Reset availability so next call re-checks
                self._ollama_available = None
        
        # Fallback: built-in knowledge base
        kb_result = _find_kb_answer(message)
        
        if kb_result:
            return {
                "answer": kb_result["answer"],
                "suggestions": self._generate_context_suggestions(message),
                "related_topics": kb_result.get("topics", [])
            }
        
        # Generic fallback
        return {
            "answer": """Thanks for your question! Here are some general green coding tips:

**🌱 Top Green Coding Practices:**
1. **Optimize loops** — Use list comprehensions, avoid `range(len())`
2. **Choose efficient data structures** — Sets for lookups, generators for large data
3. **Batch I/O operations** — Minimize disk and network calls
4. **Use built-in functions** — `sum()`, `map()`, `filter()` are C-optimized
5. **Profile before optimizing** — Measure energy impact with tools like CodeCarbon

Try asking me about specific topics like:
- "How to optimize loops?"
- "What are energy-efficient data structures?"
- "Explain Big-O complexity impact on energy"

**🌿 Green Impact:** Following these practices can reduce code energy consumption by 30-70%.""",
            "suggestions": [
                "How to optimize a nested loop?",
                "What are the most energy-efficient languages?",
                "Explain Big-O complexity impact on energy.",
                "How to reduce memory usage in Python?"
            ],
            "related_topics": ["general"]
        }

    def _extract_topics(self, text: str) -> List[str]:
        """Extract green coding topics from text"""
        text_lower = text.lower()
        topics = set()
        if "loop" in text_lower: topics.add("loop_optimization")
        if "memory" in text_lower or "ram" in text_lower: topics.add("memory_usage")
        if "complexity" in text_lower or "big o" in text_lower: topics.add("algorithm_complexity")
        if "data structure" in text_lower: topics.add("data_structures")
        if "carbon" in text_lower or "emission" in text_lower: topics.add("carbon_tracking")
        return list(topics)

    def _generate_suggestions(self, context_text: str) -> List[str]:
        """Generate static follow-up suggestions based on context"""
        base_suggestions = [
            "How can I measure my code's energy?",
            "What are the most energy-efficient languages?",
            "Explain Python list comprehension efficiency."
        ]
        return base_suggestions
    
    def _generate_context_suggestions(self, message: str) -> List[str]:
        """Generate context-aware follow-up suggestions"""
        msg_lower = message.lower()
        
        if "loop" in msg_lower:
            return [
                "How to optimize nested loops?",
                "When should I use list comprehensions?",
                "What's the energy cost of O(n²) vs O(n)?"
            ]
        elif "memory" in msg_lower:
            return [
                "When to use generators vs lists?",
                "How to profile memory usage?",
                "What causes memory leaks?"
            ]
        elif "string" in msg_lower:
            return [
                "Best practices for string handling in Java?",
                "How does join() save energy?",
                "String interning explained"
            ]
        else:
            return [
                "How to optimize loops for energy?",
                "What are green coding best practices?",
                "How to measure code's carbon footprint?"
            ]


def _try_start_ollama():
    """Attempt to start Ollama server in the background."""
    try:
        if sys.platform == "win32":
            subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        else:
            subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        logger.info("Ollama server started in background")
    except FileNotFoundError:
        logger.info("Ollama not installed — chatbot will use built-in knowledge base")
    except Exception as e:
        logger.info(f"Could not start Ollama: {e} — chatbot will use built-in knowledge base")


# Try to start Ollama on import
_try_start_ollama()

# Global chatbot instance
green_chatbot = GreenCodingChatbot()
