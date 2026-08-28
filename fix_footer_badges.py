import os
import re

footer_badges_html = '''        <div class="payment-methods" style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
          <!-- Direct Bank Transfer Badge -->
          <span class="payment-badge" title="Direct Bank Transfer" style="display:inline-flex; align-items:center; background:#f4f6fa; border:1px solid #cce0eb; border-radius:6px; padding:5px 12px; gap:6px; font-size:11px; font-weight:800; color:#1a5276;">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#1a5276" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="2" y="5" width="20" height="14" rx="2"></rect>
              <line x1="2" y1="10" x2="22" y2="10"></line>
            </svg>
            <span>Bank Transfer</span>
          </span>

          <!-- WhatsApp Order & Support Badge -->
          <a href="https://api.whatsapp.com/send?phone=923334275944&text=Hello%20Al-Deewan%20Brand%2C%20I%20have%20an%20inquiry." target="_blank" class="payment-badge" title="WhatsApp Order & Support" style="display:inline-flex; align-items:center; background:#e8f9ee; border:1px solid #bdf1cc; border-radius:6px; padding:5px 12px; gap:6px; font-size:11px; font-weight:800; color:#128c7e; text-decoration:none;">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="#25D366">
              <path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981z"/>
            </svg>
            <span>WhatsApp Orders</span>
          </a>
        </div>'''

for fname in os.listdir('.'):
    if not fname.endswith('.html'): continue
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Clean up duplicate "Powered By Whizzly Lab"
    content = re.sub(
        r'©\s*2026\s*Al-Deewan\s*Brand\.?\s*All\s*Rights\s*Reserved\.?(\s*Powered\s*By\s*Whizzly\s*Lab)+',
        '© 2026 Al-Deewan Brand. All Rights Reserved. Powered By Whizzly Lab',
        content,
        flags=re.IGNORECASE
    )
    content = re.sub(
        r'Powered\s*By\s*Whizzly\s*Lab\s*Powered\s*By\s*Whizzly\s*Lab',
        'Powered By Whizzly Lab',
        content,
        flags=re.IGNORECASE
    )

    # 2. Replace payment methods section with just COD and WhatsApp badges
    content = re.sub(r'<div class="payment-methods"[\s\S]*?</div>', footer_badges_html.strip(), content)

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Fixed footer in:', fname)

print('All footers successfully updated!')
