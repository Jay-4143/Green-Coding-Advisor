# Inefficient Python Code for Testing Green Coding Advisor
# This code contains multiple anti-patterns and inefficiencies

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
    # Bad: Manual sum calculation with range(len())
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
    # Bad: Manual counting with range(len())
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
    # Bad: Manual reversal with range(len())
    for i in range(len(items) - 1, -1, -1):
        reversed_items.append(items[i])
    return reversed_items

def remove_duplicates(data):
    """Remove duplicates inefficiently - O(n²) complexity"""
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

def find_common_elements(list1, list2):
    """Find common elements inefficiently"""
    common = []
    # Bad: Nested loops - O(n²) complexity
    for i in range(len(list1)):
        for j in range(len(list2)):
            if list1[i] == list2[j]:
                common.append(list1[i])
                break
    return common

def calculate_average(numbers):
    """Calculate average inefficiently"""
    total = 0
    count = 0
    # Bad: Manual calculation instead of built-in functions
    for i in range(len(numbers)):
        total = total + numbers[i]
        count = count + 1
    if count > 0:
        return total / count
    return 0

def find_min_max(values):
    """Find min and max inefficiently"""
    if len(values) == 0:
        return None, None
    min_val = values[0]
    max_val = values[0]
    # Bad: Two separate passes could be one
    for i in range(len(values)):
        if values[i] < min_val:
            min_val = values[i]
    for i in range(len(values)):
        if values[i] > max_val:
            max_val = values[i]
    return min_val, max_val

def check_if_all_positive(numbers):
    """Check if all numbers are positive inefficiently"""
    all_positive = True
    # Bad: Doesn't short-circuit, continues even after finding False
    for i in range(len(numbers)):
        if numbers[i] <= 0:
            all_positive = False
    return all_positive

def multiply_matrices(matrix1, matrix2):
    """Multiply matrices with triple nested loops"""
    result = []
    # Bad: Triple nested loops - O(n³) complexity
    for i in range(len(matrix1)):
        row = []
        for j in range(len(matrix2[0])):
            sum_val = 0
            for k in range(len(matrix2)):
                sum_val = sum_val + matrix1[i][k] * matrix2[k][j]
            row.append(sum_val)
        result.append(row)
    return result

def flatten_list(nested_list):
    """Flatten nested list inefficiently"""
    flat = []
    # Bad: Nested loops with manual appending
    for i in range(len(nested_list)):
        for j in range(len(nested_list[i])):
            flat.append(nested_list[i][j])
    return flat

def count_word_occurrences(text_list, word):
    """Count word occurrences inefficiently"""
    count = 0
    # Bad: Manual counting with range(len())
    for i in range(len(text_list)):
        if text_list[i] == word:
            count = count + 1
    return count

def get_unique_items(items):
    """Get unique items inefficiently"""
    unique = []
    # Bad: O(n²) complexity for uniqueness check
    for i in range(len(items)):
        is_unique = True
        for j in range(len(unique)):
            if items[i] == unique[j]:
                is_unique = False
                break
        if is_unique:
            unique.append(items[i])
    return unique

def main():
    """Main function demonstrating inefficiencies"""
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    matrix1 = [[1, 2], [3, 4]]
    matrix2 = [[5, 6], [7, 8]]
    duplicates = [1, 2, 2, 3, 3, 3, 4, 5, 5, 6]
    nested = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
    
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
    common = find_common_elements([1, 2, 3], [2, 3, 4])
    avg = calculate_average(numbers)
    min_val, max_val = find_min_max(numbers)
    all_pos = check_if_all_positive([1, 2, 3, -1])
    flat = flatten_list(nested)
    word_count = count_word_occurrences(['hello', 'world', 'hello'], 'hello')
    unique = get_unique_items(duplicates)
    
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
    print("Common:", common)
    print("Average:", avg)
    print("Min:", min_val, "Max:", max_val)
    print("All Positive:", all_pos)
    print("Flattened:", flat)
    print("Word Count:", word_count)
    print("Unique Items:", unique)

if __name__ == "__main__":
    main()
