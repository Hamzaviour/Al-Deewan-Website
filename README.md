# 🛍️ Al-Deewan Brand - E-Commerce Website

An exact, modern, high-performance Pakistani fashion & lawn e-commerce website built for **Al-Deewan Brand**, featuring full product browsing, faceted filters, real-time slide-out cart and wishlist drawers, predictive search, order tracking, instant WhatsApp order generator, and cash on delivery (COD) checkout.

---

## 🌟 Key Features

- 👗 **Rich Product Catalog**: Complete collection of 1,920+ 100% original unstitched and ready-to-wear suites from top Pakistani designer brands (Khaadi, Sapphire, Nishat Linen, Almirah, Baroque, Asim Jofa, Bareeze, Ethnic, and more).
- 🏷️ **Faceted Filtering & Sorting**: Filter by brand, availability (In Stock / Out of Stock), category (3PC, 2PC, Unstitched, Ready to Wear, Menswear), price range slider, and multi-criteria sorting.
- 🛍️ **Interactive Slide-Out Cart Drawer**: Live subtotal calculator with free delivery progress bar (Rs. 3,500 threshold nationwide).
- 💖 **Wishlist System**: 1-click wishlist toggle with persistent badge counter.
- 🔍 **Predictive Live Search**: Instant auto-suggest search modal indexing the entire catalog.
- 📱 **Mobile-First Bottom Navigation Bar**: Floating bottom navigation bar across all pages for mobile shoppers.
- 💬 **WhatsApp Direct Ordering (CTA)**:
  - 1-tap WhatsApp Order button on every product page automatically pre-filling product title, SKU, price, and link.
  - Floating WhatsApp chat widget on every page linked to **`0333-4275944`**.
- 🚚 **Shipment Tracking Portal**: Order ID & Tracking Number tracking interface with visual milestone progress timeline.
- 💳 **Complete Pakistani E-Commerce Checkout**:
  - Cash on Delivery (COD) & Direct Bank Transfer options.
  - Pakistani city delivery address selector.
  - Voucher discount engine (`SUMMER10`).
  - Order confirmation receipt with order ID generator.

---

## 📁 Project Structure

```text
├── index.html                  # Main Homepage (Hero Banner, Brand Ticker, Featured Grids)
├── collections.html            # Catalog Browser with Faceted Filters & Sorting
├── product.html                # Product Details Page (Gallery, WhatsApp Order, Stock Status)
├── cart.html                   # Dedicated Shopping Bag Page
├── checkout.html               # Multi-step Checkout Page with COD & City Selector
├── order-tracking.html         # Shipment Tracking Simulator with Progress Timeline
├── thank-you.html              # Order Confirmation Receipt Page
├── shop-by-brand.html          # Directory of 50+ Pakistani Brands
├── contact.html                # Contact Us Page with Address & Hotline Form
├── refunds.html                # Official Refund & Exchange Policy
├── privacy-policy.html         # Privacy Policy Page
├── customer-services.html      # Customer Support Terms & FAQs
├── assets/
│   ├── css/
│   │   └── style.css           # Master Theme Stylesheet (Typography, Layout, Colors, Animations)
│   ├── js/
│   │   ├── catalog-data.js     # Structured Catalog Database (1,920+ Products & 85 Collections)
│   │   ├── store.js            # Global State Manager (Cart, Wishlist, Currency, Toasts)
│   │   └── main.js             # Master UI Controllers (Drawers, Modals, Brand Ticker, Sliders)
│   └── images/                 # Optimized High-Res Brand Logos, Banners & Icons
├── .gitignore                  # Git Ignore Configuration
└── README.md                   # Project Documentation
```

---

## 🚀 Getting Started Locally

### Prerequisites
You only need any local static HTTP server (Python, Node, or VS Code Live Server).

### Method 1: Using Python
```bash
# In the project directory:
python -m http.server 8080
```
Open your browser and navigate to:
👉 **`http://localhost:8080`**

### Method 2: Using Node (`npx serve`)
```bash
npx serve -l 8080 .
```

---

## 🏢 Store Information

- **Brand Name**: Al-Deewan Brand
- **Physical Address**: 86-Dogar Plaza, Gulshan Block Iqbal Town Near Makki Masjid, Lahore, Pakistan
- **Telephone Hotlines**: `0333-4275944` / `0344-6463719`
- **WhatsApp Support**: `+92 333 4275944`
- **Support Email**: `care@aldeewanbrand.com`

---

## 📌 How to Push to GitHub

```bash
# 1. Initialize git
git init

# 2. Add all files
git add .

# 3. Commit your changes
git commit -m "Initial commit of Al-Deewan Brand e-commerce website"

# 4. Link your remote GitHub repository
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git

# 5. Rename branch to main and push
git branch -M main
git push -u origin main
```

---

## ⚡ 1-Click Deployment to Vercel

The project is fully pre-configured for Vercel with [`vercel.json`](file:///e:/Work/Al-Deewan%20Website/vercel.json).

1. Log into your [Vercel Dashboard](https://vercel.com).
2. Click **"Add New..."** → **"Project"**.
3. Import your GitHub repository.
4. Leave all build settings as default (Framework Preset: *Other / Static*) and click **"Deploy"**.
5. Your store will be live with a global CDN URL and free SSL certificate!

---

## 📄 License & Credits

© 2026 **Al-Deewan Brand**. All Rights Reserved.  
*Powered By Whizzly Lab*
