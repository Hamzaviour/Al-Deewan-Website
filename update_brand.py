import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]
print('Found HTML files to update:', html_files)

for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Update Favicon
    content = re.sub(r'href="assets/images/round_logo[^"]*"', 'href="assets/images/favicon.png"', content)
    
    # 2. Update Header Logo
    content = re.sub(
        r'<a href="index\.html" class="header-logo">[\s\S]*?</a>',
        '''<a href="index.html" class="header-logo">
          <img src="assets/images/al_deewan_header_logo.png" alt="Al-Deewan Brand Logo" />
          <div class="header-logo__text">
            <span class="brand-main">AL-DEEWAN</span>
            <span class="brand-sub">BRAND</span>
          </div>
        </a>''',
        content
    )
    
    # 3. Update Footer Logo
    content = re.sub(
        r'<a href="index\.html" class="footer-logo">[\s\S]*?</a>',
        '''<a href="index.html" class="footer-logo" style="display:inline-flex; align-items:center; gap:10px; margin-bottom:16px;">
            <img src="assets/images/al_deewan_header_logo.png" alt="Al-Deewan Brand" style="height:50px;" />
            <div style="font-size:18px; font-weight:900; color:#000; letter-spacing:0.04em;">AL-DEEWAN <span style="font-size:11px; display:block; color:#444; letter-spacing:0.18em;">BRAND</span></div>
          </a>''',
        content
    )

    # 4. Update Address
    content = re.sub(r'9A Asif Block[^<\n]*Lahore[^<\n]*', '86-Dogar Plaza, Gulshan Block Iqbal Town Near Makki Masjid, Lahore', content)
    
    # 5. Update Phone numbers in HTML
    content = re.sub(r'0309\s*/\s*0326-1794000', '0333-4275944 / 0344-6463719', content)
    content = re.sub(r'0309-1794000\s*&\s*0326-1794000', '0333-4275944 & 0344-6463719', content)
    content = re.sub(r'0309-1794000', '0333-4275944', content)
    content = re.sub(r'03091794000', '03334275944', content)
    content = re.sub(r'923091794000', '923334275944', content)
    content = re.sub(r'\+92\s*309\s*1794000', '+92 333 4275944', content)
    
    # 6. Update Brand mentions in titles/footers
    content = content.replace('Branded Cut Pieces', 'Al-Deewan Brand')
    content = content.replace('BRANDED CUT PIECES', 'AL-DEEWAN BRAND')
    content = content.replace('care@brandedcutpieces.com.pk', 'care@aldeewanbrand.com')
    content = content.replace('brandedcutpieces.info@gmail.com', 'aldeewanbrand@gmail.com')
    
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)

print('All HTML files updated successfully!')
