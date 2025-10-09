from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),  # Default dashboard index
    path("applications/", views.dashboard_applications, name="dashboard_applications"),
    path("analytics/", views.analytics, name="analytics"),
]
