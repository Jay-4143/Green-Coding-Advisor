# Very Inefficient Python Code - Should Get Low Green Score
# Contains multiple anti-patterns and inefficiencies

def process_large_dataset(data):
    """Process data with multiple inefficiencies"""
    result = []
    # Bad: range(len()) instead of direct iteration
    for i in range(len(data)):
        # Bad: Manual append instead of list comprehension
        result.append(data[i] * 2 + 1)
    return result

def calculate_total(numbers):
    """Calculate total inefficiently"""
    total = 0
    # Bad: Manual sum calculation
    for i in range(len(numbers)):
        total = total + numbers[i]
    return total

def find_maximum(values):
    """Find maximum inefficiently"""
    if len(values) == 0:
        return None
    max_val = values[0]
    # Bad: range(len()) iteration
    for i in range(len(values)):
        if values[i] > max_val:
            max_val = values[i]
    return max_val

def create_output_string(items):
    """Create string with inefficient concatenation"""
    output = ""
    # Bad: String concatenation in loop
    for i in range(len(items)):
        output = output + str(items[i])
        if i < len(items) - 1:
            output = output + ", "
    return output

def get_even_numbers(nums):
    """Get even numbers inefficiently"""
    evens = []
    # Bad: range(len()) and manual filtering
    for i in range(len(nums)):
        if nums[i] % 2 == 0:
            evens.append(nums[i])
    return evens

def process_2d_array(arr):
    """Process 2D array with nested loops"""
    output = []
    # Bad: Nested range(len()) loops
    for i in range(len(arr)):
        row = []
        for j in range(len(arr[i])):
            row.append(arr[i][j] * 3)
        output.append(row)
    return output

def count_items(data, item):
    """Count items manually"""
    count = 0
    # Bad: Manual counting
    for i in range(len(data)):
        if data[i] == item:
            count = count + 1
    return count

def merge_arrays(arr1, arr2):
    """Merge arrays manually"""
    merged = []
    # Bad: Manual array merging
    for i in range(len(arr1)):
        merged.append(arr1[i])
    for i in range(len(arr2)):
        merged.append(arr2[i])
    return merged

def compute_squares(numbers):
    """Compute squares inefficiently"""
    squares = []
    # Bad: range(len()) and redundant variable
    for i in range(len(numbers)):
        value = numbers[i]
        squares.append(value * value)
    return squares

def filter_positive(numbers):
    """Filter positive numbers inefficiently"""
    positives = []
    # Bad: range(len()) iteration
    for i in range(len(numbers)):
        if numbers[i] > 0:
            positives.append(numbers[i])
    return positives

def reverse_list(items):
    """Reverse list manually"""
    reversed_items = []
    # Bad: Manual reversal
    for i in range(len(items) - 1, -1, -1):
        reversed_items.append(items[i])
    return reversed_items

def multiply_matrices(matrix1, matrix2):
    """Multiply matrices with triple nested loops"""
    result = []
    # Bad: Triple nested loops
    for i in range(len(matrix1)):
        row = []
        for j in range(len(matrix2[0])):
            sum_val = 0
            for k in range(len(matrix2)):
                sum_val = sum_val + matrix1[i][k] * matrix2[k][j]
            row.append(sum_val)
        result.append(row)
    return result

def remove_duplicates(data):
    """Remove duplicates inefficiently"""
    unique = []
    # Bad: O(n²) duplicate checking
    for i in range(len(data)):
        found = False
        for j in range(len(unique)):
            if data[i] == unique[j]:
                found = True
                break
        if not found:
            unique.append(data[i])
    return unique

def main():
    """Main function with many inefficient operations"""
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    matrix1 = [[1, 2], [3, 4]]
    matrix2 = [[5, 6], [7, 8]]
    duplicates = [1, 2, 2, 3, 3, 3, 4, 5, 5, 6]
    
    # Multiple inefficient operations
    processed = process_large_dataset(numbers)
    total = calculate_total(numbers)
    maximum = find_maximum(numbers)
    output_str = create_output_string(numbers)
    evens = get_even_numbers(numbers)
    matrix_result = process_2d_array([numbers[:3], numbers[3:6], numbers[6:9]])
    count = count_items(numbers, 5)
    merged = merge_arrays([1, 2, 3], [4, 5, 6])
    squares = compute_squares(numbers)
    positives = filter_positive([-5, -2, 0, 3, 7, -1, 9])
    reversed_list = reverse_list(numbers)
    multiplied = multiply_matrices(matrix1, matrix2)
    unique_items = remove_duplicates(duplicates)
    
    print("Processed:", processed)
    print("Total:", total)
    print("Maximum:", maximum)
    print("Output String:", output_str)
    print("Evens:", evens)
    print("Matrix:", matrix_result)
    print("Count:", count)
    print("Merged:", merged)
    print("Squares:", squares)
    print("Positives:", positives)
    print("Reversed:", reversed_list)
    print("Multiplied:", multiplied)
    print("Unique:", unique_items)

if __name__ == "__main__":
    main()

