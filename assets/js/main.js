/**
 * Al-Deewan Brand - Master Interactive UI Logic
 * Manages Drawers, Hero Slider, Brands Carousel, Quick View, Search, & Cart UI
 */

const MainUI = {
  init() {
    this.ensureDrawersAndModals();
    this.initHeroSlider();
    this.initDrawers();
    this.initCartDrawer();
    this.initWishlistDrawer();
    this.initSearchModal();
    this.initQuickView();
    this.initMobileNav();
    this.initWhatsAppFloat();
    this.renderHeaderCartWishlist();
  },

  ensureDrawersAndModals() {
    // 1. Drawer Overlay
    if (!document.querySelector('.drawer-overlay')) {
      const overlay = document.createElement('div');
      overlay.className = 'drawer-overlay';
      document.body.appendChild(overlay);
    }

    // 2. Mobile Nav Drawer
    if (!document.getElementById('mobile-nav-drawer')) {
      const navDrawer = document.createElement('div');
      navDrawer.className = 'slide-drawer left';
      navDrawer.id = 'mobile-nav-drawer';
      navDrawer.innerHTML = `
        <div class="drawer-header">
          <div class="drawer-title">Menu</div>
          <button class="drawer-close">&times;</button>
        </div>
        <div class="drawer-body">
          <ul class="mobile-nav-list">
            <li><a href="index.html">HOME</a></li>
            <li><a href="collections.html?collection=new-in">NEW ARRIVAL 🔥</a></li>
            <li><a href="shop-by-brand.html">SHOP BY BRAND</a></li>
            <li><a href="collections.html?category=Unstitched">UNSTITCHED 3PC</a></li>
            <li><a href="collections.html?category=Ready+to+Wear">READY TO WEAR</a></li>
            <li><a href="order-tracking.html">ORDER TRACKING</a></li>
            <li style="border-top:1px solid #eee; padding-top:14px;"><a href="contact.html" style="font-size:14px; color:#666;">Contact & Support</a></li>
            <li><a href="refunds.html" style="font-size:14px; color:#666;">Refund Policy</a></li>
          </ul>
        </div>
      `;
      document.body.appendChild(navDrawer);
    }

    // 3. Cart Drawer
    if (!document.getElementById('cart-drawer')) {
      const cartDrawer = document.createElement('div');
      cartDrawer.className = 'slide-drawer';
      cartDrawer.id = 'cart-drawer';
      cartDrawer.innerHTML = `
        <div class="drawer-header">
          <div class="drawer-title">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path><line x1="3" y1="6" x2="21" y2="6"></line><path d="M16 10a4 4 0 0 1-8 0"></path></svg>
            Shopping Cart
          </div>
          <button class="drawer-close">&times;</button>
        </div>
        <div class="drawer-body">
          <div id="cart-shipping-progress"></div>
          <div id="cart-drawer-items"></div>
        </div>
        <div class="drawer-footer" id="cart-drawer-footer">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
            <span style="font-size:14px; font-weight:700;">Subtotal:</span>
            <span style="font-size:18px; font-weight:900; color:var(--color-accent-red);" id="cart-drawer-subtotal">Rs.0.00</span>
          </div>
          <p style="font-size:11px; color:#888; margin-bottom:16px;">Taxes and standard shipping calculated at checkout.</p>
          <a href="checkout.html" class="btn-primary" style="margin-bottom:8px;">PROCEED TO CHECKOUT</a>
          <a href="cart.html" class="btn-black">VIEW SHOPPING BAG</a>
        </div>
      `;
      document.body.appendChild(cartDrawer);
    }

    // 4. Wishlist Drawer
    if (!document.getElementById('wishlist-drawer')) {
      const wishlistDrawer = document.createElement('div');
      wishlistDrawer.className = 'slide-drawer';
      wishlistDrawer.id = 'wishlist-drawer';
      wishlistDrawer.innerHTML = `
        <div class="drawer-header">
          <div class="drawer-title">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg>
            My Wishlist
          </div>
          <button class="drawer-close">&times;</button>
        </div>
        <div class="drawer-body">
          <div id="wishlist-drawer-items"></div>
        </div>
      `;
      document.body.appendChild(wishlistDrawer);
    }

    // 5. Predictive Search Modal
    if (!document.getElementById('search-modal')) {
      const searchModal = document.createElement('div');
      searchModal.className = 'search-modal';
      searchModal.id = 'search-modal';
      searchModal.innerHTML = `
        <div class="container">
          <div class="search-box">
            <input type="text" id="predictive-search-input" placeholder="Search lawn suits, brands, fabrics, 3PC, 2PC..." autocomplete="off" />
            <button id="search-modal-close" aria-label="Close Search">&times;</button>
          </div>
          <div class="search-results-grid" id="search-results-grid">
            <p style="grid-column: 1/-1; text-align:center; color:#888; padding:20px;">Type at least 2 characters to search over 20,000+ lawn outfits...</p>
          </div>
        </div>
      `;
      document.body.appendChild(searchModal);
    }
  },

  // Hero Slider
  initHeroSlider() {
    const slides = document.querySelectorAll('.hero-slide');
    const dots = document.querySelectorAll('.hero-dot');
    const prevBtn = document.querySelector('.hero-arrow.prev');
    const nextBtn = document.querySelector('.hero-arrow.next');
    
    if (!slides.length) return;
    
    let currentSlide = 0;
    let slideInterval;
    
    const showSlide = (index) => {
      slides.forEach(s => s.classList.remove('active'));
      dots.forEach(d => d.classList.remove('active'));
      
      currentSlide = (index + slides.length) % slides.length;
      slides[currentSlide].classList.add('active');
      if (dots[currentSlide]) dots[currentSlide].classList.add('active');
    };
    
    const startAutoplay = () => {
      stopAutoplay();
      slideInterval = setInterval(() => {
        showSlide(currentSlide + 1);
      }, 5000);
    };
    
    const stopAutoplay = () => {
      if (slideInterval) clearInterval(slideInterval);
    };
    
    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        showSlide(currentSlide + 1);
        startAutoplay();
      });
    }
    
    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        showSlide(currentSlide - 1);
        startAutoplay();
      });
    }
    
    dots.forEach((dot, idx) => {
      dot.addEventListener('click', () => {
        showSlide(idx);
        startAutoplay();
      });
    });
    
    const heroElem = document.querySelector('.hero-slider');
    if (heroElem) {
      heroElem.addEventListener('mouseenter', stopAutoplay);
      heroElem.addEventListener('mouseleave', startAutoplay);
    }
    
    startAutoplay();
  },

  // Drawers & Overlays
  initDrawers() {
    document.addEventListener('click', (e) => {
      if (e.target.closest('.drawer-overlay') || e.target.closest('.drawer-close') || e.target.closest('#search-modal-close') || e.target.closest('.modal-close')) {
        this.closeAllDrawers();
      }
    });
    
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') this.closeAllDrawers();
    });
  },

  closeAllDrawers() {
    document.querySelectorAll('.slide-drawer, .search-modal, .quick-view-modal').forEach(el => {
      el.classList.remove('active');
    });
    const overlay = document.querySelector('.drawer-overlay');
    if (overlay) overlay.classList.remove('active');
    document.body.style.overflow = '';
  },

  // Cart Drawer
  initCartDrawer() {
    document.addEventListener('click', (e) => {
      if (e.target.closest('#cart-drawer-toggle') || e.target.closest('.cart-drawer-trigger')) {
        e.preventDefault();
        this.openCartDrawer();
      }
    });
    
    window.addEventListener('cart:updated', () => {
      this.renderCartDrawerItems();
    });
  },

  openCartDrawer() {
    this.closeAllDrawers();
    const drawer = document.getElementById('cart-drawer');
    const overlay = document.querySelector('.drawer-overlay');
    if (drawer) {
      this.renderCartDrawerItems();
      drawer.classList.add('active');
      if (overlay) overlay.classList.add('active');
      document.body.style.overflow = 'hidden';
    }
  },

  renderCartDrawerItems() {
    const container = document.getElementById('cart-drawer-items');
    const footer = document.getElementById('cart-drawer-footer');
    if (!container) return;
    
    const cart = Store.getCart();
    const subtotal = Store.getCartSubtotal();
    const freeDeliveryThreshold = 3500;
    const progressPercent = Math.min(100, Math.round((subtotal / freeDeliveryThreshold) * 100));
    
    // Render Free Shipping Bar
    const shippingProgressEl = document.getElementById('cart-shipping-progress');
    if (shippingProgressEl) {
      if (subtotal >= freeDeliveryThreshold) {
        shippingProgressEl.innerHTML = `
          <div class="free-shipping-bar" style="background:#e8f8f0; color:#1e7e4a;">
            🎉 Congratulations! You have unlocked <strong>FREE Delivery</strong> across Pakistan!
            <div class="progress-track"><div class="progress-fill" style="width: 100%; background: #27ae60;"></div></div>
          </div>
        `;
      } else {
        const remaining = freeDeliveryThreshold - subtotal;
        shippingProgressEl.innerHTML = `
          <div class="free-shipping-bar">
            Add <strong>${Store.formatMoney(remaining)}</strong> more to get <strong>FREE Delivery</strong>!
            <div class="progress-track"><div class="progress-fill" style="width: ${progressPercent}%;"></div></div>
          </div>
        `;
      }
    }
    
    if (cart.length === 0) {
      container.innerHTML = `
        <div style="text-align:center; padding: 50px 20px;">
          <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#ccc" stroke-width="1.5" style="margin:0 auto 16px;"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path><line x1="3" y1="6" x2="21" y2="6"></line><path d="M16 10a4 4 0 0 1-8 0"></path></svg>
          <h3 style="font-size: 16px; font-weight: 700; margin-bottom: 8px;">Your cart is empty</h3>
          <p style="font-size: 13px; color: #888; margin-bottom: 24px;">Looks like you haven't added anything to your cart yet.</p>
          <a href="collections.html" class="btn-primary" style="display:inline-block; width:auto; padding:10px 28px;">Start Shopping</a>
        </div>
      `;
      if (footer) footer.style.display = 'none';
      return;
    }
    
    if (footer) footer.style.display = 'block';
    
    container.innerHTML = cart.map(item => `
      <div class="cart-item" data-id="${item.id}">
        <img src="${item.image}" alt="${item.title}" class="cart-item__img" />
        <div class="cart-item__details">
          <div>
            <div class="cart-item__title">${item.title}</div>
            <div class="cart-item__price">${Store.formatMoney(item.price)}</div>
          </div>
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <div class="cart-item__qty">
              <button class="qty-btn minus" onclick="Store.updateCartQty(${item.id}, ${item.qty - 1})">-</button>
              <span class="qty-val">${item.qty}</span>
              <button class="qty-btn plus" onclick="Store.updateCartQty(${item.id}, ${item.qty + 1})">+</button>
            </div>
            <span class="cart-item__remove" onclick="Store.removeFromCart(${item.id})">Remove</span>
          </div>
        </div>
      </div>
    `).join('');
    
    const subtotalElem = document.getElementById('cart-drawer-subtotal');
    if (subtotalElem) {
      subtotalElem.textContent = Store.formatMoney(subtotal);
    }
  },

  // Wishlist Drawer
  initWishlistDrawer() {
    document.addEventListener('click', (e) => {
      if (e.target.closest('#wishlist-drawer-toggle') || e.target.closest('.wishlist-drawer-trigger')) {
        e.preventDefault();
        this.openWishlistDrawer();
      }
    });
    
    window.addEventListener('wishlist:updated', () => {
      this.renderWishlistDrawerItems();
    });
  },

  openWishlistDrawer() {
    this.closeAllDrawers();
    const drawer = document.getElementById('wishlist-drawer');
    const overlay = document.querySelector('.drawer-overlay');
    if (drawer) {
      this.renderWishlistDrawerItems();
      drawer.classList.add('active');
      if (overlay) overlay.classList.add('active');
      document.body.style.overflow = 'hidden';
    }
  },

  renderWishlistDrawerItems() {
    const container = document.getElementById('wishlist-drawer-items');
    if (!container) return;
    
    const wishlist = Store.getWishlist();
    
    if (wishlist.length === 0) {
      container.innerHTML = `
        <div style="text-align:center; padding: 50px 20px;">
          <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#ccc" stroke-width="1.5" style="margin:0 auto 16px;"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg>
          <h3 style="font-size: 16px; font-weight: 700; margin-bottom: 8px;">Your wishlist is empty</h3>
          <p style="font-size: 13px; color: #888; margin-bottom: 24px;">Explore our collections and save your favorite outfits.</p>
          <a href="collections.html" class="btn-primary" style="display:inline-block; width:auto; padding:10px 28px;">Explore Collections</a>
        </div>
      `;
      return;
    }
    
    container.innerHTML = wishlist.map(item => `
      <div class="cart-item" data-id="${item.id}">
        <img src="${item.image}" alt="${item.title}" class="cart-item__img" />
        <div class="cart-item__details">
          <div>
            <div class="cart-item__title">${item.title}</div>
            <div class="cart-item__price">${Store.formatMoney(item.price)}</div>
          </div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px;">
            <button class="btn-primary" style="padding: 6px 14px; font-size: 11px; width:auto;" onclick="Store.addToCart(window.CATALOG_PRODUCTS.find(p => p.id === ${item.id}) || {id:${item.id}, title:'${item.title.replace(/'/g, "\\'")}', price:${item.price}, featured_image:'${item.image}'})">Add To Cart</button>
            <span class="cart-item__remove" onclick="Store.toggleWishlist({id: ${item.id}})">Remove</span>
          </div>
        </div>
      </div>
    `).join('');
  },

  // Predictive Search Modal
  initSearchModal() {
    document.addEventListener('click', (e) => {
      if (e.target.closest('#search-modal-toggle') || e.target.closest('.search-trigger')) {
        e.preventDefault();
        this.closeAllDrawers();
        const modal = document.getElementById('search-modal');
        const overlay = document.querySelector('.drawer-overlay');
        const input = document.getElementById('predictive-search-input');
        if (modal) {
          modal.classList.add('active');
          if (overlay) overlay.classList.add('active');
          if (input) setTimeout(() => input.focus(), 100);
        }
      }
    });

    document.addEventListener('input', (e) => {
      if (e.target && e.target.id === 'predictive-search-input') {
        const val = e.target.value;
        const resultsGrid = document.getElementById('search-results-grid');
        if (!resultsGrid) return;
        if (!val || val.length < 2) {
          resultsGrid.innerHTML = '<p style="grid-column: 1/-1; text-align:center; color:#888; padding:20px;">Type at least 2 characters to search over 20,000+ lawn outfits...</p>';
          return;
        }
        const results = Store.search(val, 8);
        if (results.length === 0) {
          resultsGrid.innerHTML = `<p style="grid-column: 1/-1; text-align:center; color:#888; padding:20px;">No results found for "${val}". Try searching for 'Almirah', '3PC', or 'Lawn'.</p>`;
          return;
        }
        resultsGrid.innerHTML = results.map(p => this.createProductCardHTML(p)).join('');
      }
    });
  },

  // Quick View Modal
  initQuickView() {
    // Event delegation for quickview buttons
    document.addEventListener('click', (e) => {
      const qvBtn = e.target.closest('.quick-view-btn');
      if (qvBtn) {
        e.preventDefault();
        const id = parseInt(qvBtn.dataset.id);
        const product = (window.CATALOG_PRODUCTS || []).find(p => p.id === id);
        if (product) {
          this.openQuickViewModal(product);
        }
      }
    });
  },

  openQuickViewModal(product) {
    let modal = document.getElementById('quick-view-modal');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'quick-view-modal';
      modal.className = 'quick-view-modal';
      modal.innerHTML = `
        <div class="quick-view-dialog">
          <button class="modal-close" onclick="MainUI.closeAllDrawers()">&times;</button>
          <div class="quick-view-content" id="quick-view-content"></div>
        </div>
      `;
      document.body.appendChild(modal);
    }
    
    const content = document.getElementById('quick-view-content');
    const qvImg = product.featured_image || product.image || (product.images && product.images[0]) || '';
    content.innerHTML = `
      <div style="display:grid; grid-template-columns: 1fr 1fr; gap:24px;">
        <div style="background:#f8f8f8; border-radius:8px; overflow:hidden;">
          <img src="${qvImg}" alt="${product.title}" style="width:100%; height:auto; object-fit:cover;" onerror="if(this.src!=='${product.image||''}')this.src='${product.image||''}'" />
        </div>
        <div>
          <div style="font-size:11px; text-transform:uppercase; color:#888; font-weight:700; margin-bottom:4px;">${product.vendor}</div>
          <h2 style="font-size:18px; font-weight:800; margin-bottom:8px; line-height:1.3;">${product.title}</h2>
          <div style="font-size:12px; color:#666; margin-bottom:12px;">SKU: ${product.sku}</div>
          <div style="display:flex; align-items:center; gap:10px; margin-bottom:16px;">
            <span style="font-size:20px; font-weight:900; color:var(--color-accent-red);">${Store.formatMoney(product.price)}</span>
            <span style="font-size:14px; text-decoration:line-through; color:#999;">${Store.formatMoney(product.compare_at_price)}</span>
            <span class="badge-save">SAVE ${Store.formatMoney(product.save_amount)}</span>
          </div>
          <div style="display:flex; gap:10px; margin-bottom:16px;">
            <button class="btn-primary" onclick="Store.addToCart(window.CATALOG_PRODUCTS.find(p=>p.id===${product.id})); MainUI.closeAllDrawers();">Add To Cart</button>
            <a href="product.html?handle=${product.handle}" class="btn-black" style="padding:14px;">View Details</a>
          </div>
          <button class="btn-whatsapp" onclick="MainUI.orderOnWhatsApp('${product.title.replace(/'/g, "\\'")}', '${product.sku}', '${Store.formatMoney(product.price)}', '${product.handle}')">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981z"/></svg>
            Order On WhatsApp
          </button>
        </div>
      </div>
    `;
    
    modal.classList.add('active');
    const overlay = document.querySelector('.drawer-overlay');
    if (overlay) overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  },

  // Mobile Navigation Drawer
  initMobileNav() {
    document.addEventListener('click', (e) => {
      const toggle = e.target.closest('.mobile-menu-toggle, #mobile-menu-toggle');
      if (toggle) {
        e.preventDefault();
        this.closeAllDrawers();
        const drawer = document.getElementById('mobile-nav-drawer');
        const overlay = document.querySelector('.drawer-overlay');
        if (drawer) {
          drawer.classList.add('active');
          if (overlay) overlay.classList.add('active');
          document.body.style.overflow = 'hidden';
        }
      }
    });
  },

  // WhatsApp Order Generator
  orderOnWhatsApp(title, sku, price, handle) {
    const phone = '923334275944';
    const currentUrl = window.location.origin + '/product.html?handle=' + handle;
    const msg = `Hello Al-Deewan Brand,\n\nI want to order this product:\nProduct: ${title}\nSKU: ${sku}\nPrice: ${price}\nURL: ${currentUrl}\n\nPlease confirm availability and COD process. Thank you!`;
    const url = `https://api.whatsapp.com/send?phone=${phone}&text=${encodeURIComponent(msg)}`;
    window.open(url, '_blank');
  },

  // WhatsApp Floating Button
  initWhatsAppFloat() {
    let btn = document.querySelector('.whatsapp-floating-btn');
    if (!btn) {
      btn = document.createElement('a');
      btn.className = 'whatsapp-floating-btn';
      btn.href = 'https://api.whatsapp.com/send?phone=923334275944&text=Hello%20Al-Deewan%20Brand%2C%20I%20have%20an%20inquiry%20regarding%20an%20order.';
      btn.target = '_blank';
      btn.setAttribute('aria-label', 'Chat with us on WhatsApp');
      btn.innerHTML = `
        <svg viewBox="0 0 24 24"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981z"/></svg>
      `;
      document.body.appendChild(btn);
    }
  },

  // Helper to generate a single Product Card HTML
  createProductCardHTML(p) {
    const isWishlist = Store.isInWishlist(p.id);
    const imgUrl = p.featured_image || p.image || (p.images && p.images[0]) || '';
    return `
      <div class="product-card" data-id="${p.id}">
        <div class="product-card__media">
          <a href="product.html?handle=${p.handle}">
            <img src="${imgUrl}" alt="${p.title}" loading="lazy" onerror="if(this.src!=='${p.image||''}')this.src='${p.image||''}'" />
          </a>
          <span class="badge-sale">Sale ${p.discount_percent}%</span>
          ${!p.available ? '<span class="badge-soldout">Sold Out</span>' : ''}
          <div class="product-card__actions">
            <button class="card-action-btn ${isWishlist ? 'active' : ''}" title="Add to Wishlist" onclick="Store.toggleWishlist(window.CATALOG_PRODUCTS.find(x=>x.id===${p.id}))">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="${isWishlist ? '#ff3366' : 'none'}" stroke="${isWishlist ? '#ff3366' : 'currentColor'}" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg>
            </button>
            <button class="card-action-btn quick-view-btn" data-id="${p.id}" title="Quick View">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"></circle><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path></svg>
            </button>
          </div>
        </div>
        <div class="product-card__info">
          <div class="product-card__vendor">${p.vendor || 'Al-Deewan Brand'}</div>
          <a href="product.html?handle=${p.handle}" class="product-card__title">${p.title}</a>
          <div class="product-card__prices">
            <span class="price-compare">${Store.formatMoney(p.compare_at_price)}</span>
            <span class="price-regular">${Store.formatMoney(p.price)}</span>
          </div>
          <span class="badge-save">SAVE ${Store.formatMoney(p.save_amount)}</span>
        </div>
      </div>
    `;
  },

  renderHeaderCartWishlist() {
    Store.updateCartCount();
    Store.updateWishlistCount();
  }
};

document.addEventListener('DOMContentLoaded', () => {
  MainUI.init();
});

window.MainUI = MainUI;
