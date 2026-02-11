
import time
import math
import os
import sys

def extremely_inefficient_python():
    print("Running EXTREMELY inefficient Python code...")
    start_time = time.time()
    
    # 1. Very inefficient loop iteration (Pattern: range(len()))
    # Metric: High loop overhead, index lookup cost
    large_list = [i for i in range(50000)]
    result_list = []
    
    print("1. Testing loop inefficiency...")
    for i in range(len(large_list)):
        # Inefficient: retrieving by index instead of iterating directly
        val = large_list[i]
        # Inefficient: append inside loop instead of list comprehension
        result_list.append(val * 2)
        
    # 2. String concatenation hell (Pattern: += in loop)
    # Metric: Huge memory churn creating new string objects
    print("2. Testing string inefficiency...")
    output_string = ""
    words = ["word"] * 5000
    for word in words:
        # Inefficient: creates a new string object every iteration
        output_string += word + " "
        
    # 3. Manual summation (Pattern: loops for math)
    # Metric: Python interpreter overhead vs C-optimized sum()
    print("3. Testing math inefficiency...")
    total = 0
    numbers = [i for i in range(100000)]
    for n in numbers:
        total = total + n
        
    # 4. Nested loops with redundant filtering (Pattern: nested loops)
    # Metric: O(N^2) complexity where O(N) is possible
    print("4. Testing nested loop inefficiency...")
    subset = []
    source_a = [i for i in range(1000)]
    source_b = [i for i in range(1000)]
    
    for a in source_a:
        for b in source_b:
            if a == b:
                subset.append(a)
                
    # 5. Redundant API calls/IO (simulated)
    # Metric: Waiting on IO in serial
    print("5. Testing redundant IO patterns...")
    dummy_files = ["file1", "file2", "file3", "file4", "file5"] * 100
    found_count = 0
    for fname in dummy_files:
        # Inefficient: OS call inside tight loop
        if os.path.exists(fname): 
            found_count += 1
            
    end_time = time.time()
    print(f"Inefficient code finished in {end_time - start_time:.4f} seconds")
    return output_string, total, subset

if __name__ == "__main__":
    extremely_inefficient_python()
