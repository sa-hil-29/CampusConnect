# job/admin.py
from django.contrib import admin
from .models import Job, Branch


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("code", "name")


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company_name", "min_cgpa", "deadline", "status")
    list_filter = ("status", "eligible_branches__code")
    filter_horizontal = ("eligible_branches",)
