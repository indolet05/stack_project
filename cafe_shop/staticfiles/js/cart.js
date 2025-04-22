document.addEventListener('DOMContentLoaded', () => {
    const orderButtons = document.querySelectorAll('.order-btn');

    orderButtons.forEach(button => {
        button.addEventListener('click', () => {
            const itemId = button.getAttribute('data-item-id');
            alert(`Добавлено в корзину: ID ${itemId}`);
        });
    });
});