
import time

def inefficient_python_code():
    print("Running inefficient Python code...")
    start_time = time.time()
    
    # 1. Inefficient loop with range(len())
    items = [i for i in range(100000)]
    result = []
    for i in range(len(items)):
        result.append(items[i] * 2)
        
    # 2. String concatenation in loop
    s = ""
    for i in range(1000):
        s += str(i)
        
    # 3. Manual summation
    total = 0
    numbers = [i for i in range(100000)]
    for n in numbers:
        total += n
        
    end_time = time.time()
    print(f"Inefficient code took: {end_time - start_time:.4f} seconds")
    return result, s, total

def efficient_python_code():
    print("Running efficient Python code...")
    start_time = time.time()
    
    # 1. Direct iteration (Pythonic)
    items = [i for i in range(100000)]
    result = []
    for item in items:
        result.append(item * 2)
        
    # Or even better: List Comprehension
    result_comp = [item * 2 for item in items]
        
    # 2. String join
    s = "".join(str(i) for i in range(1000))
        
    # 3. Built-in sum
    numbers = [i for i in range(100000)]
    total = sum(numbers)
        
    end_time = time.time()
    print(f"Efficient code took: {end_time - start_time:.4f} seconds")
    return result, s, total

if __name__ == "__main__":
    inefficient_python_code()
    efficient_python_code()
