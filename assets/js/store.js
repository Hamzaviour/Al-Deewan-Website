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

  // Init
  init() {
    this.updateCartCount();
    this.updateWishlistCount();
  }
};

document.addEventListener('DOMContentLoaded', () => {
  Store.init();
});

window.Store = Store;
