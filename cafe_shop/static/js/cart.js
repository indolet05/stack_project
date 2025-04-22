document.addEventListener('DOMContentLoaded', function() {
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    
    addToCartButtons.forEach(button => {
        button.addEventListener('click', async function(event) {
            event.preventDefault();
            
            const itemId = this.dataset.itemId;
            const itemName = this.dataset.itemName || 'Товар';
            const originalText = this.innerHTML;
            
            this.innerHTML = `
                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                Добавляем...
            `;
            this.disabled = true;

            try {
                const response = await fetch(this.href, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'X-Requested-With': 'XMLHttpRequest',
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        quantity: 1
                    })
                });

                const data = await response.json();

                if (response.ok && data.success) {
                    updateCartCounter(data.cart_items_count);
                    
                    showToast(`${itemName} добавлен в корзину`, 'success');
                    
                    this.innerHTML = '<i class="bi bi-check-circle"></i> Добавлено';
                    setTimeout(() => {
                        this.innerHTML = originalText;
                        this.disabled = false;
                    }, 2000);
                } else {
                    throw new Error(data.message || 'Ошибка сервера');
                }
            } catch (error) {
                console.error('Ошибка:', error);
                showToast(error.message, 'error');
                this.innerHTML = originalText;
                this.disabled = false;
            }
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function updateCartCounter(count) {
        const counterElements = document.querySelectorAll('.cart-counter');
        counterElements.forEach(element => {
            element.textContent = count;
            element.classList.add('animate-bounce');
            setTimeout(() => {
                element.classList.remove('animate-bounce');
            }, 1000);
        });
    }

    function showToast(message, type = 'success') {
        const toastContainer = document.getElementById('toast-container') || createToastContainer();
        const toast = document.createElement('div');
        
        toast.className = `toast show align-items-center text-white bg-${type}`;
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        toastContainer.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
        }, 5000);
    }
    function createToastContainer() {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '1100';
        document.body.appendChild(container);
        return container;
    }

    function initCart() {
        const cartCounter = document.querySelector('.cart-counter');
        if (cartCounter) {
            fetch('/api/cart/count/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.count !== undefined) {
                    cartCounter.textContent = data.count;
                }
            })
            .catch(console.error);
        }
    }

    initCart();
});