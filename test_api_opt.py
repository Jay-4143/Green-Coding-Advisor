import requests, json

code = """def process_data(data):
    result = []
    for i in range(len(data)):
        result.append(data[i] * 2)
    return result

def calculate_sum(numbers):
    total = 0
    for i in range(len(numbers)):
        total = total + numbers[i]
    return total
"""

r = requests.post("http://localhost:8000/submissions/optimize", json={"code": code, "language": "python", "region": "usa"})
d = r.json()
print("STATUS:", r.status_code)
print()
print("=== ORIGINAL ===")
print(d.get("original_code", "")[:200])
print()
print("=== OPTIMIZED ===")
print(d.get("optimized_code", "")[:200])
print()
changed = d.get("original_code", "").strip() != d.get("optimized_code", "").strip()
print("CODE CHANGED:", changed)
t = d.get("comparison_table", {})
gs = t.get("green_score", {})
print("Green Score:", gs.get("original"), "->", gs.get("optimized"), "(+{})".format(gs.get("improvement")))
