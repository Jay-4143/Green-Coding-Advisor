
import sys
import os
sys.path.append(os.path.abspath('backend'))
from app.ml_predictor import GrrenCodingAdviser # Typo in class name? No, I check file.

# Check file content
with open('backend/app/ml_predictor.py', 'r') as f:
    content = f.read()
    if 'range\s*\(\s*len' in content:
        print("Regex update FOUND in file.")
    else:
        print("Regex update NOT FOUND in file.")

from app.ml_predictor import green_predictor

code = "    for i in range(len(large_list)):"
print(f"Input: '{code}'")
optimized = green_predictor._optimize_python_code(code)
print(f"Output: '{optimized}'")

code2 = """
    for i in range(len(large_list)):
        val = large_list[i]
"""
print(f"Input 2:\n{code2}")
optimized2 = green_predictor._optimize_python_code(code2)
print(f"Output 2:\n{optimized2}")
