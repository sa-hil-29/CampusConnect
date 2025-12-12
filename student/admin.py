from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("user", "roll_number", "cgpa", "branch", "resume")
    list_filter = ("branch", "cgpa")
    search_fields = ("user__email", "user__name", "roll_number")
    readonly_fields = ("user",)
    fieldsets = (
        (
            "Student Info",
            {"fields": ("user", "roll_number", "cgpa", "branch", "skills")},
        ),
        ("Resume", {"fields": ("resume",)}),
    )
