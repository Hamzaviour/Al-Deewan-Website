/**
 * Al-Deewan Brand - Global Store & State Management
 * Handles Cart, Wishlist, Search, Currency Formatting, and LocalStorage
 */

const Store = {
  // Currency Formatter: Rs. 2,390.00
  formatMoney(amount) {
    const num = parseFloat(amount) || 0;
    return 'Rs.' + num.toLocaleString('en-PK', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  },

  // Cart Management
  getCart() {
    try {
      return JSON.parse(localStorage.getItem('bcp_cart')) || [];
    } catch (e) {
      return [];
    }
  },

  saveCart(cart) {
    localStorage.setItem('bcp_cart', JSON.stringify(cart));
    this.updateCartCount();
    window.dispatchEvent(new CustomEvent('cart:updated', { detail: { cart } }));
  },

  addToCart(product, qty = 1) {
    let cart = this.getCart();
    const existingIndex = cart.findIndex(item => item.id === product.id);
    
    if (existingIndex > -1) {
      cart[existingIndex].qty += qty;
    } else {
      cart.push({
        id: product.id,
        title: product.title,
        handle: product.handle,
        vendor: product.vendor,
        price: product.price,
        compare_at_price: product.compare_at_price,
        image: product.featured_image || (product.images && product.images[0]) || '',
        sku: product.sku,
        qty: qty
      });
    }
    
    this.saveCart(cart);
    this.showToast(`Added "${product.title}" to cart!`);
    
    // Open cart drawer
    if (window.MainUI && window.MainUI.openCartDrawer) {
      window.MainUI.openCartDrawer();
    }
  },

  updateCartQty(productId, newQty) {
    let cart = this.getCart();
    if (newQty <= 0) {
      cart = cart.filter(item => item.id !== productId);
    } else {
      const item = cart.find(item => item.id === productId);
      if (item) item.qty = newQty;
    }
    this.saveCart(cart);
  },

  removeFromCart(productId) {
    let cart = this.getCart().filter(item => item.id !== productId);
    this.saveCart(cart);
    this.showToast('Item removed from cart');
  },

  clearCart() {
    this.saveCart([]);
  },

  getCartSubtotal() {
    const cart = this.getCart();
    return cart.reduce((total, item) => total + (item.price * item.qty), 0);
  },

  getCartCount() {
    const cart = this.getCart();
    return cart.reduce((count, item) => count + item.qty, 0);
  },

  updateCartCount() {
    const count = this.getCartCount();
    document.querySelectorAll('.cart-count-badge, #cart-count').forEach(el => {
      el.textContent = count;
      el.style.display = count > 0 ? 'flex' : 'none';
    });
  },

  // Helper to calculate dynamic shipping fee
  getShippingFee(subtotal) {
    if (!subtotal || subtotal === 0) return 0;
    const settings = this.getSiteSettings();
    const delivery = settings.deliverySettings || { standardShippingFee: 250, freeShippingThreshold: 3500, enableFreeShipping: true };
    if (delivery.enableFreeShipping && subtotal >= (Number(delivery.freeShippingThreshold) || 3500)) {
      return 0;
    }
    return Number(delivery.standardShippingFee) || 250;
  },

  // Direct WhatsApp Checkout: Forwards all cart items, quantities, individual prices, total bill & order notes
  checkoutViaWhatsApp(orderNote = '') {
    const cart = this.getCart();
    if (!cart || cart.length === 0) {
      this.showToast('Your shopping bag is empty!');
      return;
    }

    const subtotal = this.getCartSubtotal();
    const shipping = this.getShippingFee(subtotal);
    const total = subtotal + shipping;
    const totalQty = this.getCartCount();

    let itemsList = cart.map((item, index) => {
      const productUrl = `${window.location.origin}/product.html?handle=${item.handle}`;
      const itemSubtotal = (item.price * item.qty).toLocaleString('en-PK');
      return `${index + 1}. *${item.title}*\n   • Qty: ${item.qty} × Rs. ${item.price.toLocaleString('en-PK')} = Rs. ${itemSubtotal}${item.sku ? `\n   • SKU: ${item.sku}` : ''}\n   • Link: ${productUrl}`;
    }).join('\n\n');

    let msg = `*Hello Al-Deewan Brand,*\n\n` +
      `I want to place an order via WhatsApp for *${totalQty} item(s)* in my cart:\n\n` +
      `━━━━━━━━━━━━━━━━━━━━\n` +
      `${itemsList}\n` +
      `━━━━━━━━━━━━━━━━━━━━\n` +
      `*Subtotal:* Rs. ${subtotal.toLocaleString('en-PK')}\n` +
      `*Shipping:* ${shipping === 0 ? 'FREE (Nationwide)' : `Rs. ${shipping.toLocaleString('en-PK')}`}\n` +
      `*TOTAL BILL:* Rs. ${total.toLocaleString('en-PK')}\n` +
      `*Payment:* Cash on Delivery (COD)\n` +
      (orderNote ? `*Special Note:* ${orderNote}\n` : '') +
      `━━━━━━━━━━━━━━━━━━━━\n\n` +
      `Please confirm my order and dispatch details. Thank you!`;

    const encodedMsg = encodeURIComponent(msg);
    const whatsappUrl = `https://api.whatsapp.com/send?phone=923334275944&text=${encodedMsg}`;
    window.open(whatsappUrl, '_blank');
  },

  // Wishlist Management
  getWishlist() {
    try {
      return JSON.parse(localStorage.getItem('bcp_wishlist')) || [];
    } catch (e) {
      return [];
    }
  },

  saveWishlist(wishlist) {
    localStorage.setItem('bcp_wishlist', JSON.stringify(wishlist));
    this.updateWishlistCount();
    window.dispatchEvent(new CustomEvent('wishlist:updated', { detail: { wishlist } }));
  },

  toggleWishlist(product) {
    let wishlist = this.getWishlist();
    const index = wishlist.findIndex(item => item.id === product.id);
    
    if (index > -1) {
      wishlist.splice(index, 1);
      this.showToast(`Removed from wishlist`);
    } else {
      wishlist.push({
        id: product.id,
        title: product.title,
        handle: product.handle,
        vendor: product.vendor,
        price: product.price,
        compare_at_price: product.compare_at_price,
        image: product.featured_image || (product.images && product.images[0]) || '',
        sku: product.sku
      });
      this.showToast(`Added to wishlist!`);
    }
    
    this.saveWishlist(wishlist);
    return index === -1; // returns true if added
  },

  isInWishlist(productId) {
    const wishlist = this.getWishlist();
    return wishlist.some(item => item.id === productId);
  },

  updateWishlistCount() {
    const count = this.getWishlist().length;
    document.querySelectorAll('.wishlist-count-badge, #wishlist-count').forEach(el => {
      el.textContent = count;
      el.style.display = count > 0 ? 'flex' : 'none';
    });
  },

  // Toast System
  showToast(message) {
    let toast = document.getElementById('bcp-toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'bcp-toast';
      toast.className = 'toast-notification';
      document.body.appendChild(toast);
    }
    
    toast.innerHTML = `
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#25d366" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>${message}</span>
    `;
    
    toast.classList.add('show');
    clearTimeout(this._toastTimeout);
    this._toastTimeout = setTimeout(() => {
      toast.classList.remove('show');
    }, 3200);
  },

  // Search Engine
  search(query, limit = 8) {
    if (!query || !window.CATALOG_PRODUCTS) return [];
    const q = query.toLowerCase().trim();
    return window.CATALOG_PRODUCTS.filter(p => {
      return (
        p.title.toLowerCase().includes(q) ||
        (p.vendor && p.vendor.toLowerCase().includes(q)) ||
        (p.category && p.category.toLowerCase().includes(q)) ||
        (p.sku && p.sku.toLowerCase().includes(q))
      );
    }).slice(0, limit);
  },

  // Dynamic Catalog & Settings Engine
  initCatalog() {
    try {
      const customCatalog = localStorage.getItem('aldeewan_custom_catalog');
      if (customCatalog) {
        window.CATALOG_PRODUCTS = JSON.parse(customCatalog);
      }
    } catch (e) {
      console.warn('Error reading custom catalog:', e);
    }
    return window.CATALOG_PRODUCTS || [];
  },

  getProducts() {
    this.initCatalog();
    return window.CATALOG_PRODUCTS || [];
  },

  saveProducts(products) {
    window.CATALOG_PRODUCTS = products;
    try {
      localStorage.setItem('aldeewan_custom_catalog', JSON.stringify(products));
    } catch (e) {
      console.error('Failed to save custom catalog to localStorage:', e);
    }
    window.dispatchEvent(new CustomEvent('catalog:updated', { detail: { products } }));
  },

  addProduct(productData) {
    const products = this.getProducts();
    const id = Date.now();
    const handle = (productData.title || 'product')
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '');

    const regularPrice = parseFloat(productData.price) || 0;
    const comparePrice = parseFloat(productData.compare_at_price) || regularPrice;
    const saveAmount = Math.max(0, comparePrice - regularPrice);
    const discountPercent = comparePrice > 0 ? Math.round((saveAmount / comparePrice) * 100) : 0;

    const newProduct = {
      id,
      title: productData.title || 'Untitled Article',
      handle: productData.handle || handle,
      vendor: productData.vendor || 'Al-Deewan Brand',
      category: productData.category || 'Unstitched',
      category_type: productData.category_type || '3PC',
      price: regularPrice,
      compare_at_price: comparePrice,
      save_amount: saveAmount,
      discount_percent: discountPercent,
      available: productData.available !== undefined ? productData.available : true,
      sku: productData.sku || `ALD-${id.toString().slice(-5)}`,
      barcode: productData.barcode || productData.sku || `ALD-${id.toString().slice(-5)}`,
      image: productData.image || 'assets/images/catalog/nishat-3pc-42206126-r-main.jpg',
      hover_image: productData.hover_image || productData.image || 'assets/images/catalog/nishat-3pc-42206126-r-main.jpg',
      images: productData.images && productData.images.length > 0 ? productData.images : [productData.image || 'assets/images/catalog/nishat-3pc-42206126-r-main.jpg'],
      featured_image: productData.image || 'assets/images/catalog/nishat-3pc-42206126-r-main.jpg',
      tags: productData.tags || [productData.category_type || '3PC', productData.category || 'Unstitched', productData.vendor || 'Al-Deewan Brand'],
      body_html: productData.body_html || `<p>${productData.title}</p>`,
      created_at: new Date().toISOString()
    };

    products.unshift(newProduct);
    this.saveProducts(products);
    return newProduct;
  },

  updateProduct(id, updatedData) {
    const products = this.getProducts();
    const index = products.findIndex(p => p.id === Number(id));
    if (index === -1) return false;

    const current = products[index];
    const regularPrice = updatedData.price !== undefined ? parseFloat(updatedData.price) : current.price;
    const comparePrice = updatedData.compare_at_price !== undefined ? parseFloat(updatedData.compare_at_price) : current.compare_at_price;
    const saveAmount = Math.max(0, comparePrice - regularPrice);
    const discountPercent = comparePrice > 0 ? Math.round((saveAmount / comparePrice) * 100) : 0;

    const updated = {
      ...current,
      ...updatedData,
      id: current.id, // preserve ID
      price: regularPrice,
      compare_at_price: comparePrice,
      save_amount: saveAmount,
      discount_percent: discountPercent,
      featured_image: updatedData.image || current.featured_image || current.image,
      image: updatedData.image || current.image
    };

    products[index] = updated;
    this.saveProducts(products);
    return updated;
  },

  deleteProduct(id) {
    let products = this.getProducts();
    const initialLength = products.length;
    products = products.filter(p => p.id !== Number(id));
    if (products.length !== initialLength) {
      this.saveProducts(products);
      return true;
    }
    return false;
  },

  // Site Settings Manager
  getDefaultSettings() {
    return {
      heroBanner: {
        image: 'assets/images/hero_banner.jpg',
        link: 'collections.html'
      },
      welcomeBanner: {
        image: 'assets/images/welcome_promo_banner.png',
        link: 'collections.html?category=Unstitched'
      },
      announcementText: '⚡ Biggest Lawn Opening in Pakistan • 100% Genuine Branded Cut Pieces • Cash on Delivery Nationwide ⚡',
      brandTickerText: 'SHOP YOUR FAVORITE BRANDS',
      brandTickerSubtitle: 'Explore 100% genuine cut pieces from top designer fashion houses',
      deliverySettings: {
        standardShippingFee: 250,
        freeShippingThreshold: 3500,
        enableFreeShipping: true
      },
      featuredSections: [
        {
          id: 'section_new_arrivals',
          title: 'SUMMER 2026 NEW ARRIVALS',
          subtitle: 'Freshly dropped unstitched lawn 3-piece and 2-piece suites',
          productIds: [],
          showTabs: true
        },
        {
          id: 'section_unstitched',
          title: 'UNSTITCHED 3PC PRINTED & EMBROIDERED LAWN',
          subtitle: 'Premium Swiss Voile & Digital Printed Lawn Dupatta Sets',
          productIds: [],
          showTabs: false
        }
      ],
      sectionHeadings: {
        newArrivalsTitle: 'SUMMER 2026 NEW ARRIVALS',
        newArrivalsSubtitle: 'Freshly dropped unstitched lawn 3-piece and 2-piece suites',
        unstitchedTitle: 'UNSTITCHED 3PC PRINTED & EMBROIDERED LAWN',
        unstitchedSubtitle: 'Premium Swiss Voile & Digital Printed Lawn Dupatta Sets'
      },
      navDropdowns: {
        shopByBrand: [
          { label: 'Khaadi', url: 'collections.html?brand=Khaadi' },
          { label: 'Sapphire', url: 'collections.html?brand=Sapphire' },
          { label: 'Nishat Linen', url: 'collections.html?brand=Nishat' },
          { label: 'Al Karam', url: 'collections.html?brand=Al+Karam' },
          { label: 'Asim Jofa', url: 'collections.html?brand=Asim+Jofa' },
          { label: 'Almirah', url: 'collections.html?brand=Almirah' },
          { label: 'Baroque', url: 'collections.html?brand=Baroque' },
          { label: 'Bareeze', url: 'collections.html?brand=Bareeze' },
          { label: 'Suhana', url: 'collections.html?brand=Suhana' },
          { label: 'Limelight', url: 'collections.html?brand=Limelight' },
          { label: 'Ethnic', url: 'collections.html?brand=Ethnic' },
          { label: 'Sana Safinaz', url: 'collections.html?brand=Sana+Safinaz' },
          { label: 'Maria B', url: 'collections.html?brand=Maria+B' }
        ],
        unstitched: [
          { label: 'All 3-Piece Suits (3PC)', url: 'collections.html?category=3PC' },
          { label: 'All 2-Piece Suits (2PC)', url: 'collections.html?category=2PC' },
          { label: '1-Piece Shirts (1PC)', url: 'collections.html?category=1PC' },
          { label: 'Saya Unstitched 3pc', url: 'collections.html?brand=Saya' },
          { label: 'Bareeze Printed 3pc', url: 'collections.html?brand=Bareeze' },
          { label: 'Jacquard Lawn 3pc', url: 'collections.html?brand=Jacquard' },
          { label: 'Almirah Luxury 3pc', url: 'collections.html?brand=Almirah' },
          { label: 'Sapphire Plaino 2pc', url: 'collections.html?brand=Sapphire' },
          { label: 'Khaadi Printed 2pc', url: 'collections.html?brand=Khaadi' },
          { label: 'Gents Summer Lawn', url: 'collections.html?category=Menswear' }
        ],
        readyToWear: [
          { label: 'Khaadi Stitched 2Pc', url: 'collections.html?brand=Khaadi&category=Ready+to+Wear' },
          { label: 'Sapphire Stitched 2Pc', url: 'collections.html?brand=Sapphire&category=Ready+to+Wear' },
          { label: 'Limelight Stitched 2Pc', url: 'collections.html?brand=Limelight&category=Ready+to+Wear' },
          { label: 'Zellbury Stitched 2Pc', url: 'collections.html?brand=Zellbury&category=Ready+to+Wear' },
          { label: 'All 1-Piece Kurtis', url: 'collections.html?category=1PC' },
          { label: 'All Ready To Wear Suits', url: 'collections.html?category=Ready+to+Wear' }
        ]
      },
      adminPassword: 'deewan2026'
    };
  },

  getSiteSettings() {
    try {
      const saved = localStorage.getItem('aldeewan_site_settings');
      if (saved) {
        return { ...this.getDefaultSettings(), ...JSON.parse(saved) };
      }
    } catch (e) {
      console.warn('Error loading settings:', e);
    }
    return this.getDefaultSettings();
  },

  saveSiteSettings(settings) {
    const updated = { ...this.getSiteSettings(), ...settings };
    try {
      localStorage.setItem('aldeewan_site_settings', JSON.stringify(updated));
    } catch (e) {
      console.error('Error saving settings:', e);
    }
    window.dispatchEvent(new CustomEvent('settings:updated', { detail: { settings: updated } }));
    this.applySiteSettings();
    return updated;
  },

  applySiteSettings() {
    const settings = this.getSiteSettings();

    // 1. Announcement bar
    const announcementItems = document.querySelectorAll('.announcement-bar__item, .announcement-bar .ticker-item, .announcement-ticker span');
    if (announcementItems.length > 0 && settings.announcementText) {
      announcementItems.forEach(item => {
        item.innerHTML = `<span class="announcement-bar__tag">Announcement</span> <span>${settings.announcementText}</span>`;
      });
    }

    // 2. Hero Banner
    const heroImg = document.querySelector('.hero-banner img, .hero-section img');
    if (heroImg && settings.heroBanner && settings.heroBanner.image) {
      heroImg.src = settings.heroBanner.image;
    }
    const heroLink = document.querySelector('.hero-banner a, .hero-section a');
    if (heroLink && settings.heroBanner && settings.heroBanner.link) {
      heroLink.href = settings.heroBanner.link;
    }

    // 3. Welcome Promotional Banner
    const promoImg = document.querySelector('.welcome-promo-banner img, #home-promo-banner img');
    if (promoImg && settings.welcomeBanner && settings.welcomeBanner.image) {
      promoImg.src = settings.welcomeBanner.image;
    }
    const promoLink = document.querySelector('.welcome-promo-banner a, #home-promo-banner a');
    if (promoLink && settings.welcomeBanner && settings.welcomeBanner.link) {
      promoLink.href = settings.welcomeBanner.link;
    }

    // 4. Section Headings & Featured Collections (Homepage)
    const featuredSecs = settings.featuredSections || [];
    if (featuredSecs.length > 0 || settings.sectionHeadings) {
      const sections = document.querySelectorAll('.products-section');
      const s1Title = featuredSecs[0]?.title || settings.sectionHeadings?.newArrivalsTitle;
      const s1Sub = featuredSecs[0]?.subtitle || settings.sectionHeadings?.newArrivalsSubtitle;
      const s2Title = featuredSecs[1]?.title || settings.sectionHeadings?.unstitchedTitle;
      const s2Sub = featuredSecs[1]?.subtitle || settings.sectionHeadings?.unstitchedSubtitle;

      if (sections.length > 0 && s1Title) {
        const sec1Title = sections[0].querySelector('.section-title');
        const sec1Sub = sections[0].querySelector('.section-subtitle');
        if (sec1Title) sec1Title.textContent = s1Title;
        if (sec1Sub && s1Sub) sec1Sub.textContent = s1Sub;
      }

      if (sections.length > 1 && s2Title) {
        const sec2Title = sections[1].querySelector('.section-title');
        const sec2Sub = sections[1].querySelector('.section-subtitle');
        if (sec2Title) sec2Title.textContent = s2Title;
        if (sec2Sub && s2Sub) sec2Sub.textContent = s2Sub;
      }
    }

    // 5. Navigation Dropdowns
    if (settings.navDropdowns) {
      // Shop by Brand dropdown
      const brandDropdown = document.querySelector('.nav-item-dropdown:nth-child(2) .nav-dropdown-menu');
      if (brandDropdown && settings.navDropdowns.shopByBrand && settings.navDropdowns.shopByBrand.length > 0) {
        brandDropdown.innerHTML = settings.navDropdowns.shopByBrand.map(b => `
          <a href="${b.url}" class="nav-dropdown-link">${b.label}</a>
        `).join('') + `<a href="shop-by-brand.html" class="nav-dropdown-link" style="grid-column:1/-1; border-top:1px solid #eee; margin-top:6px; color:var(--color-primary); font-weight:800;">View All 50+ Brands →</a>`;
      }
    }
  },

  exportCatalogJS() {
    const products = this.getProducts();
    return `window.CATALOG_PRODUCTS = ${JSON.stringify(products, null, 2)};\n`;
  },

  resetCatalog() {
    localStorage.removeItem('aldeewan_custom_catalog');
    localStorage.removeItem('aldeewan_site_settings');
    window.location.reload();
  },

  // Init
  init() {
    this.initCatalog();
    this.updateCartCount();
    this.updateWishlistCount();
    this.applySiteSettings();
  }
};

document.addEventListener('DOMContentLoaded', () => {
  Store.init();
});

window.Store = Store;
