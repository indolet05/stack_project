from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Профили'
    fields = ('phone', 'address', 'birth_date', 'email_confirmed')
    readonly_fields = ('created_at', 'updated_at')

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'is_staff', 'get_phone')

    def get_phone(self, obj):
        return obj.profile.phone if hasattr(obj, 'profile') else None
    get_phone.short_description = 'Телефон'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)