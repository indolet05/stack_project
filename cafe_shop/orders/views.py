from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView  # Добавляем DetailView
from django.contrib import messages
from .models import Order
from menu.models import MenuItem
from .forms import CartAddItemForm

@login_required
def create_order(request):
    if request.method == 'POST':
        order = Order.objects.create(user=request.user)
        return redirect('orders:order_list')
    return render(request, 'orders/create_order.html')

class OrderListView(ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    
    cart = request.session.get('cart', {})
    cart_item = cart.get(str(item_id), {'quantity': 0})
    cart_item['quantity'] += 1
    cart[str(item_id)] = cart_item
    request.session['cart'] = cart
    
    messages.success(request, f"{item.name} добавлен в корзину")
    return redirect('menu:menu_list')

@login_required
def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    
    for item_id, cart_item in cart.items():
        try:
            menu_item = MenuItem.objects.get(id=int(item_id))
            subtotal = menu_item.price * cart_item['quantity']
            cart_items.append({
                'menu_item': menu_item,
                'quantity': cart_item['quantity'],
                'subtotal': subtotal
            })
            total += subtotal
        except MenuItem.DoesNotExist:
            del cart[item_id]
            request.session['cart'] = cart
    
    return render(request, 'orders/cart_detail.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    item_id_str = str(item_id)
    if item_id_str in cart:
        item_name = MenuItem.objects.get(id=item_id).name
        del cart[item_id_str]
        request.session['cart'] = cart
        messages.success(request, f"{item_name} удалён из корзины")
    else:
        messages.error(request, "Товар не найден в корзине")
    return redirect('orders:cart_detail')

@login_required
def update_cart(request, item_id):
    cart = request.session.get('cart', {})
    item_id_str = str(item_id)
    form = CartAddItemForm(request.POST)
    if form.is_valid() and item_id_str in cart:
        quantity = form.cleaned_data['quantity']
        item_name = MenuItem.objects.get(id=item_id).name
        if quantity > 0:
            cart[item_id_str]['quantity'] = quantity
            messages.success(request, f"Количество для {item_name} обновлено")
        else:
            del cart[item_id_str]
            messages.success(request, f"{item_name} удалён из корзины")
        request.session['cart'] = cart
    else:
        messages.error(request, "Ошибка обновления корзины")
    return redirect('orders:cart_detail')

class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)