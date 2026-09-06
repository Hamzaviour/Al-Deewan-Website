import os
import re

html_files = [
    "index.html",
    "collections.html",
    "product.html",
    "shop-by-brand.html",
    "order-tracking.html",
    "contact.html",
    "customer-services.html",
    "refunds.html",
    "privacy-policy.html",
    "download-app.html"
]

for filename in html_files:
    if not os.path.exists(filename):
        continue
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update cart-drawer-shipping text from "Rs. 250" or similar to "According to parcel weight"
    content = re.sub(
        r'<span[^>]*id="cart-drawer-shipping"[^>]*>.*?</span>',
        '<span style="font-size:12.5px; font-weight:700; color:#5e3585;" id="cart-drawer-shipping">According to parcel weight</span>',
        content
    )

    # 2. Add or ensure weight banner in drawer footer if not present
    if 'Delivery Charges will be according to the weight of the parcel' not in content:
        notice_html = '''<div style="background:#f5effc; border:1px solid #dcd3ea; border-radius:8px; padding:10px 12px; font-size:12px; font-weight:700; color:#5e3585; margin-bottom:12px; display:flex; align-items:center; gap:8px;">
        <span>⚖️</span>
        <span>Delivery Charges will be according to the weight of the parcel.</span>
      </div>\n      '''
        content = content.replace(
            '<div class="drawer-footer" id="cart-drawer-footer">\n',
            '<div class="drawer-footer" id="cart-drawer-footer">\n      ' + notice_html
        )
        content = content.replace(
            '<div class="drawer-footer" id="cart-drawer-footer">',
            '<div class="drawer-footer" id="cart-drawer-footer">\n      ' + notice_html
        )

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated cart drawer in {filename}")

print("All cart drawers updated successfully!")
