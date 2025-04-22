from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from menu.models import MenuItem, Category
from .models import Order, OrderItem

class OrdersTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        cls.category = Category.objects.create(name="Напитки")
        cls.menu_item = MenuItem.objects.create(
            name="Капучино",
            price=200.00,
            category=cls.category,
            is_available=True
        )
        cls.order = Order.objects.create(user=cls.user)
        cls.order_item = OrderItem.objects.create(
            order=cls.order,
            menu_item=cls.menu_item,
            quantity=2,
            price_at_order=200.00
        )

    def setUp(self):
        self.client = Client()
        self.client.login(username='testuser', password='testpass')

    def test_order_str(self):
        self.assertEqual(str(self.order), f"Заказ #{self.order.id} - testuser")

    def test_order_item_str(self):
        expected = f"Капучино x2 (Заказ #{self.order.id})"
        self.assertEqual(str(self.order_item), expected)

    def test_order_item_subtotal(self):
        self.assertEqual(self.order_item.get_subtotal(), 400.00)

    def test_order_total_calculation(self):
        self.assertEqual(self.order.total_price, 400.00)

    def test_add_to_cart_view(self):
        response = self.client.post(
            reverse('orders:add_to_cart', args=[self.menu_item.id]),
            {'quantity': 1}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session['cart'][str(self.menu_item.id)], 1)

    def test_order_list_view(self):
        response = self.client.get(reverse('orders:order_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"Заказ #{self.order.id}")

    def test_order_detail_view(self):
        response = self.client.get(
            reverse('orders:order_detail', args=[self.order.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Капучино")