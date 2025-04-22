from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import MenuItem, Category, SubCategory, Tag

class MenuListView(ListView):
    model = MenuItem
    template_name = 'menu/menu_list.html'
    context_object_name = 'menu_items'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_available=True)
        
        search_query = self.request.GET.get('search')
        category_slug = self.request.GET.get('category')
        
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(tags__name__icontains=search_query)
            ).distinct()
        
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class MenuItemDetailView(DetailView):
    model = MenuItem
    template_name = 'menu/menu_item_detail.html'
    context_object_name = 'menu_item'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_items'] = MenuItem.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:3]
        return context