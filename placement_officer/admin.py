# placement_officer/admin.py
from django.contrib import admin
from .models import OfficerDashboard


@admin.register(OfficerDashboard)
class OfficerDashboardAdmin(admin.ModelAdmin):
    list_display = (
        "officer",
        "total_jobs_posted",
        "total_applications",
        "total_selections",
    )
    list_filter = ("officer__email",)
    search_fields = ("officer__email", "officer__name")
    readonly_fields = ("officer",)
