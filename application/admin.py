from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("student", "job", "status", "application_date")
    list_filter = ("status", "application_date", "job__company_name")
    search_fields = ("student__user__email", "job__title")
    readonly_fields = ("application_date",)
    fieldsets = (
        ("Application Info", {"fields": ("student", "job", "status")}),
        ("Date", {"fields": ("application_date",)}),
    )
