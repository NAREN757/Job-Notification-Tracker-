
import os
import codecs

path = r'C:\Users\naren\.gemini\antigravity\scratch\preview.html'

with codecs.open(path, 'r', 'utf-8') as f:
    lines = f.readlines()

new_lines = []
# Keep 0 to 2817 (lines 1-2818)
new_lines.extend(lines[:2818])

# Skip 2818 to 2959 (lines 2819-2960)

# Keep 2960 to 2961 (lines 2961-2962)
new_lines.extend(lines[2960:2962])

# Skip 2962 (line 2963)

# Keep 2963 to End (lines 2964-End)
new_lines.extend(lines[2963:])

with codecs.open(path, 'w', 'utf-8') as f:
    f.writelines(new_lines)

print("Cleaned preview.html")
