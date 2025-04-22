from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from cafe_shop import views

handler404 = 'cafe_shop.views.custom_404'
handler500 = 'cafe_shop.views.custom_500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('menu/', include('menu.urls')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('users/', include('users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)