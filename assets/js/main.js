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
    this.initCompareUI();
    this.initMobileNav();
    this.initWhatsAppFloat();
    this.renderHeaderCartWishlist();
    if (window.Store && typeof window.Store.applySiteSettings === 'function') {
      window.Store.applySiteSettings();
    }
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
            <li class="mobile-nav-item has-submenu">
              <div class="mobile-nav-header">
                <a href="collections.html?category=Unstitched">UNSTITCHED</a>
                <button class="mobile-nav-toggle" aria-label="Toggle Submenu">+</button>
              </div>
              <ul class="mobile-submenu">
                <li class="mobile-nav-item has-submenu">
                  <div class="mobile-nav-header">
                    <a href="collections.html?category=Unstitched&type=2PC">2PC</a>
                    <button class="mobile-nav-toggle" aria-label="Toggle Submenu">+</button>
                  </div>
                  <ul class="mobile-submenu">
                    <li><a href="collections.html?category=Unstitched&type=2PC&season=Winter">Winter</a></li>
                    <li><a href="collections.html?category=Unstitched&type=2PC&season=Summer">Summer</a></li>
                  </ul>
                </li>
                <li class="mobile-nav-item has-submenu">
                  <div class="mobile-nav-header">
                    <a href="collections.html?category=Unstitched&type=3PC">3PC</a>
                    <button class="mobile-nav-toggle" aria-label="Toggle Submenu">+</button>
                  </div>
                  <ul class="mobile-submenu">
                    <li><a href="collections.html?category=Unstitched&type=3PC&season=Winter">Winter</a></li>
                    <li><a href="collections.html?category=Unstitched&type=3PC&season=Summer">Summer</a></li>
                  </ul>
                </li>
              </ul>
            </li>
            <li class="mobile-nav-item has-submenu">
              <div class="mobile-nav-header">
                <a href="collections.html?category=Ready+to+Wear">READY TO WEAR</a>
                <button class="mobile-nav-toggle" aria-label="Toggle Submenu">+</button>
              </div>
              <ul class="mobile-submenu">
                <li><a href="collections.html?category=Ready+to+Wear&type=2PC">2PC</a></li>
                <li><a href="collections.html?category=Ready+to+Wear&type=3PC">3PC</a></li>
              </ul>
            </li>
            <li class="mobile-nav-item has-submenu" id="mobile-nav-kids">
              <div class="mobile-nav-header">
                <a href="collections.html?category=Kids">KIDS</a>
                <button class="mobile-nav-toggle" aria-label="Toggle Submenu">+</button>
              </div>
              <ul class="mobile-submenu">
                <li><a href="collections.html?category=Kids&type=Girls+Eastern">Girls Eastern</a></li>
                <li><a href="collections.html?category=Kids&type=Boys+Kurta">Boys Kurta</a></li>
                <li><a href="collections.html?category=Kids">All Kids Collection</a></li>
              </ul>
            </li>
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
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <span style="font-size:13px; font-weight:600; color:#555;">Subtotal:</span>
            <span style="font-size:15px; font-weight:800; color:#111;" id="cart-drawer-subtotal">Rs.0.00</span>
          </div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <span style="font-size:13px; font-weight:600; color:#555;">Delivery Charges:</span>
            <span style="font-size:12.5px; font-weight:700; color:#5e3585;" id="cart-drawer-shipping">According to parcel weight</span>
          </div>
          <button class="btn-whatsapp" id="cart-drawer-whatsapp-btn" onclick="Store.checkoutViaWhatsApp()" style="width:100%; padding:14px 10px; font-weight:800; margin-bottom:8px; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; gap:4px; cursor:pointer;">
            <div style="display:flex; align-items:center; justify-content:center; gap:8px; font-size:14px; letter-spacing:0.02em;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981z"/></svg>
              <span>ORDER ON WHATSAPP</span>
            </div>
            <div style="font-size:13px; font-weight:700;">(<span id="cart-drawer-btn-total">Rs.0.00</span>)</div>
          </button>
          <a href="cart.html" class="btn-black" style="display:flex; justify-content:center; align-items:center; padding:12px; font-size:12px;">VIEW SHOPPING BAG</a>
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

    // 6. Floating Compare Bar (Bottom)
    if (!document.getElementById('compare-floating-bar')) {
      const compareBar = document.createElement('div');
      compareBar.id = 'compare-floating-bar';
      compareBar.className = 'compare-floating-bar';
      compareBar.innerHTML = `
        <div class="compare-bar-inner">
          <div class="compare-bar-left">
            <div class="compare-bar-title">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 3 21 3 21 8"></polyline><line x1="4" y1="14" x2="21" y2="3"></line><polyline points="8 21 3 21 3 16"></polyline><line x1="20" y1="10" x2="3" y2="21"></line></svg>
              <span>Compare</span>
              <span class="compare-bar-count" id="compare-bar-count">0/4</span>
            </div>
            <div class="compare-bar-slots" id="compare-bar-slots"></div>
          </div>
          <div class="compare-bar-actions">
            <button type="button" class="btn-compare-now" id="compare-now-btn" onclick="MainUI.openCompareModal()">
              <span>COMPARE NOW</span>
              <span class="compare-action-badge" id="compare-action-badge">0</span>
            </button>
            <button type="button" class="btn-compare-clear" onclick="Store.clearCompare()">Clear All</button>
            <button type="button" class="compare-bar-close" onclick="MainUI.toggleCompareBar(false)" aria-label="Minimize Bar">&times;</button>
          </div>
        </div>
      `;
      document.body.appendChild(compareBar);
    }

    // 7. Full Product Comparison Modal
    if (!document.getElementById('compare-modal')) {
      const compareModal = document.createElement('div');
      compareModal.id = 'compare-modal';
      compareModal.className = 'compare-modal';
      compareModal.innerHTML = `
        <div class="compare-modal-dialog">
          <div class="compare-modal-header">
            <div class="compare-modal-title">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 3 21 3 21 8"></polyline><line x1="4" y1="14" x2="21" y2="3"></line><polyline points="8 21 3 21 3 16"></polyline><line x1="20" y1="10" x2="3" y2="21"></line></svg>
              <h2>Compare Products</h2>
              <span class="compare-modal-badge" id="compare-modal-count">0 items</span>
            </div>
            <div style="display:flex; align-items:center; gap:12px;">
              <button type="button" class="compare-modal-clear" onclick="Store.clearCompare(); MainUI.closeCompareModal();">Clear All</button>
              <button type="button" class="modal-close" onclick="MainUI.closeCompareModal()" aria-label="Close Comparison">&times;</button>
            </div>
          </div>
          <div class="compare-modal-body" id="compare-modal-content">
            <!-- Dynamic comparison table/cards rendered here -->
          </div>
        </div>
      `;
      document.body.appendChild(compareModal);
    }
  },

  // Hero Main Banner Slider (Smooth Slide-Left Carousel with Touch Swipe Support)
  initHeroSlider() {
    const track = document.getElementById('hero-slider-track');
    const container = document.getElementById('hero-slider-container');
    if (!track) return;

    let slides = track.querySelectorAll('.hero-slide');
    if (!slides.length) return;

    let currentSlide = 0;
    let slideInterval = null;
    let autoplaySpeed = 5000;
    
    if (window.Store && typeof window.Store.getSiteSettings === 'function') {
      const settings = window.Store.getSiteSettings();
      if (settings && settings.heroAutoplaySpeed) {
        autoplaySpeed = parseInt(settings.heroAutoplaySpeed, 10) || 5000;
      }
    }

    const updateSlider = (index, animate = true) => {
      slides = track.querySelectorAll('.hero-slide');
      const total = slides.length;
      if (total === 0) return;

      currentSlide = (index + total) % total;
      
      track.style.transition = animate ? 'transform 0.65s cubic-bezier(0.25, 1, 0.5, 1)' : 'none';
      track.style.transform = `translateX(-${currentSlide * 100}%)`;

      // Update dots
      const dots = document.querySelectorAll('#hero-slider-dots .hero-slider-dot');
      dots.forEach((dot, idx) => {
        dot.classList.toggle('active', idx === currentSlide);
        dot.setAttribute('aria-current', idx === currentSlide ? 'true' : 'false');
      });
    };

    const nextSlide = () => updateSlider(currentSlide + 1);
    const prevSlide = () => updateSlider(currentSlide - 1);

    const startAutoplay = () => {
      stopAutoplay();
      slideInterval = setInterval(nextSlide, autoplaySpeed);
    };

    const stopAutoplay = () => {
      if (slideInterval) {
        clearInterval(slideInterval);
        slideInterval = null;
      }
    };

    // Controls
    const prevBtn = document.getElementById('hero-slider-prev');
    const nextBtn = document.getElementById('hero-slider-next');
    if (prevBtn) {
      prevBtn.onclick = (e) => {
        e.preventDefault();
        prevSlide();
        startAutoplay();
      };
    }
    if (nextBtn) {
      nextBtn.onclick = (e) => {
        e.preventDefault();
        nextSlide();
        startAutoplay();
      };
    }

    // Dots delegation
    const dotsContainer = document.getElementById('hero-slider-dots');
    if (dotsContainer) {
      dotsContainer.onclick = (e) => {
        const dot = e.target.closest('.hero-slider-dot');
        if (dot && dot.dataset.index !== undefined) {
          const idx = parseInt(dot.dataset.index, 10);
          updateSlider(idx);
          startAutoplay();
        }
      };
    }

    // Touch & Swipe Support
    let touchStartX = 0;
    let touchEndX = 0;
    let isTouching = false;

    track.addEventListener('touchstart', (e) => {
      isTouching = true;
      touchStartX = e.touches[0].clientX;
      stopAutoplay();
    }, { passive: true });

    track.addEventListener('touchmove', (e) => {
      if (!isTouching) return;
      touchEndX = e.touches[0].clientX;
    }, { passive: true });

    track.addEventListener('touchend', () => {
      if (!isTouching) return;
      isTouching = false;
      const swipeDistance = touchStartX - touchEndX;
      if (Math.abs(swipeDistance) > 40) {
        if (swipeDistance > 0) {
          nextSlide(); // Swiped left -> next
        } else {
          prevSlide(); // Swiped right -> prev
        }
      }
      startAutoplay();
    });

    // Pause on Hover
    if (container) {
      container.addEventListener('mouseenter', stopAutoplay);
      container.addEventListener('mouseleave', startAutoplay);
    }

      // Expose dynamic render helper
    window.MainUI_renderHeroSlider = (slidesData, speedMs) => {
      if (!slidesData || !slidesData.length) return;
      if (speedMs) autoplaySpeed = speedMs;
      
      track.innerHTML = slidesData.map((s, idx) => {
        const bannerImg = s.image || s.mobileImage || 'assets/images/banners/hero_slide_3.jpg';
        return `
        <div class="hero-slide" data-index="${idx}">
          <a href="${s.link || '#'}" class="hero-slide-link" aria-label="${s.title || 'Slide ' + (idx + 1)}">
            <img src="${bannerImg}" alt="${s.title || 'Hero Banner Slide ' + (idx + 1)}" class="hero-slide-img" loading="${idx === 0 ? 'eager' : 'lazy'}" onerror="this.onerror=null; this.src='assets/images/banners/hero_slide_3.jpg';" />
          </a>
        </div>
      `;
      }).join('');

      if (dotsContainer) {
        dotsContainer.innerHTML = slidesData.map((_, idx) => `
          <button type="button" class="hero-slider-dot ${idx === 0 ? 'active' : ''}" data-index="${idx}" aria-label="Slide ${idx + 1}"></button>
        `).join('');
      }

      updateSlider(0, false);
      startAutoplay();
    };

    // Auto-render from active settings if available
    if (window.Store && typeof window.Store.getSiteSettings === 'function') {
      const activeSettings = window.Store.getSiteSettings();
      if (activeSettings && activeSettings.heroSlides && activeSettings.heroSlides.length > 0) {
        window.MainUI_renderHeroSlider(activeSettings.heroSlides, activeSettings.heroAutoplaySpeed);
      } else {
        updateSlider(0, false);
        startAutoplay();
      }
    } else {
      updateSlider(0, false);
      startAutoplay();
    }

    // Real-time listener for settings updates
    window.addEventListener('settings:updated', (e) => {
      if (e.detail && Array.isArray(e.detail.heroSlides) && e.detail.heroSlides.length > 0) {
        window.MainUI_renderHeroSlider(e.detail.heroSlides, e.detail.heroAutoplaySpeed);
      }
    });
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
    document.querySelectorAll('.slide-drawer, .search-modal, .quick-view-modal, .compare-modal').forEach(el => {
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

    
    const shippingProgressEl = document.getElementById('cart-shipping-progress');
    if (shippingProgressEl) {
      shippingProgressEl.innerHTML = '';
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
      if (shippingProgressEl) shippingProgressEl.innerHTML = '';
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
    const shippingElem = document.getElementById('cart-drawer-shipping');
    if (shippingElem) {
      shippingElem.textContent = 'According to parcel weight';
    }
    const btnTotalElem = document.getElementById('cart-drawer-btn-total');
    if (btnTotalElem) {
      btnTotalElem.textContent = Store.formatMoney(subtotal);
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

      // Submenu accordion toggle
      const subToggle = e.target.closest('.mobile-nav-toggle');
      if (subToggle) {
        e.preventDefault();
        e.stopPropagation();
        const parentItem = subToggle.closest('.mobile-nav-item');
        if (parentItem) {
          parentItem.classList.toggle('open');
          subToggle.textContent = parentItem.classList.contains('open') ? '−' : '+';
        }
      }
    });
  },

  // WhatsApp Order Generator
  orderOnWhatsApp(title, sku, price, handle, qty = 1) {
    const phone = '923334275944';
    const currentUrl = window.location.origin + '/product.html?handle=' + handle;
    const msg = `*Hello Al-Deewan Brand,*\n\n` +
      `I want to order this product:\n` +
      `• *Product:* ${title}\n` +
      (sku ? `• *SKU:* ${sku}\n` : '') +
      `• *Price:* ${price}\n` +
      `• *Quantity:* ${qty}\n` +
      `• *URL:* ${currentUrl}\n\n` +
      `Please confirm my order and share payment/dispatch details. Thank you!`;
    const url = `https://api.whatsapp.com/send?phone=${phone}&text=${encodeURIComponent(msg)}`;
    window.open(url, '_blank');
  },

  // WhatsApp Floating Button
  initWhatsAppFloat() {
    let btn = document.querySelector('.whatsapp-float, .whatsapp-floating-btn');
    if (!btn) {
      btn = document.createElement('a');
      btn.className = 'whatsapp-float';
      btn.href = 'https://api.whatsapp.com/send?phone=923334275944&text=Hello%20Al-Deewan%20Brand%2C%20I%20have%20an%20inquiry%20regarding%20an%20order.';
      btn.target = '_blank';
      btn.setAttribute('aria-label', 'Chat with us on WhatsApp');
      btn.innerHTML = `
        <img src="assets/images/whatsapp_floating_icon.png" alt="WhatsApp Chat" width="62" height="62" loading="eager" />
      `;
      document.body.appendChild(btn);
    }
  },

  // Compare System UI
  initCompareUI() {
    window.addEventListener('compare:updated', () => {
      this.renderCompareBar();
      this.updateCompareButtonsDOM();
      const modal = document.getElementById('compare-modal');
      if (modal && modal.classList.contains('active')) {
        this.renderCompareModalContent();
      }
    });
    this.renderCompareBar();
  },

  updateCompareButtonsDOM() {
    const compareList = Store.getCompare();
    document.querySelectorAll('.compare-btn').forEach(btn => {
      const id = parseInt(btn.dataset.id);
      const isComp = compareList.some(item => item.id === id);
      if (isComp) {
        btn.classList.add('active');
        btn.setAttribute('data-tooltip', 'In Compare');
      } else {
        btn.classList.remove('active');
        btn.setAttribute('data-tooltip', 'Compare');
      }
    });
  },

  renderCompareBar() {
    const bar = document.getElementById('compare-floating-bar');
    if (!bar) return;
    const compare = Store.getCompare();
    const count = compare.length;

    if (count === 0) {
      bar.classList.remove('active');
      return;
    }

    bar.classList.add('active');
    const countBadge = document.getElementById('compare-bar-count');
    const actionBadge = document.getElementById('compare-action-badge');
    if (countBadge) countBadge.textContent = `${count}/4`;
    if (actionBadge) actionBadge.textContent = count;

    const slotsContainer = document.getElementById('compare-bar-slots');
    if (slotsContainer) {
      let slotsHTML = '';
      for (let i = 0; i < 4; i++) {
        if (i < count) {
          const item = compare[i];
          slotsHTML += `
            <div class="compare-slot filled" title="${item.title}">
              <img src="${item.image}" alt="${item.title}" />
              <button type="button" class="compare-slot-remove" onclick="event.stopPropagation(); Store.removeFromCompare(${item.id});" aria-label="Remove ${item.title}">&times;</button>
            </div>
          `;
        } else {
          slotsHTML += `
            <div class="compare-slot empty">
              <span>+</span>
            </div>
          `;
        }
      }
      slotsContainer.innerHTML = slotsHTML;
    }

    const nowBtn = document.getElementById('compare-now-btn');
    if (nowBtn) {
      if (count >= 2) {
        nowBtn.classList.add('pulse-ready');
      } else {
        nowBtn.classList.remove('pulse-ready');
      }
    }
  },

  toggleCompareBar(show) {
    const bar = document.getElementById('compare-floating-bar');
    if (bar) {
      if (show) bar.classList.add('active');
      else bar.classList.remove('active');
    }
  },

  openCompareModal() {
    this.closeAllDrawers();
    const modal = document.getElementById('compare-modal');
    const overlay = document.querySelector('.drawer-overlay');
    if (!modal) return;
    
    this.renderCompareModalContent();
    modal.classList.add('active');
    if (overlay) overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  },

  closeCompareModal() {
    const modal = document.getElementById('compare-modal');
    const overlay = document.querySelector('.drawer-overlay');
    if (modal) modal.classList.remove('active');
    if (overlay) overlay.classList.remove('active');
    document.body.style.overflow = '';
  },

  renderCompareModalContent() {
    const content = document.getElementById('compare-modal-content');
    const countEl = document.getElementById('compare-modal-count');
    if (!content) return;
    
    const compare = Store.getCompare();
    if (countEl) countEl.textContent = `${compare.length} items`;

    if (compare.length === 0) {
      content.innerHTML = `
        <div style="text-align:center; padding: 60px 20px;">
          <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#ccc" stroke-width="1.5" style="margin:0 auto 16px;"><polyline points="16 3 21 3 21 8"></polyline><line x1="4" y1="14" x2="21" y2="3"></line><polyline points="8 21 3 21 3 16"></polyline><line x1="20" y1="10" x2="3" y2="21"></line></svg>
          <h3 style="font-size: 18px; font-weight: 800; margin-bottom: 8px;">No Products in Comparison</h3>
          <p style="font-size: 13.5px; color: #888; margin-bottom: 24px;">Hover over any product and click the compare icon to add items.</p>
          <button class="btn-primary" onclick="MainUI.closeCompareModal()" style="display:inline-block; width:auto; padding:10px 28px;">Browse Products</button>
        </div>
      `;
      return;
    }

    // Build side-by-side comparison table
    content.innerHTML = `
      <div class="compare-table-wrapper">
        <table class="compare-table">
          <thead>
            <tr>
              <th class="compare-label-cell">Product Details</th>
              ${compare.map(item => `
                <th class="compare-col-head">
                  <div class="compare-item-card">
                    <button type="button" class="compare-item-remove-btn" onclick="Store.removeFromCompare(${item.id})" title="Remove item">&times;</button>
                    <a href="product.html?handle=${item.handle}" class="compare-item-img-link">
                      <img src="${item.image}" alt="${item.title}" class="compare-item-img" onerror="if(this.src!=='${item.image||''}')this.src='${item.image||''}'" />
                    </a>
                    <div class="compare-item-vendor">${item.vendor || 'Al-Deewan Brand'}</div>
                    <a href="product.html?handle=${item.handle}" class="compare-item-title">${item.title}</a>
                    <div class="compare-item-sku">SKU: ${item.sku || 'N/A'}</div>
                  </div>
                </th>
              `).join('')}
              ${compare.length < 2 ? `
                <th class="compare-col-placeholder">
                  <div class="compare-placeholder-card">
                    <div class="placeholder-icon">+</div>
                    <h4>Add Another Product</h4>
                    <p>Select at least 2 products from any collection to view side-by-side comparison.</p>
                    <button type="button" class="btn-primary" onclick="MainUI.closeCompareModal()" style="width:auto; padding:8px 18px; font-size:11px;">Select Product</button>
                  </div>
                </th>
              ` : ''}
            </tr>
          </thead>
          <tbody>
            <!-- Row: Price -->
            <tr>
              <td class="compare-label-cell">Price & Savings</td>
              ${compare.map(item => `
                <td class="compare-val-cell">
                  <div class="compare-price-wrap">
                    <span class="compare-price-current">${Store.formatMoney(item.price)}</span>
                    ${item.compare_at_price > item.price ? `
                      <span class="compare-price-old">${Store.formatMoney(item.compare_at_price)}</span>
                      <span class="badge-save">SAVE ${Store.formatMoney(item.save_amount)}</span>
                    ` : ''}
                  </div>
                </td>
              `).join('')}
              ${compare.length < 2 ? `<td class="compare-val-cell muted">-</td>` : ''}
            </tr>

            <!-- Row: Brand -->
            <tr>
              <td class="compare-label-cell">Brand / Vendor</td>
              ${compare.map(item => `
                <td class="compare-val-cell">
                  <span class="compare-badge-brand">${item.vendor || 'Al-Deewan'}</span>
                </td>
              `).join('')}
              ${compare.length < 2 ? `<td class="compare-val-cell muted">-</td>` : ''}
            </tr>

            <!-- Row: Suit Type -->
            <tr>
              <td class="compare-label-cell">Suit Type</td>
              ${compare.map(item => `
                <td class="compare-val-cell">
                  <strong>${item.category_type || '3PC Suit'}</strong>
                </td>
              `).join('')}
              ${compare.length < 2 ? `<td class="compare-val-cell muted">-</td>` : ''}
            </tr>

            <!-- Row: Category -->
            <tr>
              <td class="compare-label-cell">Category</td>
              ${compare.map(item => `
                <td class="compare-val-cell">
                  ${item.category || 'Unstitched'}
                </td>
              `).join('')}
              ${compare.length < 2 ? `<td class="compare-val-cell muted">-</td>` : ''}
            </tr>

            <!-- Row: Fabric -->
            <tr>
              <td class="compare-label-cell">Fabric</td>
              ${compare.map(item => `
                <td class="compare-val-cell">
                  ${item.fabric || 'Premium Lawn'}
                </td>
              `).join('')}
              ${compare.length < 2 ? `<td class="compare-val-cell muted">-</td>` : ''}
            </tr>

            <!-- Row: Availability -->
            <tr>
              <td class="compare-label-cell">Availability</td>
              ${compare.map(item => `
                <td class="compare-val-cell">
                  <span class="compare-stock-badge ${item.available ? 'in-stock' : 'out-of-stock'}">
                    ${item.available ? '● In Stock' : '✕ Sold Out'}
                  </span>
                </td>
              `).join('')}
              ${compare.length < 2 ? `<td class="compare-val-cell muted">-</td>` : ''}
            </tr>

            <!-- Row: Actions -->
            <tr class="compare-actions-row">
              <td class="compare-label-cell">Order & Purchase</td>
              ${compare.map(item => `
                <td class="compare-val-cell">
                  <div class="compare-item-actions">
                    <button type="button" class="btn-primary" onclick="Store.addToCart(window.CATALOG_PRODUCTS.find(p=>p.id===${item.id}) || {id:${item.id}, title:'${item.title.replace(/'/g, "\\'")}', price:${item.price}, featured_image:'${item.image}'}, 1); MainUI.closeCompareModal();">
                      Add To Cart
                    </button>
                    <button type="button" class="btn-whatsapp" onclick="MainUI.orderOnWhatsApp('${item.title.replace(/'/g, "\\'")}', '${item.sku}', '${Store.formatMoney(item.price)}', '${item.handle}')" style="padding:10px 14px; font-size:11.5px;">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981z"/></svg>
                      Order on WhatsApp
                    </button>
                    <a href="product.html?handle=${item.handle}" class="btn-black" style="padding:10px 14px; font-size:11.5px;">
                      View Details
                    </a>
                  </div>
                </td>
              `).join('')}
              ${compare.length < 2 ? `<td class="compare-val-cell muted">-</td>` : ''}
            </tr>
          </tbody>
        </table>
      </div>
    `;
  },

  // Toggle Compare
  toggleCompare(id) {
    const product = (window.CATALOG_PRODUCTS || []).find(p => p.id === id);
    if (product) {
      const wasAdded = Store.toggleCompare(product);
      this.updateCompareButtonsDOM();
      this.renderCompareBar();
      
      // If 2 or more products are in compare, popup comparison modal or animate compare bar
      const compareList = Store.getCompare();
      if (wasAdded && compareList.length >= 2) {
        this.openCompareModal();
      }
    }
  },

  // Helper to generate a single Product Card HTML
  createProductCardHTML(p) {
    const isWishlist = Store.isInWishlist(p.id);
    const isCompare = Store.isInCompare ? Store.isInCompare(p.id) : false;
    const imgUrl = p.featured_image || p.image || (p.images && p.images[0]) || '';
    return `
      <div class="product-card" data-id="${p.id}">
        <div class="product-card__media">
          <a href="product.html?handle=${p.handle}">
            <img src="${imgUrl}" alt="${p.title}" loading="lazy" decoding="async" onerror="this.onerror=null; this.src='assets/images/catalog/nishat-3pc-42206126-r-main.jpg';" />
          </a>
          <span class="badge-sale">Sale ${p.discount_percent}%</span>
          ${!p.available ? '<span class="badge-soldout">Sold Out</span>' : ''}
          <div class="product-card__actions action-buttons">
            <!-- Heart Icon: Wishlist -->
            <button type="button" class="card-action-btn action-btn add-to-wishlist ${isWishlist ? 'active' : ''}" data-id="${p.id}" data-tooltip="${isWishlist ? 'In Wishlist' : 'Add to Wishlist'}" onclick="event.preventDefault(); event.stopPropagation(); Store.toggleWishlist(window.CATALOG_PRODUCTS.find(x=>x.id===${p.id}))" aria-label="Add to Wishlist">
              <svg width="17" height="17" viewBox="0 0 24 24" fill="${isWishlist ? '#ff3366' : 'none'}" stroke="${isWishlist ? '#ff3366' : 'currentColor'}" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg>
            </button>
            
            <!-- Eye Icon: Quick View -->
            <button type="button" class="card-action-btn action-btn quick-view-btn" data-id="${p.id}" data-tooltip="Quick View" onclick="event.preventDefault(); event.stopPropagation(); MainUI.openQuickViewModal(window.CATALOG_PRODUCTS.find(x=>x.id===${p.id}))" aria-label="Quick View">
              <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"></circle><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path></svg>
            </button>

            <!-- Compare Icon -->
            <button type="button" class="card-action-btn action-btn compare-btn ${isCompare ? 'active' : ''}" data-id="${p.id}" data-tooltip="${isCompare ? 'In Compare' : 'Compare'}" onclick="event.preventDefault(); event.stopPropagation(); MainUI.toggleCompare(${p.id})" aria-label="Compare">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 3 21 3 21 8"></polyline><line x1="4" y1="14" x2="21" y2="3"></line><polyline points="8 21 3 21 3 16"></polyline><line x1="20" y1="10" x2="3" y2="21"></line></svg>
            </button>

            <!-- Bag Icon: Add to Cart -->
            <button type="button" class="card-action-btn action-btn add-to-cart-btn" data-id="${p.id}" data-tooltip="Add to Cart" onclick="event.preventDefault(); event.stopPropagation(); Store.addToCart(window.CATALOG_PRODUCTS.find(x=>x.id===${p.id}), 1)" aria-label="Add to Cart">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path><line x1="3" y1="6" x2="21" y2="6"></line><path d="M16 10a4 4 0 0 1-8 0"></path></svg>
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
