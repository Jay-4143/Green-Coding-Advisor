
import sys
import os
# Add backend to path
sys.path.append(os.path.abspath('backend'))

# Mock torch/transformers if missing to avoid heavy load or errors
import unittest.mock
sys.modules['torch'] = unittest.mock.MagicMock()
sys.modules['transformers'] = unittest.mock.MagicMock()
sys.modules['joblib'] = unittest.mock.MagicMock()

from app.ml_predictor import green_predictor

def test_score(name, code, lang):
    print(f"Analyzing {name} ({lang})...")
    # Force reload of models logic if needed? No, purely heuristic now.
    results = green_predictor.analyze_code(code, lang)
    score = results['metrics']['green_score']
    print(f"  -> Score: {score}")
    return score

# Python Samples
py_inefficient = """
def bad():
    s = ""
    # Inefficient loop
    for i in range(len(items)):
        s += items[i]
"""
py_optimized = """
def good():
    s_parts = []
    # Efficient loop
    for item in items:
        s_parts.append(item)
    s = "".join(s_parts)
"""

# JS Samples
js_inefficient = """
async function bad() {
    for (const item of items) {
        await fetch(item);
    }
    const x = document.getElementById('x');
    x.innerHTML += "<div></div>";
}
"""
js_optimized = """
async function good() {
    await Promise.all(items.map(item => fetch(item)));
    const fragment = document.createDocumentFragment();
}
"""

# Java Samples
java_inefficient = """
public class Bad {
    public void test() {
        String s = "";
        for (int i=0; i<10; i++) {
            s += "test";
        }
    }
}
"""
java_optimized = """
public class Good {
    public void test() {
        StringBuilder sb = new StringBuilder();
        for (int i=0; i<10; i++) {
            sb.append("test");
        }
    }
}
"""

print("\n--- Verifying Green Scores ---")
s1 = test_score("Py Inefficient", py_inefficient, "python")
s2 = test_score("Py Optimized", py_optimized, "python")
if s2 > s1 + 10: print("PASS: Python score Improved significantly")
else: print(f"FAIL: Python score diff too small ({s2-s1})")

s3 = test_score("JS Inefficient", js_inefficient, "javascript")
s4 = test_score("JS Optimized", js_optimized, "javascript")
if s4 > s3 + 10: print("PASS: JS score Improved significantly")
else: print(f"FAIL: JS score diff too small ({s4-s3})")

s5 = test_score("Java Inefficient", java_inefficient, "java")
s6 = test_score("Java Optimized", java_optimized, "java")
if s6 > s5 + 10: print("PASS: Java score Improved significantly")
else: print(f"FAIL: Java score diff too small ({s6-s5})")
