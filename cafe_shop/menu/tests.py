from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Category, SubCategory, Tag, MenuItem

class MenuModelsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            name="Напитки",
            description="Горячие и холодные напитки"
        )
        cls.subcategory = SubCategory.objects.create(
            category=cls.category,
            name="Кофе"
        )
        cls.tag = Tag.objects.create(name="Горячий")
        cls.menu_item = MenuItem.objects.create(
            name="Эспрессо",
            description="Крепкий черный кофе",
            price=150.00,
            category=cls.category,
            subcategory=cls.subcategory,
            stock=10
        )
        cls.menu_item.tags.add(cls.tag)

    def test_category_str(self):
        self.assertEqual(str(self.category), "Напитки")

    def test_subcategory_str(self):
        self.assertEqual(str(self.subcategory), "Кофе (Напитки)")

    def test_menu_item_str(self):
        self.assertEqual(str(self.menu_item), "Эспрессо")

    def test_menu_item_absolute_url(self):
        url = reverse('menu:menu_item_detail', kwargs={'slug': self.menu_item.slug})
        self.assertEqual(self.menu_item.get_absolute_url(), url)

    def test_menu_item_in_stock(self):
        self.assertTrue(self.menu_item.is_in_stock)
        self.menu_item.stock = 0
        self.assertTrue(self.menu_item.is_in_stock)

class MenuViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="Еда")
        cls.menu_item = MenuItem.objects.create(
            name="Бургер",
            price=250.00,
            category=cls.category,
            is_available=True
        )

    def test_menu_list_view(self):
        response = self.client.get(reverse('menu:menu_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Бургер")
        self.assertTemplateUsed(response, 'menu/menu_list.html')

    def test_menu_item_detail_view(self):
        url = reverse('menu:menu_item_detail', kwargs={'slug': self.menu_item.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Бургер")
        self.assertTemplateUsed(response, 'menu/menu_item_detail.html')

    def test_category_filter(self):
        response = self.client.get(
            reverse('menu:menu_list') + f'?category={self.category.slug}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Бургер")