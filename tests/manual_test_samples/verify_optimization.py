
import sys
import os

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from app.ml_predictor import green_predictor

def verify_file(filepath, language):
    try:
        with open(filepath, 'r') as f:
            code = f.read()
            
        result = green_predictor.optimize_code(code, language=language)
        optimized_code = result['optimized_code']
        
        if code.strip() == optimized_code.strip():
            print(f"FAIL: {language}")
        else:
            print(f"PASS: {language}")
            print("--- Optimized Code Snippet ---")
            print(optimized_code)
            print("------------------------------")
            
    except Exception as e:
        print(f"ERROR: {language} - {e}")

if __name__ == "__main__":
    # Pass None as language to test auto-detection
    verify_file('tests/manual_test_samples/inefficient.js', None)
    verify_file('tests/manual_test_samples/Inefficient.java', None)
    verify_file('tests/manual_test_samples/inefficient.c', None)
    verify_file('tests/manual_test_samples/inefficient.py', None)
