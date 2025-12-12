from django.urls import path
from . import views

app_name = "analytics"

urlpatterns = [
    path("data/", views.placement_stats, name="data"),
]
