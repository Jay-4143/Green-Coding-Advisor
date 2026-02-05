# Inefficient Python Code for Testing Green Coding Advisor
# This code intentionally contains multiple inefficiencies to test the optimization system

def process_data(data_list):
    """Process a list of numbers with multiple inefficiencies"""
    result = []
    
    # Inefficiency 1: Using range(len()) instead of direct iteration
    for i in range(len(data_list)):
        result.append(data_list[i] * 2)
    
    return result

def calculate_sum(numbers):
    """Calculate sum using inefficient method"""
    total = 0
    # Inefficiency 2: Manual sum instead of built-in sum()
    for i in range(len(numbers)):
        total = total + numbers[i]
    return total

def find_max_value(values):
    """Find maximum value inefficiently"""
    max_val = values[0]
    # Inefficiency 3: Using range(len()) for iteration
    for i in range(len(values)):
        if values[i] > max_val:
            max_val = values[i]
    return max_val

def build_string(items):
    """Build string using inefficient concatenation"""
    output = ""
    # Inefficiency 4: String concatenation in loop
    for i in range(len(items)):
        output = output + str(items[i]) + ", "
    return output

def filter_even_numbers(nums):
    """Filter even numbers inefficiently"""
    evens = []
    # Inefficiency 5: Using range(len()) and manual filtering
    for i in range(len(nums)):
        if nums[i] % 2 == 0:
            evens.append(nums[i])
    return evens

def process_matrix(matrix):
    """Process 2D matrix with nested loops"""
    result = []
    # Inefficiency 6: Nested loops with range(len())
    for i in range(len(matrix)):
        row = []
        for j in range(len(matrix[i])):
            row.append(matrix[i][j] * 2)
        result.append(row)
    return result

def count_occurrences(data, target):
    """Count occurrences inefficiently"""
    count = 0
    # Inefficiency 7: Manual counting instead of built-in methods
    for i in range(len(data)):
        if data[i] == target:
            count = count + 1
    return count

def combine_lists(list1, list2):
    """Combine lists inefficiently"""
    combined = []
    # Inefficiency 8: Manual list combination
    for i in range(len(list1)):
        combined.append(list1[i])
    for i in range(len(list2)):
        combined.append(list2[i])
    return combined

def square_numbers(numbers):
    """Square numbers with redundant computation"""
    squared = []
    # Inefficiency 9: Redundant operations and range(len())
    for i in range(len(numbers)):
        num = numbers[i]
        squared.append(num * num)
    return squared

def main():
    """Main function demonstrating inefficiencies"""
    # Sample data
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    
    # Call inefficient functions
    processed = process_data(data)
    total = calculate_sum(data)
    maximum = find_max_value(data)
    string_result = build_string(data)
    evens = filter_even_numbers(data)
    matrix_result = process_matrix(matrix)
    count = count_occurrences(data, 5)
    combined = combine_lists([1, 2, 3], [4, 5, 6])
    squared = square_numbers(data)
    
    print("Processed:", processed)
    print("Sum:", total)
    print("Max:", maximum)
    print("String:", string_result)
    print("Evens:", evens)
    print("Matrix:", matrix_result)
    print("Count of 5:", count)
    print("Combined:", combined)
    print("Squared:", squared)

if __name__ == "__main__":
    main()

