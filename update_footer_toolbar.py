import os
import re

payment_badges_svg = '''        <div class="payment-methods" style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
          <!-- Visa -->
          <span class="payment-badge" title="Visa" style="display:inline-flex; align-items:center;">
            <svg viewBox="0 0 38 24" width="38" height="24" fill="none"><rect width="38" height="24" rx="3" fill="#1434CB"/><path d="M15.4 16.5H13.2L14.6 7.5H16.8L15.4 16.5ZM21.2 7.7C20.7 7.5 20 7.3 19.1 7.3C16.9 7.3 15.3 8.5 15.3 10.2C15.3 11.5 16.4 12.2 17.2 12.6C18.1 13 18.4 13.3 18.4 13.7C18.4 14.3 17.7 14.6 17 14.6C16.1 14.6 15.6 14.5 14.8 14.1L14.5 14L14.2 16C14.8 16.3 15.8 16.5 16.9 16.5C19.3 16.5 20.8 15.3 20.8 13.5C20.8 12.5 20.1 11.7 18.7 11C18 10.6 17.6 10.4 17.6 10C17.6 9.6 18.1 9.2 19 9.2C19.8 9.2 20.4 9.4 20.8 9.6L21 9.7L21.2 7.7ZM25.8 13.5L26.7 8.8C26.7 8.8 26.6 8.8 26.3 8.8C25.6 8.8 24.9 9.1 24.6 9.8L22 16.5H24.3L24.8 15.1H27.5L27.8 16.5H30L28.1 7.5H26.2C25.7 7.5 25.3 7.8 25.1 8.2L21.5 16.5H23.9L24.4 15.1H27.2L27.4 16.5H29.7L27.8 7.5H25.9L24 16.5H26.3L25.8 13.5ZM12.2 7.5L9.9 13.7L9.6 12.3C9.1 10.6 7.6 8.7 5.9 7.8L7.8 16.5H10.2L13.8 7.5H12.2Z" fill="white"/></svg>
          </span>
          <!-- Mastercard -->
          <span class="payment-badge" title="Mastercard" style="display:inline-flex; align-items:center;">
            <svg viewBox="0 0 38 24" width="38" height="24" fill="none"><rect width="38" height="24" rx="3" fill="#252525"/><circle cx="15" cy="12" r="7" fill="#EB001B"/><circle cx="23" cy="12" r="7" fill="#F79E1B"/><path d="M19 6.8C20.6 8.1 21.6 10 21.6 12C21.6 14 20.6 15.9 19 17.2C17.4 15.9 16.4 14 16.4 12C16.4 10 17.4 8.1 19 6.8Z" fill="#FF5F00"/></svg>
          </span>
          <!-- Link -->
          <span class="payment-badge" title="Link" style="display:inline-flex; align-items:center;">
            <svg viewBox="0 0 38 24" width="38" height="24" fill="none"><rect width="38" height="24" rx="3" fill="#00D66F"/><path d="M12 12C12 9.2 14.2 7 17 7H19V9H17C15.3 9 14 10.3 14 12C14 13.7 15.3 15 17 15H19V17H17C14.2 17 12 14.8 12 12Z" fill="#0A2540"/><path d="M26 12C26 14.8 23.8 17 21 17H19V15H21C22.7 15 24 13.7 24 12C24 10.3 22.7 9 21 9H19V7H21C23.8 7 26 9.2 26 12Z" fill="#0A2540"/><rect x="16" y="11" width="6" height="2" fill="#0A2540"/></svg>
          </span>
          <!-- Google Pay -->
          <span class="payment-badge" title="Google Pay" style="display:inline-flex; align-items:center;">
            <svg viewBox="0 0 38 24" width="38" height="24" fill="none"><rect width="38" height="24" rx="3" fill="#FFFFFF" stroke="#D5D5D5"/><path d="M15.2 12.1C15.2 11.7 15.1 11.3 15.1 10.9H11.5V12.9H13.6C13.5 13.4 13.2 13.9 12.7 14.2V15.3H14.1C14.9 14.5 15.2 13.4 15.2 12.1Z" fill="#4285F4"/><path d="M11.5 15.8C12.6 15.8 13.4 15.5 14.1 14.8L12.7 13.7C12.3 14 11.9 14.1 11.5 14.1C10.5 14.1 9.6 13.4 9.3 12.5H7.9V13.6C8.6 15 10 15.8 11.5 15.8Z" fill="#34A853"/><path d="M9.3 12.5C9.2 12.2 9.2 11.8 9.2 11.5C9.2 11.2 9.2 10.8 9.3 10.5V9.4H7.9C7.6 10 7.4 10.7 7.4 11.5C7.4 12.3 7.6 13 7.9 13.6L9.3 12.5Z" fill="#FBBC04"/><path d="M11.5 8.9C12.1 8.9 12.6 9.1 13 9.5L14.2 8.3C13.4 7.6 12.5 7.2 11.5 7.2C10 7.2 8.6 8 7.9 9.4L9.3 10.5C9.6 9.6 10.5 8.9 11.5 8.9Z" fill="#EA4335"/><path d="M18.8 8.5H17.2V15.5H18.8V8.5Z" fill="#5F6368"/><path d="M22.8 10.5C21.8 10.5 21 11.3 21 12.3C21 13.3 21.8 14.1 22.8 14.1C23.8 14.1 24.6 13.3 24.6 12.3C24.6 11.3 23.8 10.5 22.8 10.5ZM22.8 12.8C22.2 12.8 21.8 12.3 21.8 11.7C21.8 11.1 22.2 10.6 22.8 10.6C23.4 10.6 23.8 11.1 23.8 11.7C23.8 12.3 23.4 12.8 22.8 12.8Z" fill="#5F6368"/><path d="M26.2 15.5V8.5H27.5V9.4C27.9 8.8 28.6 8.5 29.3 8.5C30.6 8.5 31.5 9.4 31.5 10.7V15.5H30.1V11C30.1 10.2 29.5 9.7 28.7 9.7C28 9.7 27.5 10.3 27.5 11.1V15.5H26.2Z" fill="#5F6368"/></svg>
          </span>
          <!-- Shop Pay -->
          <span class="payment-badge" title="Shop Pay" style="display:inline-flex; align-items:center;">
            <svg viewBox="0 0 38 24" width="38" height="24" fill="none"><rect width="38" height="24" rx="3" fill="#5A31F4"/><path d="M13.2 15.5C11.5 15.5 10.5 14.4 10.5 13.1C10.5 11.1 12.4 10.7 13.8 10.4C14.8 10.2 15.2 9.9 15.2 9.4C15.2 8.8 14.6 8.4 13.8 8.4C12.8 8.4 12.1 8.8 11.9 9.5H10.6C10.9 8.2 12.1 7.3 13.8 7.3C15.4 7.3 16.6 8.2 16.6 9.6V15.3H15.3V14.4C14.7 15.1 14 15.5 13.2 15.5ZM13.6 14.4C14.5 14.4 15.3 13.7 15.3 12.7V11.3C14.5 11.5 11.9 11.8 11.9 13.1C11.9 13.9 12.6 14.4 13.6 14.4Z" fill="white"/><path d="M19.8 15.3H18.4V7.5H19.8V15.3Z" fill="white"/><path d="M24.7 15.5C23 15.5 21.8 14.2 21.8 12.4C21.8 10.6 23 9.3 24.7 9.3C26.4 9.3 27.6 10.6 27.6 12.4C27.6 14.2 26.4 15.5 24.7 15.5ZM24.7 14.3C25.6 14.3 26.2 13.5 26.2 12.4C26.2 11.3 25.6 10.5 24.7 10.5C23.8 10.5 23.2 11.3 23.2 12.4C23.2 13.5 23.8 14.3 24.7 14.3Z" fill="white"/></svg>
          </span>
          <!-- Direct Bank Transfer Badge -->
          <span class="payment-badge" title="Direct Bank Transfer" style="display:inline-flex; align-items:center; background:#f4f6fa; border:1px solid #cce0eb; border-radius:6px; padding:5px 12px; gap:6px; font-size:11px; font-weight:800; color:#1a5276;">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#1a5276" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="2" y="5" width="20" height="14" rx="2"></rect>
              <line x1="2" y1="10" x2="22" y2="10"></line>
            </svg>
            <span>Bank Transfer</span>
          </span>
        </div>'''

mobile_toolbar_html = '''  <!-- Mobile Bottom Toolbar -->
  <div class="mobile-toolbar">
    <a href="collections.html" class="toolbar-item">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
      <span>Shop</span>
    </a>
    <button class="toolbar-item search-trigger">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
      <span>Search</span>
    </button>
    <button class="toolbar-item" onclick="MainUI.openWishlistDrawer()">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg>
      <span>Wishlist</span>
    </button>
    <button class="toolbar-item" onclick="MainUI.openCartDrawer()">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path><line x1="3" y1="6" x2="21" y2="6"></line><path d="M16 10a4 4 0 0 1-8 0"></path></svg>
      <span>Cart</span>
    </button>
    <a href="order-tracking.html" class="toolbar-item">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
      <span>Track</span>
    </a>
  </div>'''

for fname in os.listdir('.'):
    if not fname.endswith('.html'): continue
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update copyright line: Powered By Whizzly Lab
    content = re.sub(r'©\s*2026\s*Al-Deewan\s*Brand\.?\s*All Rights Reserved\.?\s*Powered By [^<\n]*', '© 2026 Al-Deewan Brand. All Rights Reserved. Powered By Whizzly Lab', content)
    content = re.sub(r'Powered By Jacq360', 'Powered By Whizzly Lab', content)
    content = re.sub(r'© 2026 Al-Deewan Brand\. All Rights Reserved\.', '© 2026 Al-Deewan Brand. All Rights Reserved. Powered By Whizzly Lab', content)

    # 2. Remove Download Mobile App from information link lists
    content = re.sub(r'<li><a href="download-app\.html">Download Mobile App</a></li>\s*', '', content)
    content = re.sub(r'<li><a href="download-app\.html">Download App</a></li>\s*', '', content)

    # 3. Replace payment methods with SVG icons
    content = re.sub(r'<div class="payment-methods"[\s\S]*?</div>', payment_badges_svg.strip(), content)

    # 4. Ensure mobile toolbar is present before </body> or before overlays
    if 'class="mobile-toolbar"' not in content and '</body>' in content:
        content = content.replace('</body>', mobile_toolbar_html + '\n</body>')

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Updated:', fname)

print('All HTML pages updated successfully!')
