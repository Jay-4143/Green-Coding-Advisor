
import re

line = "    for i in range(len(large_list)):"
stripped = line.strip()

print(f"Line: '{stripped}'")

regex = r'for\s+(\w+)\s+in\s+range\s*\(\s*len\s*\(\s*(\w+)\s*\)\s*\)'
match = re.search(regex, stripped)

if match:
    print("MATCH!")
    print(match.groups())
else:
    print("NO MATCH")
