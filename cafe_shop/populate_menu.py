from django.core.management.base import BaseCommand
from menu.models import Category, SubCategory, MenuItem, Tag

class Command(BaseCommand):
    help = 'Populate the menu with test data'

    def handle(self, *args, **options):
        # Очистка существующих данных (опционально)
        MenuItem.objects.all().delete()
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        Tag.objects.all().delete()

        # Создание категорий
        main_dishes = Category.objects.create(name="Основные блюда", description="Горячие блюда")
        desserts = Category.objects.create(name="Десерты", description="Сладости")

        # Создание подкатегорий
        pizza = SubCategory.objects.create(category=main_dishes, name="Пицца")
        pasta = SubCategory.objects.create(category=main_dishes, name="Паста")
        cakes = SubCategory.objects.create(category=desserts, name="Торты")

        # Создание тегов
        vegetarian = Tag.objects.create(name="Вегетарианское")
        spicy = Tag.objects.create(name="Острое")

        # Создание пунктов меню
        items = [
            {
                'name': "Пицца Маргарита",
                'description': "Классическая пицца с томатами и сыром",
                'price': 500.00,
                'category': main_dishes,
                'subcategory': pizza,
                'tags': [vegetarian],
                'is_available': True
            },
            {
                'name': "Пицца Пепперони",
                'description': "Пицца с острой пепперони и сыром",
                'price': 600.00,
                'category': main_dishes,
                'subcategory': pizza,
                'tags': [spicy],
                'is_available': True
            },
            {
                'name': "Спагетти Карбонара",
                'description': "Кремовый соус с беконом и пармезаном",
                'price': 450.00,
                'category': main_dishes,
                'subcategory': pasta,
                'tags': [],
                'is_available': True
            },
            {
                'name': "Шоколадный торт",
                'description': "Нежный торт с шоколадной глазурью",
                'price': 300.00,
                'category': desserts,
                'subcategory': cakes,
                'tags': [],
                'is_available': True
            }
        ]

        for item_data in items:
            item = MenuItem.objects.create(
                name=item_data['name'],
                description=item_data['description'],
                price=item_data['price'],
                category=item_data['category'],
                subcategory=item_data['subcategory'],
                is_available=item_data['is_available']
            )
            item.tags.set(item_data['tags'])

        self.stdout.write(self.style.SUCCESS(f'Successfully populated menu with {len(items)} items'))