# Simple inefficient code that should trigger optimizations
def process_data(data):
    result = []
    for i in range(len(data)):
        result.append(data[i] * 2)
    return result

def calculate_total(numbers):
    total = 0
    for i in range(len(numbers)):
        total = total + numbers[i]
    return total

def build_string(items):
    output = ""
    for i in range(len(items)):
        output = output + str(items[i])
    return output

def filter_evens(nums):
    evens = []
    for i in range(len(nums)):
        if nums[i] % 2 == 0:
            evens.append(nums[i])
    return evens

