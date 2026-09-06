import re

html_files = [
    'index.html',
    'collections.html',
    'product.html',
    'shop-by-brand.html',
    'contact.html',
    'order-tracking.html',
    'customer-services.html',
    'download-app.html',
    'privacy-policy.html',
    'refunds.html',
    'cart.html',
    'checkout.html',
    'thank-you.html'
]

payment_group_html = '''        <div class="payment-methods">
          <img src="assets/images/payments/visa.png" alt="Visa" class="payment-icon" />
          <img src="assets/images/payments/mastercard.png" alt="Mastercard" class="payment-icon" />
          <img src="assets/images/payments/tabby.png" alt="Tabby" class="payment-icon" />
          <img src="assets/images/payments/gpay.png" alt="Google Pay" class="payment-icon" />
          <img src="assets/images/payments/shoppay.png" alt="Shop Pay" class="payment-icon" />
        </div>'''

for fpath in html_files:
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace single payment-methods div with payment_group_html
        new_content = re.sub(
            r'<div class="payment-methods">.*?</div>',
            payment_group_html,
            content,
            flags=re.DOTALL
        )

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Updated payment icons in {fpath}')
    except Exception as e:
        print(f'Error updating {fpath}: {e}')

print('All pages updated with individual payment icons!')
