import os

for fname in os.listdir('.'):
    if not fname.endswith('.html'): continue
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '<div class="slide-drawer left" id="mobile-nav-drawer">' in content:
        if 'href="index.html">HOME</a>' not in content and 'href="index.html">Home</a>' not in content:
            content = content.replace(
                '<li><a href="collections.html?collection=new-in"',
                '<li><a href="index.html" style="font-weight:700; font-size:15px; text-transform:uppercase;">HOME</a></li>\n        <li><a href="collections.html?collection=new-in"'
            )
            with open(fname, 'w', encoding='utf-8') as f:
                f.write(content)
            print('Added HOME to mobile nav in:', fname)

print('Done updating HTML files!')
