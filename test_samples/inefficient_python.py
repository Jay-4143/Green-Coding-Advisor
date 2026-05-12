"""
Inefficient Python Code — For Green Coding Advisor Testing
This code contains several known anti-patterns that the optimizer should detect.
"""

# 1. Index-based iteration with range(len())
def process_items(items):
    result = []
    for i in range(len(items)):
        if items[i] > 0:
            result.append(items[i] * 2)
    return result


# 2. String concatenation in loop (creates new string each time)
def build_csv(rows):
    output = ""
    for row in rows:
        line = ""
        for item in row:
            line += str(item) + ","
        output += line + "\n"
    return output


# 3. Manual summation instead of built-in sum()
def calculate_total(numbers):
    total = 0
    for num in numbers:
        total += num
    average = total / len(numbers)
    return total, average


# 4. File I/O inside loop (should batch read)
def count_lines_in_files(file_paths):
    total_lines = 0
    for path in file_paths:
        f = open(path, 'r')
        content = f.read()
        f.close()
        lines = content.split('\n')
        count = 0
        for line in lines:
            if len(line) > 0:
                count += 1
        total_lines += count
    return total_lines


# 5. Nested loop that could be a list comprehension
def get_even_squares(numbers):
    result = []
    for num in numbers:
        square = num * num
        if square % 2 == 0:
            result.append(square)
    return result


# 6. Dictionary iteration without .items()
def merge_configs(default_config, user_config):
    merged = {}
    for key in default_config.keys():
        merged[key] = default_config[key]
    for key in user_config.keys():
        merged[key] = user_config[key]
    return merged


# 7. Repeated computation in loop
def find_duplicates(data):
    duplicates = []
    for i in range(len(data)):
        for j in range(len(data)):
            if i != j and data[i] == data[j]:
                if data[i] not in duplicates:
                    duplicates.append(data[i])
    return duplicates


if __name__ == "__main__":
    items = [1, -2, 3, -4, 5, 6, -7, 8, 9, 10]
    print("Processed:", process_items(items))
    
    rows = [["Name", "Age", "City"], ["Alice", 30, "NYC"], ["Bob", 25, "LA"]]
    print("CSV:\n", build_csv(rows))
    
    numbers = [10, 20, 30, 40, 50]
    total, avg = calculate_total(numbers)
    print(f"Total: {total}, Average: {avg}")
    
    print("Even squares:", get_even_squares(range(1, 11)))
    
    print("Duplicates:", find_duplicates([1, 2, 3, 2, 4, 3, 5]))
