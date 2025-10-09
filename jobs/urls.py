from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.job_create, name="job_create"),
    path("list/", views.job_list, name="job_list"),
    path(
        "edit/<int:job_id>/", views.job_edit, name="job_edit"
    ),  # Dynamic routing for editing a specific job
]
