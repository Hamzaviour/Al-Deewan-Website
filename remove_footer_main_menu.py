import os
import re

pattern = re.compile(
    r'\s*(?:<!--\s*Main\s*Menu\s*-->\s*)?<div>\s*<h3\s+class="footer-heading">\s*MAIN MENU\s*</h3>\s*<ul\s+class="footer-links">.*?</ul>\s*</div>',
    re.DOTALL | re.IGNORECASE
)

for fname in os.listdir('.'):
    if not fname.endswith('.html'): continue
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'MAIN MENU' in content and 'footer-heading' in content:
        new_content = pattern.sub('', content)
        if new_content != content:
            with open(fname, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print('Removed footer MAIN MENU from:', fname)
        else:
            print('Pattern did not match directly in:', fname)

print('Done removing MAIN MENU from all footers!')
