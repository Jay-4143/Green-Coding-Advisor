# Already Optimal Python Code - Should Show Zero Improvements
# This code uses best practices and should not be optimized further

def process_data(data_list):
    """Process a list of numbers using list comprehension"""
    return [item * 2 for item in data_list]

def calculate_sum(numbers):
    """Calculate sum using built-in function"""
    return sum(numbers)

def find_max_value(values):
    """Find maximum value using built-in function"""
    return max(values)

def build_string(items):
    """Build string using join method"""
    return ", ".join(str(item) for item in items)

def filter_even_numbers(nums):
    """Filter even numbers using list comprehension"""
    return [num for num in nums if num % 2 == 0]

def process_matrix(matrix):
    """Process 2D matrix using nested list comprehension"""
    return [[cell * 2 for cell in row] for row in matrix]

def count_occurrences(data, target):
    """Count occurrences using built-in method"""
    return data.count(target)

def combine_lists(list1, list2):
    """Combine lists using addition operator"""
    return list1 + list2

def square_numbers(numbers):
    """Square numbers using list comprehension"""
    return [num * num for num in numbers]

def main():
    """Main function with optimal code patterns"""
    # Sample data
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    
    # Call optimal functions
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

