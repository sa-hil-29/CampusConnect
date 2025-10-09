from django.urls import path
from . import views

urlpatterns = [
    path(
        "apply/<int:job_id>/", views.apply_job, name="apply_job"
    ),  # Dynamic routing for applying to a specific job
    path(
        "update/<int:app_id>/", views.update_application, name="update_application"
    ),  # Dynamic routing for updating a specific application
]
