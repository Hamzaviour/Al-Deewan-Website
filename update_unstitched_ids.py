import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html') and f != 'admin.html']

for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find <div class="nav-item-dropdown">\s*<a href="collections.html?category=Unstitched"
    # and replace with <div class="nav-item-dropdown" id="nav-dropdown-unstitched">\s*<a href="collections.html?category=Unstitched"
    new_content = re.sub(
        r'<div class="nav-item-dropdown">(\s*<a[^>]*href="collections\.html\?category=Unstitched")',
        r'<div class="nav-item-dropdown" id="nav-dropdown-unstitched">\1',
        content
    )

    if new_content != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {fpath}")
    else:
        print(f"No match or already updated in {fpath}")
