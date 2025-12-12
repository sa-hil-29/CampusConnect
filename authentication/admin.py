from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import User

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "role", "is_active", "date_joined")
    list_filter = ("role", "is_active")
    search_fields = ("email", "name")
    readonly_fields = ("date_joined",)
    fieldsets = (
        ("Personal Info", {"fields": ("email", "name", "role")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important dates", {"fields": ("date_joined",)}),
    )
