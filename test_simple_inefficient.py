# Simple Inefficient Python Code for Quick Testing
# Copy and paste this into your website to test the optimization system

def process_data(data):
    """Inefficient: range(len()) with append()"""
    result = []
    for i in range(len(data)):
        result.append(data[i] * 2)
    return result

def calculate_sum(numbers):
    """Inefficient: Manual sum with range(len())"""
    total = 0
    for i in range(len(numbers)):
        total = total + numbers[i]
    return total

def filter_evens(nums):
    """Inefficient: range(len()) with conditional append()"""
    evens = []
    for i in range(len(nums)):
        if nums[i] % 2 == 0:
            evens.append(nums[i])
    return evens

def build_string(items):
    """Inefficient: String concatenation in loop"""
    output = ""
    for i in range(len(items)):
        output = output + str(items[i])
    return output

def find_max(values):
    """Inefficient: Manual max finding"""
    max_val = values[0]
    for i in range(len(values)):
        if values[i] > max_val:
            max_val = values[i]
    return max_val

