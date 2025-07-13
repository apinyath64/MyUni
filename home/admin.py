from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("username", "email", "is_admin", "is_staff", "is_active")
    list_filter = ("is_admin", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ('username', 'email', 'password')}),
        ('Permissions', {'fields': ("is_admin", "is_staff", "is_active")}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_admin', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Place)
admin.site.register(Post)
admin.site.register(Event)
admin.site.register(EventImage)
admin.site.register(EventMember)