import os

target_btn = '''<button class="btn-whatsapp" id="cart-drawer-whatsapp-btn" onclick="Store.checkoutViaWhatsApp()" style="width:100%; justify-content:center; padding:14px; font-weight:800; font-size:13px; margin-bottom:8px; display:flex; align-items:center; gap:8px;">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981z"/></svg>
        ORDER ON WHATSAPP (<span id="cart-drawer-btn-total">Rs.0.00</span>)
      </button>'''

for fname in os.listdir('.'):
    if not fname.endswith('.html'): continue
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '<a href="checkout.html" class="btn-primary" style="margin-bottom:8px;">PROCEED TO CHECKOUT</a>' in content:
        content = content.replace(
            '<a href="checkout.html" class="btn-primary" style="margin-bottom:8px;">PROCEED TO CHECKOUT</a>',
            target_btn
        )
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)
        print('Updated cart drawer in:', fname)

print('All HTML pages checked and updated!')
