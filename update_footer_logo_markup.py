import os
import re

pattern = re.compile(r'<a\s+href="index\.html"\s+class="footer-logo"[^>]*>[\s\S]*?</a>', re.IGNORECASE)

replacement = '''<a href="index.html" class="footer-logo">
            <img src="assets/images/al_deewan_header_logo.png" alt="Al-Deewan Brand" />
            <div class="footer-logo__text">
              <span class="footer-logo__main">AL-DEEWAN</span>
              <span class="footer-logo__sub">BRAND</span>
            </div>
          </a>'''

for fname in os.listdir('.'):
    if not fname.endswith('.html'): continue
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'class="footer-logo"' in content:
        new_content = pattern.sub(replacement, content)
        if new_content != content:
            with open(fname, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print('Updated footer logo in:', fname)

print('All HTML pages footer logos updated!')
