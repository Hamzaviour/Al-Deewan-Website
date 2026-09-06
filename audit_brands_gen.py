import os

files = sorted([f for f in os.listdir('assets/images/brands') if f.endswith(('.png', '.jpg'))])

html = """<!DOCTYPE html>
<html>
<head>
<title>Brand Images Visual Audit</title>
<style>
body { font-family: sans-serif; background: #f5f5f5; padding: 20px; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 16px; }
.card { background: #fff; border: 1px solid #ccc; border-radius: 8px; padding: 10px; text-align: center; }
.card img { width: 160px; height: 160px; object-fit: contain; border: 1px solid #eee; }
.fname { font-size: 13px; font-weight: bold; margin-top: 8px; word-break: break-all; }
</style>
</head>
<body>
<h1>Brand Images Visual Audit (All Files)</h1>
<div class="grid">
"""

for f in files:
    html += f"""
<div class="card">
  <img src="assets/images/brands/{f}" alt="{f}" />
  <div class="fname">{f}</div>
</div>
"""

html += """
</div>
</body>
</html>
"""

with open('audit_brands.html', 'w', encoding='utf-8') as out:
    out.write(html)

print('Generated audit_brands.html with', len(files), 'images')
