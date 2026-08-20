import os

replacements = [
    ('padding: 50px 16px 80px;', 'padding: 40px 16px 20px;'),
    ('padding:50px 16px 80px;', 'padding: 40px 16px 20px;'),
    ('padding:60px 16px 80px;', 'padding: 40px 16px 20px;'),
    ('padding: 60px 16px 80px;', 'padding: 40px 16px 20px;'),
    ('padding: 40px 16px 80px;', 'padding: 40px 16px 20px;'),
    ('padding:40px 16px 80px;', 'padding: 40px 16px 20px;')
]

for fname in os.listdir('.'):
    if not fname.endswith('.html'): continue
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            modified = True
    
    if modified:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)
        print('Updated padding in:', fname)

print('All HTML pages updated!')
