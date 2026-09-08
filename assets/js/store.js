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

  // Direct WhatsApp Checkout: Forwards all cart items, quantities, individual prices, total bill & order notes
  checkoutViaWhatsApp(orderNote = '') {
    const cart = this.getCart();
    if (!cart || cart.length === 0) {
      this.showToast('Your shopping bag is empty!');
      return;
    }

    const subtotal = this.getCartSubtotal();
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
      `*Delivery Charges:* According to the weight of the parcel\n` +
      `*TOTAL AMOUNT:* Rs. ${subtotal.toLocaleString('en-PK')} (+ Delivery as per parcel weight)\n` +
      `*Payment:* Direct Bank Transfer / Online Payment\n` +
      (orderNote ? `*Special Note:* ${orderNote}\n` : '') +
      `━━━━━━━━━━━━━━━━━━━━\n\n` +
      `Please confirm my order and share parcel weight & delivery fee. Thank you!`;

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

  // Compare Management
  getCompare() {
    try {
      return JSON.parse(localStorage.getItem('bcp_compare')) || [];
    } catch (e) {
      return [];
    }
  },

  saveCompare(compare) {
    localStorage.setItem('bcp_compare', JSON.stringify(compare));
    window.dispatchEvent(new CustomEvent('compare:updated', { detail: { compare } }));
  },

  toggleCompare(product) {
    let compare = this.getCompare();
    const index = compare.findIndex(item => item.id === product.id);
    
    if (index > -1) {
      compare.splice(index, 1);
      this.showToast(`Removed from compare list`);
      this.saveCompare(compare);
      return false;
    } else {
      if (compare.length >= 4) {
        this.showToast(`You can compare up to 4 products at a time.`);
        return false;
      }
      compare.push({
        id: product.id,
        title: product.title,
        handle: product.handle,
        vendor: product.vendor || 'Al-Deewan Brand',
        price: product.price,
        compare_at_price: product.compare_at_price,
        save_amount: product.save_amount || (product.compare_at_price > product.price ? product.compare_at_price - product.price : 0),
        discount_percent: product.discount_percent || 0,
        image: product.featured_image || product.image || (product.images && product.images[0]) || '',
        sku: product.sku || '',
        category: product.category || 'Unstitched',
        category_type: product.category_type || '3PC',
        fabric: product.fabric || 'Lawn',
        available: product.available !== undefined ? product.available : true
      });
      if (compare.length >= 2) {
        this.showToast(`Added to compare! (${compare.length}/4 items ready)`);
      } else {
        this.showToast(`Added to compare list! (1/4)`);
      }
      this.saveCompare(compare);
      return true;
    }
  },

  removeFromCompare(productId) {
    let compare = this.getCompare();
    const filtered = compare.filter(item => item.id !== productId);
    this.saveCompare(filtered);
    this.showToast(`Item removed from compare`);
  },

  clearCompare() {
    this.saveCompare([]);
    this.showToast(`Cleared compare list`);
  },

  isInCompare(productId) {
    const compare = this.getCompare();
    return compare.some(item => item.id === productId);
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

  saveProducts(products, adminPasscode) {
    window.CATALOG_PRODUCTS = products;
    try {
      localStorage.setItem('aldeewan_custom_catalog', JSON.stringify(products));
    } catch (e) {
      console.error('Failed to save custom catalog to localStorage:', e);
    }
    window.dispatchEvent(new CustomEvent('catalog:updated', { detail: { products } }));

    // Sync to server API so all devices and visitors receive new/updated articles
    const passcode = adminPasscode || localStorage.getItem('aldeewan_admin_pass') || 'deewan2026';
    return fetch('api/products.php', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Admin-Passcode': passcode
      },
      body: JSON.stringify({ products, adminPasscode: passcode })
    })
    .then(res => res.json())
    .then(data => {
      if (data && data.success) {
        console.log('✅ Products synced to server for all devices:', data.count);
      } else {
        console.warn('⚠️ Server response on product sync:', data);
      }
      return data;
    })
    .catch(e => {
      console.warn('Product server sync note:', e);
      return null;
    });
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

    const newImages = (productData.images && Array.isArray(productData.images) && productData.images.length > 0)
      ? productData.images
      : [productData.image || 'assets/images/catalog/nishat-3pc-42206126-r-main.jpg'];
    const mainImg = productData.featured_image || productData.image || newImages[0];
    const hoverImg = productData.hover_image || newImages[1] || mainImg;
    const seasonVal = productData.season || 'Summer';
    const genderVal = productData.gender || (productData.category === 'Menswear' ? 'Men' : (productData.category === 'Kids' ? 'Kids' : 'Women'));
    const fabricVal = productData.fabric || '';

    const newProduct = {
      id,
      title: productData.title || 'Untitled Article',
      handle: productData.handle || handle,
      vendor: productData.vendor || 'Al-Deewan Brand',
      category: productData.category || 'Unstitched',
      category_type: productData.category_type || '3PC',
      season: seasonVal,
      gender: genderVal,
      fabric: fabricVal,
      price: regularPrice,
      compare_at_price: comparePrice,
      save_amount: saveAmount,
      discount_percent: discountPercent,
      available: productData.available !== undefined ? productData.available : true,
      sku: productData.sku || `ALD-${id.toString().slice(-5)}`,
      barcode: productData.barcode || productData.sku || `ALD-${id.toString().slice(-5)}`,
      image: mainImg,
      hover_image: hoverImg,
      images: newImages,
      featured_image: mainImg,
      tags: productData.tags || [
        productData.category_type || '3PC',
        productData.category || 'Unstitched',
        productData.vendor || 'Al-Deewan Brand',
        seasonVal,
        genderVal,
        fabricVal
      ].filter(Boolean),
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

    let updatedImages = current.images || [current.image || 'assets/images/catalog/nishat-3pc-42206126-r-main.jpg'];
    if (updatedData.images && Array.isArray(updatedData.images) && updatedData.images.length > 0) {
      updatedImages = updatedData.images;
    } else if (updatedData.image && (!updatedImages || updatedImages.length === 0)) {
      updatedImages = [updatedData.image];
    }

    const updatedMainImg = updatedData.featured_image || updatedData.image || updatedImages[0] || current.image;
    const updatedHoverImg = updatedData.hover_image || updatedImages[1] || updatedMainImg;

    const seasonVal = updatedData.season !== undefined ? updatedData.season : (current.season || 'Summer');
    const genderVal = updatedData.gender !== undefined ? updatedData.gender : (current.gender || (current.category === 'Menswear' ? 'Men' : (current.category === 'Kids' ? 'Kids' : 'Women')));
    const fabricVal = updatedData.fabric !== undefined ? updatedData.fabric : (current.fabric || '');

    const updated = {
      ...current,
      ...updatedData,
      id: current.id, // preserve ID
      season: seasonVal,
      gender: genderVal,
      fabric: fabricVal,
      price: regularPrice,
      compare_at_price: comparePrice,
      save_amount: saveAmount,
      discount_percent: discountPercent,
      images: updatedImages,
      featured_image: updatedMainImg,
      hover_image: updatedHoverImg,
      image: updatedMainImg
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
      heroSlides: [
        {
          id: 1,
          image: 'assets/images/banners/hero_slide_luxury.png',
          title: 'Luxury Lawn Collection 2026',
          link: 'https://api.whatsapp.com/send?phone=923334275944&text=Hello%20Al-Deewan%20Brand%2C%20I%20would%20like%20to%20order%20from%20the%20Luxury%20Lawn%20Collection.'
        },
        {
          id: 2,
          image: 'assets/images/banners/hero_slide_winter.png',
          title: 'Winter Khaddar & Karandi Shawl Collection',
          link: 'collections.html?season=Winter'
        },
        {
          id: 3,
          image: 'assets/images/banners/hero_slide_summer.png',
          title: 'Summer Lawn 2026 Launch',
          link: 'collections.html?season=Summer'
        }
      ],
      heroAutoplaySpeed: 5000,
      heroBanner: {
        image: 'assets/images/banners/hero_slide_luxury.png',
        link: 'https://api.whatsapp.com/send?phone=923334275944&text=Hello%20Al-Deewan%20Brand%2C%20I%20would%20like%20to%20order%20from%20the%20Branded%20Collection.'
      },
      welcomeBanner: {
        image: 'assets/images/web_banner_promo.png',
        link: 'https://api.whatsapp.com/send?phone=923334275944&text=Hello%20Al-Deewan%20Brand%2C%20I%20would%20like%20to%20order%20from%20the%20Branded%20Collection.'
      },
      announcementText: '⚡ 100% Genuine Branded Pieces • 50+ Top Designer Brands Launch • Biggest Lawn Opening in Pakistan ⚡',
      brandTickerText: 'SHOP YOUR FAVORITE BRANDS',
      brandTickerSubtitle: 'Explore 100% genuine cut pieces from top designer fashion houses',
      deliverySettings: {
        standardShippingFee: 250,
        freeShippingThreshold: 3500,
        enableFreeShipping: true
      },
      featuredSections: [
        {
          id: 'section_binsaeed',
          title: 'BIN SAEED STITCHED 2PC',
          subtitle: 'Pure Lawn & Cotton Stitched 2-Piece Suits with Matching Trousers / Dupattas',
          viewAllUrl: 'collections.html?brand=Bin+Saeed&type=2PC',
          targetGridId: 'binsaeed-products-grid',
          productIds: [],
          visible: true
        },
        {
          id: 'section_unstitched',
          title: 'UNSTITCHED 3PC PRINTED & EMBROIDERED LAWN',
          subtitle: 'Premium Swiss Voile & Digital Printed Lawn Dupatta Sets',
          viewAllUrl: 'collections.html?category=Unstitched&type=3PC',
          targetGridId: 'unstitched-products-grid',
          productIds: [],
          visible: true
        },
        {
          id: 'section_rtw',
          title: 'READY TO WEAR STITCHED COLLECTION',
          subtitle: 'Designer Stitched Kurties, 2-Piece & 3-Piece Pret Ensembles',
          viewAllUrl: 'collections.html?category=Ready+to+Wear',
          targetGridId: 'rtw-products-grid',
          productIds: [],
          visible: false // Hidden by default as requested
        },
        {
          id: 'section_designer',
          title: 'TOP DESIGNER LAWN SUITS',
          subtitle: 'Exclusive Cut Pieces from Pakistan Top 50+ Fashion Houses',
          viewAllUrl: 'collections.html',
          targetGridId: 'featured-brands-products-grid',
          productIds: [],
          visible: true
        }
      ],
      sectionHeadings: {
        binSaeedTitle: 'BIN SAEED STITCHED 2PC',
        unstitchedTitle: 'UNSTITCHED 3PC PRINTED & EMBROIDERED LAWN',
        rtwTitle: 'READY TO WEAR STITCHED COLLECTION',
        designerTitle: 'TOP DESIGNER LAWN SUITS'
      },
      navDropdowns: {
        unstitched: {
          visible: true,
          label: 'UNSTITCHED',
          url: 'collections.html?category=Unstitched',
          columns: [
            {
              id: '1pc',
              label: '1PC',
              url: 'collections.html?category=Unstitched&type=1PC',
              visible: true,
              isCustom: false,
              sublinks: [
                { label: 'Winter', url: 'collections.html?category=Unstitched&type=1PC&season=Winter' },
                { label: 'Summer', url: 'collections.html?category=Unstitched&type=1PC&season=Summer' },
                { label: 'Bedsheets', url: 'collections.html?type=Bedsheet' }
              ]
            },
            {
              id: '2pc',
              label: '2PC',
              url: 'collections.html?category=Unstitched&type=2PC',
              visible: true,
              isCustom: false,
              sublinks: [
                { label: 'Winter', url: 'collections.html?category=Unstitched&type=2PC&season=Winter' },
                { label: 'Summer', url: 'collections.html?category=Unstitched&type=2PC&season=Summer' }
              ]
            },
            {
              id: '3pc',
              label: '3PC',
              url: 'collections.html?category=Unstitched&type=3PC',
              visible: true,
              isCustom: false,
              sublinks: [
                { label: 'Winter', url: 'collections.html?category=Unstitched&type=3PC&season=Winter' },
                { label: 'Summer', url: 'collections.html?category=Unstitched&type=3PC&season=Summer' }
              ]
            },
            {
              id: '4pc',
              label: '4PC',
              url: 'collections.html?category=Unstitched&type=4PC',
              visible: false,
              isCustom: false,
              sublinks: [
                { label: 'Winter', url: 'collections.html?category=Unstitched&type=4PC&season=Winter' },
                { label: 'Summer', url: 'collections.html?category=Unstitched&type=4PC&season=Summer' }
              ]
            },
            {
              id: '5pc',
              label: '5PC',
              url: 'collections.html?category=Unstitched&type=5PC',
              visible: false,
              isCustom: false,
              sublinks: [
                { label: 'Winter', url: 'collections.html?category=Unstitched&type=5PC&season=Winter' },
                { label: 'Summer', url: 'collections.html?category=Unstitched&type=5PC&season=Summer' }
              ]
            }
          ]
        },
        readyToWear: {
          visible: true,
          label: 'READY TO WEAR',
          url: 'collections.html?category=Ready+to+Wear',
          links: [
            { label: '1PC (Kurtis)', url: 'collections.html?category=Ready+to+Wear&type=1PC', visible: true },
            { label: '2PC', url: 'collections.html?category=Ready+to+Wear&type=2PC', visible: true },
            { label: '3PC', url: 'collections.html?category=Ready+to+Wear&type=3PC', visible: true },
            { label: 'All Ready to Wear', url: 'collections.html?category=Ready+to+Wear', visible: true }
          ]
        },
        kids: {
          visible: true,
          label: 'KIDS',
          url: 'collections.html?category=Kids',
          links: [
            { label: 'Girls Eastern', url: 'collections.html?category=Kids&type=Girls+Eastern', visible: true },
            { label: 'Boys Kurta', url: 'collections.html?category=Kids&type=Boys+Kurta', visible: true },
            { label: 'All Kids Collection', url: 'collections.html?category=Kids', visible: true }
          ]
        },
        mainNavLinks: [
          { label: 'NEW ARRIVAL', url: 'collections.html?collection=new-in', badge: 'HOT', visible: true },
          { label: 'SHOP BY BRAND', url: 'shop-by-brand.html', badge: '', visible: true },
          { label: 'ORDER TRACKING', url: 'order-tracking.html', badge: '', visible: true }
        ]
      },
      adminPassword: 'deewan2026'
    };
  },

  getSiteSettings() {
    const defaults = this.getDefaultSettings();
    try {
      const saved = localStorage.getItem('aldeewan_site_settings');
      if (saved) {
        const parsed = JSON.parse(saved);
        
        // Ensure heroSlides exists with 3 default slides if not present
        if (!parsed.heroSlides || !Array.isArray(parsed.heroSlides) || parsed.heroSlides.length === 0) {
          parsed.heroSlides = defaults.heroSlides;
        }

        // Preserve saved featuredSections (allow any count including deletions)
        let mergedSections = parsed.featuredSections;
        if (!mergedSections || !Array.isArray(mergedSections) || (mergedSections[0] && mergedSections[0].id === 'section_new_arrivals')) {
          mergedSections = defaults.featuredSections;
        } else {
          mergedSections = mergedSections.map(s => ({
            visible: s.visible !== undefined ? s.visible : true,
            ...s
          }));
        }

        // Normalize / Migrate navDropdowns
        let navDropdowns = parsed.navDropdowns || {};

        // Migrate / Normalize Unstitched structure
        if (navDropdowns.unstitched) {
          let u = navDropdowns.unstitched;
          let cols = [];
          if (Array.isArray(u.columns) && u.columns.length > 0) {
            cols = u.columns.map(c => ({
              id: c.id || ('col_' + Math.random().toString(36).substr(2, 9)),
              label: c.label || 'Submenu',
              url: c.url || 'collections.html?category=Unstitched',
              visible: c.visible !== undefined ? c.visible : true,
              isCustom: c.isCustom !== undefined ? c.isCustom : false,
              sublinks: Array.isArray(c.sublinks) ? c.sublinks : []
            }));
          } else {
            const legacy1 = u.items1pc || defaults.navDropdowns.unstitched.columns[0];
            const legacy2 = u.items2pc || defaults.navDropdowns.unstitched.columns[1];
            const legacy3 = u.items3pc || defaults.navDropdowns.unstitched.columns[2];
            const legacy4 = u.items4pc || defaults.navDropdowns.unstitched.columns[3];
            const legacy5 = u.items5pc || defaults.navDropdowns.unstitched.columns[4];
            cols = [
              { id: '1pc', label: legacy1.label || '1PC', url: legacy1.url || 'collections.html?category=Unstitched&type=1PC', visible: legacy1.visible !== false, isCustom: false, sublinks: legacy1.sublinks || [] },
              { id: '2pc', label: legacy2.label || '2PC', url: legacy2.url || 'collections.html?category=Unstitched&type=2PC', visible: legacy2.visible !== false, isCustom: false, sublinks: legacy2.sublinks || [] },
              { id: '3pc', label: legacy3.label || '3PC', url: legacy3.url || 'collections.html?category=Unstitched&type=3PC', visible: legacy3.visible !== false, isCustom: false, sublinks: legacy3.sublinks || [] },
              { id: '4pc', label: legacy4.label || '4PC', url: legacy4.url || 'collections.html?category=Unstitched&type=4PC', visible: legacy4.visible === true, isCustom: false, sublinks: legacy4.sublinks || [] },
              { id: '5pc', label: legacy5.label || '5PC', url: legacy5.url || 'collections.html?category=Unstitched&type=5PC', visible: legacy5.visible === true, isCustom: false, sublinks: legacy5.sublinks || [] }
            ];
          }

          // Ensure 1PC has Bedsheets in its sublinks
          const c1 = cols.find(c => c.id === '1pc' || c.label === '1PC');
          if (c1 && Array.isArray(c1.sublinks)) {
            if (!c1.sublinks.some(s => /bedsheet/i.test(s.label))) {
              c1.sublinks.push({ label: 'Bedsheets', url: 'collections.html?type=Bedsheet' });
            }
          }

          navDropdowns.unstitched = {
            visible: u.visible !== undefined ? u.visible : true,
            label: u.label || 'UNSTITCHED',
            url: u.url || 'collections.html?category=Unstitched',
            columns: cols,
            items1pc: cols.find(c => c.id === '1pc') || cols[0],
            items2pc: cols.find(c => c.id === '2pc') || cols[1],
            items3pc: cols.find(c => c.id === '3pc') || cols[2],
            items4pc: cols.find(c => c.id === '4pc') || cols[3],
            items5pc: cols.find(c => c.id === '5pc') || cols[4]
          };
        } else {
          navDropdowns.unstitched = defaults.navDropdowns.unstitched;
        }

        // Migrate Ready to Wear structure
        if (Array.isArray(navDropdowns.readyToWear)) {
          navDropdowns.readyToWear = {
            visible: true,
            label: 'READY TO WEAR',
            url: 'collections.html?category=Ready+to+Wear',
            links: navDropdowns.readyToWear.map(l => typeof l === 'object' ? { visible: true, ...l } : { label: l, url: 'collections.html?category=Ready+to+Wear', visible: true })
          };
        } else if (!navDropdowns.readyToWear) {
          navDropdowns.readyToWear = defaults.navDropdowns.readyToWear;
        }

        // Migrate Kids structure
        if (Array.isArray(navDropdowns.kids)) {
          navDropdowns.kids = {
            visible: true,
            label: 'KIDS',
            url: 'collections.html?category=Kids',
            links: navDropdowns.kids.map(l => typeof l === 'object' ? { visible: true, ...l } : { label: l, url: 'collections.html?category=Kids', visible: true })
          };
        } else if (!navDropdowns.kids) {
          navDropdowns.kids = defaults.navDropdowns.kids;
        }

        if (!navDropdowns.mainNavLinks) {
          navDropdowns.mainNavLinks = defaults.navDropdowns.mainNavLinks;
        }

        let announcementText = parsed.announcementText || defaults.announcementText;

        return {
          ...defaults,
          ...parsed,
          announcementText,
          featuredSections: mergedSections,
          navDropdowns
        };
      }
    } catch (e) {
      console.warn('Error loading settings:', e);
    }
    return defaults;
  },

  saveSiteSettings(newSettings, adminPasscode) {
    try {
      const current = this.getSiteSettings();
      const updated = {
        ...current,
        ...newSettings,
        navDropdowns: {
          ...(current.navDropdowns || {}),
          ...((newSettings && newSettings.navDropdowns) || {})
        }
      };
      localStorage.setItem('aldeewan_site_settings', JSON.stringify(updated));
      this.applySiteSettings();
      window.dispatchEvent(new CustomEvent('settings:updated', { detail: updated }));

      // Sync to Server API so all devices and visitors receive changes live
      const passcode = adminPasscode || localStorage.getItem('aldeewan_admin_pass') || 'deewan2026';
      fetch('api/settings.php', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Admin-Passcode': passcode
        },
        body: JSON.stringify({ ...updated, adminPasscode: passcode })
      })
      .then(res => res.json())
      .then(data => {
        if (data && data.success) {
          console.log('✅ Site settings synced to server for all devices:', data.message);
        } else {
          console.warn('⚠️ Server response on settings sync:', data);
        }
      })
      .catch(e => console.warn('Site settings server sync note:', e));

      return true;
    } catch (e) {
      console.error('Failed to save settings:', e);
      return false;
    }
  },

  // Apply Site Settings Dynamically to DOM
  applySiteSettings() {
    const settings = this.getSiteSettings();

    // 1. Below-Hero Animated Marquee Ticker (Controlled by Announcement Text in Admin)
    if (settings.announcementText) {
      const tickerContainer = document.querySelector('.announcement-bar__ticker');
      if (tickerContainer) {
        const rawText = settings.announcementText.trim();
        let parts = rawText.split(/[•|]/).map(s => s.trim().replace(/^⚡|⚡$/g, '').trim()).filter(Boolean);
        if (!parts.length) parts = [rawText];
        const makeItems = () => parts.map(p => `
          <div class="announcement-bar__item">
            <span class="announcement-bar__flash">⚡</span>
            <span>${p}</span>
          </div>
        `).join('');
        tickerContainer.innerHTML = makeItems() + makeItems() + makeItems() + makeItems();
      }
    }

    // 2. Hero Banner Slider Carousel
    if (settings.heroSlides && settings.heroSlides.length > 0) {
      if (typeof window.MainUI_renderHeroSlider === 'function') {
        window.MainUI_renderHeroSlider(settings.heroSlides, settings.heroAutoplaySpeed || 5000);
      }
    }

    // Fallback single hero banner
    const heroImg = document.querySelector('.hero-banner img, .hero-section img, .hero-banner-section img, .hero-banner-img');
    if (heroImg && settings.heroSlides && settings.heroSlides[0]) {
      heroImg.src = settings.heroSlides[0].image;
    }
    document.querySelectorAll('.hero-slider-section picture source, .hero-banner picture source, .hero-banner-section picture source').forEach(source => {
      if (settings.heroSlides && settings.heroSlides[0]) {
        source.srcset = settings.heroSlides[0].image;
      }
    });
    const heroLink = document.querySelector('.hero-banner a, .hero-section a, .hero-banner-section a, .hero-banner-link');
    if (heroLink && settings.heroSlides && settings.heroSlides[0]) {
      heroLink.href = settings.heroSlides[0].link || '#';
    }

    // 3. Welcome Promotional Banner
    const promoImg = document.querySelector('.welcome-promo-banner img, #home-promo-banner img');
    if (promoImg) {
      const bannerSrc = (settings.welcomeBanner && settings.welcomeBanner.image) ? settings.welcomeBanner.image : 'assets/images/web_banner_promo.png';
      promoImg.src = bannerSrc;
      promoImg.loading = 'eager';
      promoImg.onerror = function() {
        this.onerror = null;
        this.src = 'assets/images/web_banner_promo.png';
      };
    }
    const promoLink = document.querySelector('.welcome-promo-banner a, #home-promo-banner a');
    if (promoLink && settings.welcomeBanner && settings.welcomeBanner.link) {
      promoLink.href = settings.welcomeBanner.link;
    }

    // 4. Brand Ticker Headings
    const brandTickerH2 = document.querySelector('.brands-title h2');
    if (brandTickerH2 && settings.brandTickerText) {
      brandTickerH2.innerHTML = settings.brandTickerText.replace(/ /g, '<br>');
    }

    // 5. Featured Section Headings & Links & Visibility (Homepage Collections)
    const featuredSecs = settings.featuredSections || [];
    // Section 1: Bin Saeed
    const s1 = featuredSecs.find(s => s.id === 'section_binsaeed') || featuredSecs[0];
    const block1 = document.getElementById('section-block-binsaeed');
    if (block1) {
      block1.style.display = (s1 && s1.visible !== false) ? '' : 'none';
    }
    if (s1) {
      const h1 = document.getElementById('heading-binsaeed');
      const l1 = document.getElementById('link-binsaeed');
      if (h1 && s1.title) h1.textContent = s1.title;
      if (l1 && s1.viewAllUrl) l1.href = s1.viewAllUrl;
    }

    // Section 2: Unstitched 3PC
    const s2 = featuredSecs.find(s => s.id === 'section_unstitched') || featuredSecs[1];
    const block2 = document.getElementById('section-block-unstitched');
    if (block2) {
      block2.style.display = (s2 && s2.visible !== false) ? '' : 'none';
    }
    if (s2) {
      const h2 = document.getElementById('heading-unstitched');
      const l2 = document.getElementById('link-unstitched');
      if (h2 && s2.title) h2.textContent = s2.title;
      if (l2 && s2.viewAllUrl) l2.href = s2.viewAllUrl;
    }

    // Section 3: Ready to Wear (Block 3)
    const s3 = featuredSecs.find(s => s.id === 'section_rtw') || featuredSecs[2];
    const block3 = document.getElementById('section-block-rtw');
    if (block3) {
      block3.style.display = (s3 && s3.visible !== false) ? '' : 'none';
    }
    if (s3) {
      const h3 = document.getElementById('heading-rtw');
      const l3 = document.getElementById('link-rtw');
      if (h3 && s3.title) h3.textContent = s3.title;
      if (l3 && s3.viewAllUrl) l3.href = s3.viewAllUrl;
    }

    // Section 4: Top Designer Suits
    const s4 = featuredSecs.find(s => s.id === 'section_designer') || featuredSecs[3];
    const block4 = document.getElementById('section-block-designer');
    if (block4) {
      block4.style.display = (s4 && s4.visible !== false) ? '' : 'none';
    }
    if (s4) {
      const h4 = document.getElementById('heading-designer');
      const l4 = document.getElementById('link-designer');
      if (h4 && s4.title) h4.textContent = s4.title;
      if (l4 && s4.viewAllUrl) l4.href = s4.viewAllUrl;
    }

    // 6. Navigation Dropdowns & Menus (Hideable & Editable with 1PC, 2PC, 3PC, 4PC, 5PC support)
    if (settings.navDropdowns) {
      const navs = settings.navDropdowns;

      // Desktop Nav Items
      const allDropdowns = Array.from(document.querySelectorAll('.nav-item-dropdown, .nav-item'));
      const unstitchedDropdown = document.getElementById('nav-dropdown-unstitched') || allDropdowns.find(el => {
        const txt = el.textContent.trim().toUpperCase();
        return txt.startsWith('UNSTITCHED') || !!el.querySelector('a[href*="Unstitched"]');
      });
      const rtwDropdown = document.getElementById('nav-dropdown-rtw') || allDropdowns.find(el => {
        const txt = el.textContent.trim().toUpperCase();
        return txt.startsWith('READY TO WEAR') || !!el.querySelector('a[href*="Ready"]');
      });
      const kidsDropdown = document.getElementById('nav-dropdown-kids') || allDropdowns.find(el => {
        const txt = el.textContent.trim().toUpperCase();
        return txt.startsWith('KIDS') || !!el.querySelector('a[href*="Kids"]');
      });

      // 6a. UNSTITCHED Dropdown (1PC, 2PC, 3PC, 4PC, 5PC + Custom submenus)
      if (unstitchedDropdown && navs.unstitched) {
        const uCfg = navs.unstitched;
        unstitchedDropdown.style.display = (uCfg.visible !== false) ? '' : 'none';
        const topLink = unstitchedDropdown.querySelector('.header-nav__link');
        if (topLink && uCfg.url) topLink.href = uCfg.url;

        const menu = unstitchedDropdown.querySelector('.nav-dropdown-menu');
        if (menu) {
          const cols = Array.isArray(uCfg.columns) ? uCfg.columns : [
            uCfg.items1pc, uCfg.items2pc, uCfg.items3pc, uCfg.items4pc, uCfg.items5pc
          ].filter(Boolean);

          const visibleCols = cols.filter(c => c && c.visible !== false && c.sublinks && c.sublinks.length > 0);

          menu.innerHTML = visibleCols.map(col => `
            <li class="nav-dropdown-item has-submenu">
              <a href="${col.url || `collections.html?category=Unstitched&type=${encodeURIComponent(col.label || '')}`}" class="nav-dropdown-link">
                <span>${col.label || 'Submenu'}</span>
                <svg class="nav-arrow-right" width="6" height="10" viewBox="0 0 6 10" fill="currentColor"><path d="M0.5 0L5.5 5L0.5 10V0Z"/></svg>
              </a>
              <ul class="nav-submenu">
                ${col.sublinks.map(item => `<li><a href="${item.url}" class="nav-dropdown-link">${item.label}</a></li>`).join('')}
              </ul>
            </li>
          `).join('');
        }
      }

      // 6b. READY TO WEAR Dropdown (1PC, 2PC, 3PC, etc.)
      if (rtwDropdown && navs.readyToWear) {
        const rtwCfg = navs.readyToWear;
        rtwDropdown.style.display = (rtwCfg.visible !== false) ? '' : 'none';
        const topLink = rtwDropdown.querySelector('.header-nav__link');
        if (topLink && rtwCfg.url) topLink.href = rtwCfg.url;

        const menu = rtwDropdown.querySelector('.nav-dropdown-menu');
        if (menu && rtwCfg.links) {
          const visibleLinks = rtwCfg.links.filter(l => l.visible !== false);
          menu.innerHTML = visibleLinks.map(item => `
            <li class="nav-dropdown-item">
              <a href="${item.url}" class="nav-dropdown-link">${item.label}</a>
            </li>
          `).join('');
        }
      }

      // 6c. KIDS Dropdown
      if (kidsDropdown && navs.kids) {
        const kCfg = navs.kids;
        kidsDropdown.style.display = (kCfg.visible !== false) ? '' : 'none';
        const topLink = kidsDropdown.querySelector('.header-nav__link');
        if (topLink && kCfg.url) topLink.href = kCfg.url;

        const menu = kidsDropdown.querySelector('.nav-dropdown-menu');
        if (menu && kCfg.links) {
          const visibleLinks = kCfg.links.filter(l => l.visible !== false);
          menu.innerHTML = visibleLinks.map(item => `
            <li class="nav-dropdown-item">
              <a href="${item.url}" class="nav-dropdown-link">${item.label}</a>
            </li>
          `).join('');
        }
      }

      // 6d. Mobile Nav Drawer Dropdown Submenus Synchronization
      const mobileNavHeaders = document.querySelectorAll('#mobile-nav-drawer .mobile-nav-header a');
      mobileNavHeaders.forEach(link => {
        const linkText = link.textContent.trim().toUpperCase();
        const parentItem = link.closest('.mobile-nav-item');

        if (linkText === 'UNSTITCHED') {
          if (navs.unstitched && parentItem) {
            parentItem.style.display = (navs.unstitched.visible !== false) ? '' : 'none';
            const submenu = parentItem.querySelector('.mobile-submenu');
            if (submenu) {
              const u = navs.unstitched;
              const cols = Array.isArray(u.columns) ? u.columns : [
                u.items1pc, u.items2pc, u.items3pc, u.items4pc, u.items5pc
              ].filter(Boolean);

              const visibleCols = cols.filter(c => c && c.visible !== false && c.sublinks && c.sublinks.length > 0);

              submenu.innerHTML = visibleCols.map(col => `
                <li class="mobile-nav-item has-submenu">
                  <div class="mobile-nav-header">
                    <a href="${col.url || `collections.html?category=Unstitched&type=${encodeURIComponent(col.label || '')}`}">${col.label || 'Submenu'}</a>
                    <button class="mobile-nav-toggle" aria-label="Toggle Submenu">+</button>
                  </div>
                  <ul class="mobile-submenu">
                    ${col.sublinks.map(item => `<li><a href="${item.url}">${item.label}</a></li>`).join('')}
                  </ul>
                </li>
              `).join('');
            }
          }
        } else if (linkText === 'READY TO WEAR') {
          if (navs.readyToWear && parentItem) {
            parentItem.style.display = (navs.readyToWear.visible !== false) ? '' : 'none';
            const submenu = parentItem.querySelector('.mobile-submenu');
            if (submenu && navs.readyToWear.links) {
              const visibleLinks = navs.readyToWear.links.filter(l => l.visible !== false);
              submenu.innerHTML = visibleLinks.map(item => `
                <li><a href="${item.url}">${item.label}</a></li>
              `).join('');
            }
          }
        } else if (linkText === 'KIDS' || linkText === 'CHILDREN') {
          if (navs.kids && parentItem) {
            parentItem.style.display = (navs.kids.visible !== false) ? '' : 'none';
            const submenu = parentItem.querySelector('.mobile-submenu');
            if (submenu && navs.kids.links) {
              const visibleLinks = navs.kids.links.filter(l => l.visible !== false);
              submenu.innerHTML = visibleLinks.map(item => `
                <li><a href="${item.url}">${item.label}</a></li>
              `).join('');
            }
          }
        }
      });
    }
  },

  // --- Brand Directory & Top Favorite Brands Management ---
  getDefaultBrands() {
    return [
      { id: 'b_kayseria', name: 'Kayseria', img: 'assets/images/brands/kayseria.png', logo: 'assets/images/brands/kayseria.png', letter: 'K', isFavorite: true, isTopFavorite: true, visible: true, hidden: false },
      { id: 'b_khaadi', name: 'Khaadi', img: 'assets/images/brands/khaadi.png', logo: 'assets/images/brands/khaadi.png', letter: 'K', isFavorite: true, isTopFavorite: true, visible: true, hidden: false },
      { id: 'b_sapphire', name: 'Sapphire', img: 'assets/images/brands/sapphire.png', logo: 'assets/images/brands/sapphire.png', letter: 'S', isFavorite: true, isTopFavorite: true, visible: true, hidden: false },
      { id: 'b_nishat', name: 'Nishat Linen', img: 'assets/images/brands/nishat.png', logo: 'assets/images/brands/nishat.png', letter: 'N', isFavorite: true, isTopFavorite: true, visible: true, hidden: false },
      { id: 'b_alkaram', name: 'Alkaram Studio', img: 'assets/images/brands/alkaram.png', logo: 'assets/images/brands/alkaram.png', letter: 'A', isFavorite: true, isTopFavorite: true, visible: true, hidden: false },
      { id: 'b_asim_jofa', name: 'Asim Jofa', img: 'assets/images/brands/asim_jofa.png', logo: 'assets/images/brands/asim_jofa.png', letter: 'A', isFavorite: true, isTopFavorite: true, visible: true, hidden: false },
      { id: 'b_bonanza', name: 'Bonanza Satrangi', img: 'assets/images/brands/bonanza.png', logo: 'assets/images/brands/bonanza.png', letter: 'B', isFavorite: true, isTopFavorite: true, visible: true, hidden: false },
      { id: 'b_prime_point', name: 'Prime Point', img: 'assets/images/brands/prime_point.png', logo: 'assets/images/brands/prime_point.png', letter: 'P', isFavorite: true, isTopFavorite: true, visible: true, hidden: false },
      { id: 'b_bareeze', name: 'Bareeze', img: 'assets/images/brands/bareeze.png', logo: 'assets/images/brands/bareeze.png', letter: 'B', isFavorite: true, isTopFavorite: true, visible: true, hidden: false },
      { id: 'b_bin_saeed', name: 'Bin Saeed', img: 'assets/images/brands/bin_saeed.png', logo: 'assets/images/brands/bin_saeed.png', letter: 'B', isFavorite: true, isTopFavorite: true, visible: true, hidden: false },
      { id: 'b_gul_ahmed', name: 'Gul Ahmed', img: 'assets/images/brands/gul_ahmed.png', logo: 'assets/images/brands/gul_ahmed.png', letter: 'G', isFavorite: true, isTopFavorite: true, visible: true, hidden: false },
      { id: 'b_maria_b', name: 'Maria B', img: 'assets/images/brands/maria_b.png', logo: 'assets/images/brands/maria_b.png', letter: 'M', isFavorite: true, isTopFavorite: true, visible: true, hidden: false },
      { id: 'b_limelight', name: 'Limelight', img: 'assets/images/brands/limelight.png', logo: 'assets/images/brands/limelight.png', letter: 'L', isFavorite: true, isTopFavorite: true, visible: true, hidden: false },
      { id: 'b_ethnic', name: 'Ethnic', img: 'assets/images/brands/ethnic.png', logo: 'assets/images/brands/ethnic.png', letter: 'E', isFavorite: true, isTopFavorite: true, visible: true, hidden: false },
      { id: 'b_saya', name: 'Saya', img: 'assets/images/brands/saya.png', logo: 'assets/images/brands/saya.png', letter: 'S', isFavorite: true, isTopFavorite: true, visible: true, hidden: false },
      { id: 'b_sana_safinaz', name: 'Sana Safinaz', img: 'assets/images/brands/sana_safinaz.png', logo: 'assets/images/brands/sana_safinaz.png', letter: 'S', isFavorite: true, isTopFavorite: true, visible: true, hidden: false },
      { id: 'b_agha_noor', name: 'Agha Noor', img: 'assets/images/brands/agha_noor.png', logo: 'assets/images/brands/agha_noor.png', letter: 'A', isFavorite: true, isTopFavorite: true, visible: true, hidden: false },
      { id: 'b_baroque', name: 'Baroque', img: 'assets/images/brands/baroque.png', logo: 'assets/images/brands/baroque.png', letter: 'B', isFavorite: true, isTopFavorite: true, visible: true, hidden: false },
      // Complete A-Z Directory Brands:
      { id: 'b_almirah', name: 'Almirah', img: '', logo: '', letter: 'A', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_afrozeh', name: 'Afrozeh', img: '', logo: '', letter: 'A', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_bin_ilyas', name: 'Bin Ilyas', img: 'assets/images/brands/bin_ilyas.png', logo: 'assets/images/brands/bin_ilyas.png', letter: 'B', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_beechtree', name: 'Beechtree', img: 'assets/images/brands/beechtree.png', logo: 'assets/images/brands/beechtree.png', letter: 'B', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_coco', name: 'Coco', img: 'assets/images/brands/coco.png', logo: 'assets/images/brands/coco.png', letter: 'C', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_designer_lawn', name: 'Designer Lawn', img: '', logo: '', letter: 'D', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_dhanak', name: 'Dhanak', img: '', logo: '', letter: 'D', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_ethnic_outfitters', name: 'Ethnic by Outfitters', img: '', logo: '', letter: 'E', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_edenrobe', name: 'Edenrobe', img: '', logo: '', letter: 'E', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_generation', name: 'Generation', img: '', logo: '', letter: 'G', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_hania_minnahil', name: 'Hania & Minnahil', img: '', logo: '', letter: 'H', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_hussain_rehar', name: 'Hussain Rehar', img: '', logo: '', letter: 'H', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_ideas', name: 'Ideas', img: 'assets/images/brands/ideas.png', logo: 'assets/images/brands/ideas.png', letter: 'I', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_junaid_jamshed', name: 'J. (Junaid Jamshed)', img: 'assets/images/brands/j.png', logo: 'assets/images/brands/j.png', letter: 'J', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_jacquard', name: 'Jacquard', img: 'assets/images/brands/jacquard.png', logo: 'assets/images/brands/jacquard.png', letter: 'J', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_jade', name: 'Jade', img: 'assets/images/brands/jade.png', logo: 'assets/images/brands/jade.png', letter: 'J', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_jaffrani', name: 'Jaffrani', img: 'assets/images/brands/jaffrani.png', logo: 'assets/images/brands/jaffrani.png', letter: 'J', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_johra', name: 'Johra', img: '', logo: '', letter: 'J', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_kross_kulture', name: 'Kross Kulture', img: '', logo: '', letter: 'K', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_lala', name: 'Lala', img: '', logo: '', letter: 'L', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_mahnur', name: 'Mahnur', img: 'assets/images/brands/mahnur.png', logo: 'assets/images/brands/mahnur.png', letter: 'M', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_meerak', name: 'Meerak', img: 'assets/images/brands/meerak.png', logo: 'assets/images/brands/meerak.png', letter: 'M', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_mix_brand', name: 'Mix Brand', img: '', logo: '', letter: 'M', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_noor_jahan', name: 'Noor Jahan', img: '', logo: '', letter: 'N', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_parishay', name: 'Parishay', img: 'assets/images/brands/parishay.png', logo: 'assets/images/brands/parishay.png', letter: 'P', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_pop_corn', name: 'Pop Corn', img: '', logo: '', letter: 'P', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_rajbari', name: 'Rajbari', img: '', logo: '', letter: 'R', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_rang_rasiya', name: 'Rang Rasiya', img: '', logo: '', letter: 'R', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_regalia', name: 'Regalia', img: '', logo: '', letter: 'R', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_suhana', name: 'Suhana', img: 'assets/images/brands/suhana.png', logo: 'assets/images/brands/suhana.png', letter: 'S', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_safa_iman', name: 'Safa Iman', img: '', logo: '', letter: 'S', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_soha_afreen', name: 'Soha Afreen', img: 'assets/images/brands/soha_afreen.png', logo: 'assets/images/brands/soha_afreen.png', letter: 'S', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_stylo', name: 'Stylo', img: '', logo: '', letter: 'S', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_tawakal', name: 'Tawakal', img: '', logo: '', letter: 'T', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_taana_baana', name: 'Taana Baana', img: '', logo: '', letter: 'T', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_thames', name: 'Thames', img: 'assets/images/brands/thames.png', logo: 'assets/images/brands/thames.png', letter: 'T', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_wirs', name: 'Wirs', img: '', logo: '', letter: 'W', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_warda', name: 'Warda', img: '', logo: '', letter: 'W', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_zain_zee', name: 'Zain Zee', img: '', logo: '', letter: 'Z', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_zellbury', name: 'Zellbury', img: '', logo: '', letter: 'Z', isFavorite: false, isTopFavorite: false, visible: true, hidden: false },
      { id: 'b_zaha', name: 'Zaha', img: '', logo: '', letter: 'Z', isFavorite: false, isTopFavorite: false, visible: true, hidden: false }
    ];
  },

  getBrands() {
    try {
      const saved = localStorage.getItem('aldeewan_brands');
      if (saved) {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.length > 0) return parsed;
      }
    } catch (e) {
      console.warn('Error reading saved brands:', e);
    }
    const defaults = this.getDefaultBrands();
    try {
      localStorage.setItem('aldeewan_brands', JSON.stringify(defaults));
    } catch (e) {}
    return defaults;
  },

  saveBrands(brands, adminPasscode) {
    try {
      localStorage.setItem('aldeewan_brands', JSON.stringify(brands));
      window.dispatchEvent(new CustomEvent('brands:updated', { detail: { brands } }));

      // Sync to Server API so all devices and visitors receive updated brands live
      const passcode = adminPasscode || localStorage.getItem('aldeewan_admin_pass') || 'deewan2026';
      fetch('api/brands.php', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Admin-Passcode': passcode
        },
        body: JSON.stringify({ brands, adminPasscode: passcode })
      })
      .then(res => res.json())
      .then(data => {
        if (data && data.success) {
          console.log('✅ Brands synced to server for all devices:', data.message);
        }
      })
      .catch(e => console.warn('Brands server sync note:', e));
    } catch (e) {
      console.error('Error saving brands:', e);
    }
  },

  getTopFavoriteBrands() {
    const brands = this.getBrands();
    return brands
      .filter(b => (b.isFavorite || b.isTopFavorite) && b.visible !== false && !b.hidden && (b.img || b.logo))
      .map(b => ({
        ...b,
        img: b.img || b.logo,
        logo: b.logo || b.img
      }));
  },

  normalizeBrandStr(str) {
    if (!str) return '';
    return str.toLowerCase().replace(/[^a-z0-9]/g, '');
  },

  matchBrandName(vendor, target) {
    if (!vendor || !target) return false;
    const v = this.normalizeBrandStr(vendor);
    const t = this.normalizeBrandStr(target);
    if (v === t) return true;

    if ((v.includes('alkaram') || v.includes('alkaramstudio')) && (t.includes('alkaram') || t.includes('alkaramstudio'))) return true;
    if ((v.includes('nishat') || v.includes('nishatlinen')) && (t.includes('nishat') || t.includes('nishatlinen'))) return true;
    if ((v.includes('gulahmed') || v.includes('ideas')) && (t.includes('gulahmed') || t.includes('ideas'))) return true;
    if ((v === 'j' || v.includes('junaidjamshed')) && (t === 'j' || t.includes('junaidjamshed'))) return true;
    if (v.includes('ethnic') && t.includes('ethnic')) return true;
    if (v.includes('mariab') && t.includes('mariab')) return true;
    if (v.includes('binsaeed') && t.includes('binsaeed')) return true;
    if (v.includes('asimjofa') && t.includes('asimjofa')) return true;
    if (v.includes('baroque') && t.includes('baroque')) return true;
    if (v.includes('sapphire') && t.includes('sapphire')) return true;
    if (v.includes('kayseria') && t.includes('kayseria')) return true;
    if (v.includes('aghanoor') && t.includes('aghanoor')) return true;
    if (v.includes('bonanza') && t.includes('bonanza')) return true;
    if (v.includes('limelight') && t.includes('limelight')) return true;
    if (v.includes('khaadi') && t.includes('khaadi')) return true;
    if (v.includes('bareeze') && t.includes('bareeze')) return true;
    if (v.includes('beechtree') && t.includes('beechtree')) return true;

    return v.includes(t) || t.includes(v);
  },

  addBrand(brandData) {
    const brands = this.getBrands();
    const name = (brandData.name || '').trim();
    if (!name) return null;
    const letter = (brandData.letter || name.charAt(0).toUpperCase() || 'A').toUpperCase();
    const id = brandData.id || ('b_' + name.toLowerCase().replace(/[^a-z0-9]/g, '_') + '_' + Date.now());
    const isFav = !!(brandData.isFavorite || brandData.isTopFavorite);
    const logoImg = brandData.logo || brandData.img || '';
    const isVis = brandData.visible !== false && !brandData.hidden;
    const newBrand = {
      id,
      name,
      img: logoImg,
      logo: logoImg,
      letter,
      isFavorite: isFav,
      isTopFavorite: isFav,
      visible: isVis,
      hidden: !isVis
    };
    brands.push(newBrand);
    this.saveBrands(brands);
    return newBrand;
  },

  updateBrand(brandId, brandData) {
    let brands = this.getBrands();
    const idx = brands.findIndex(b => b.id === brandId);
    if (idx > -1) {
      const name = brandData.name !== undefined ? brandData.name.trim() : brands[idx].name;
      const letter = (brandData.letter || name.charAt(0).toUpperCase() || brands[idx].letter).toUpperCase();
      const isFav = brandData.isFavorite !== undefined ? !!brandData.isFavorite : (brandData.isTopFavorite !== undefined ? !!brandData.isTopFavorite : (brands[idx].isFavorite || brands[idx].isTopFavorite || false));
      const logoImg = brandData.logo !== undefined ? brandData.logo : (brandData.img !== undefined ? brandData.img : (brands[idx].logo || brands[idx].img || ''));
      const isVis = brandData.visible !== undefined ? (brandData.visible !== false) : (brandData.hidden !== undefined ? !brandData.hidden : (brands[idx].visible !== false && !brands[idx].hidden));

      brands[idx] = {
        ...brands[idx],
        ...brandData,
        name,
        letter,
        img: logoImg,
        logo: logoImg,
        isFavorite: isFav,
        isTopFavorite: isFav,
        visible: isVis,
        hidden: !isVis
      };
      this.saveBrands(brands);
      return brands[idx];
    }
    return null;
  },

  deleteBrand(brandId) {
    let brands = this.getBrands();
    brands = brands.filter(b => b.id !== brandId);
    this.saveBrands(brands);
  },

  resetBrands() {
    const defaults = this.getDefaultBrands();
    this.saveBrands(defaults);
    return defaults;
  },

  exportCatalogJS() {
    const products = this.getProducts();
    return `window.CATALOG_PRODUCTS = ${JSON.stringify(products, null, 2)};\n`;
  },

  resetCatalog() {
    localStorage.removeItem('aldeewan_custom_catalog');
    localStorage.removeItem('aldeewan_site_settings');
    localStorage.removeItem('aldeewan_brands');
    window.location.reload();
  },

  // Server-Wide Live Synchronization Engine (Multi-Device & Visitor Sync)
  async syncFromServer() {
    // 1. Sync Site Settings (Ticker, Hero Slides, Banners, Nav Dropdowns, Sections)
    try {
      let settingsData = null;
      try {
        const res = await fetch(`api/settings.php?_t=${Date.now()}`, { cache: 'no-store' });
        if (res.ok) {
          const contentType = res.headers.get('content-type') || '';
          if (contentType.includes('application/json')) {
            settingsData = await res.json();
          }
        }
      } catch (err) {
        // Fallback to data/settings.json
      }

      if (!settingsData || settingsData.status === 'empty') {
        try {
          const resStatic = await fetch(`data/settings.json?_t=${Date.now()}`, { cache: 'no-store' });
          if (resStatic.ok) {
            settingsData = await resStatic.json();
          }
        } catch (err2) {}
      }

      if (settingsData && typeof settingsData === 'object' && !Array.isArray(settingsData) && Object.keys(settingsData).length > 0) {
        const current = localStorage.getItem('aldeewan_site_settings');
        const currentObj = current ? JSON.parse(current) : null;
        
        const merged = {
          ...(this.getDefaultSettings()),
          ...(currentObj || {}),
          ...settingsData
        };

        localStorage.setItem('aldeewan_site_settings', JSON.stringify(merged));
        this.applySiteSettings();
        window.dispatchEvent(new CustomEvent('settings:updated', { detail: merged }));
      }
    } catch (e) {
      console.warn('Server settings sync note:', e);
    }

    // 2. Sync Products Catalog
    try {
      let productsData = null;
      try {
        const res = await fetch(`api/products.php?_t=${Date.now()}`, { cache: 'no-store' });
        if (res.ok) {
          const contentType = res.headers.get('content-type') || '';
          if (contentType.includes('application/json')) {
            productsData = await res.json();
          }
        }
      } catch (err) {}

      if (!productsData || !Array.isArray(productsData) || productsData.length === 0) {
        try {
          const resStatic = await fetch(`data/products.json?_t=${Date.now()}`, { cache: 'no-store' });
          if (resStatic.ok) {
            productsData = await resStatic.json();
          }
        } catch (err2) {}
      }

      if (Array.isArray(productsData) && productsData.length > 0) {
        window.CATALOG_PRODUCTS = productsData;
        localStorage.setItem('aldeewan_custom_catalog', JSON.stringify(productsData));
        window.dispatchEvent(new CustomEvent('catalog:updated', { detail: { products: productsData } }));
      }
    } catch (e) {
      console.warn('Server products sync note:', e);
    }

    // 3. Sync Brands Directory
    try {
      let brandsData = null;
      try {
        const res = await fetch(`api/brands.php?_t=${Date.now()}`, { cache: 'no-store' });
        if (res.ok) {
          const contentType = res.headers.get('content-type') || '';
          if (contentType.includes('application/json')) {
            brandsData = await res.json();
          }
        }
      } catch (err) {}

      if (!brandsData || !Array.isArray(brandsData) || brandsData.length === 0) {
        try {
          const resStatic = await fetch(`data/brands.json?_t=${Date.now()}`, { cache: 'no-store' });
          if (resStatic.ok) {
            brandsData = await resStatic.json();
          }
        } catch (err2) {}
      }

      if (Array.isArray(brandsData) && brandsData.length > 0) {
        localStorage.setItem('aldeewan_brands', JSON.stringify(brandsData));
        window.dispatchEvent(new CustomEvent('brands:updated', { detail: { brands: brandsData } }));
      }
    } catch (e) {
      console.warn('Server brands sync note:', e);
    }
  },

  // Init
  init() {
    this.initCatalog();
    this.updateCartCount();
    this.updateWishlistCount();
    this.applySiteSettings();
    this.syncFromServer();
  }
};

document.addEventListener('DOMContentLoaded', () => {
  Store.init();
});

// Real-time Cross-Tab Live Sync
window.addEventListener('storage', (e) => {
  if (e.key === 'aldeewan_site_settings' || e.key === 'aldeewan_custom_catalog' || e.key === 'aldeewan_brands') {
    Store.applySiteSettings();
    Store.updateCartCount();
    Store.updateWishlistCount();
  }
});

window.addEventListener('pageshow', () => {
  Store.applySiteSettings();
});

window.Store = Store;
