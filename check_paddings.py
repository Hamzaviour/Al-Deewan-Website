import os
import re

for fname in os.listdir('.'):
    if not fname.endswith('.html'): continue
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    matches = re.findall(r'padding[^;\"\']*?(?:80px|100px|120px)[^;\"\']*', content)
    if matches:
        print(fname, '->', matches)
