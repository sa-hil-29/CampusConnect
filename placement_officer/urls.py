from django.urls import path
from . import views

app_name = "placement_officer"

urlpatterns = [
    path("", views.officer_dashboard, name="dashboard"),
    path("post-job/", views.post_job, name="post_job"),
    path(
        "update/<int:app_id>/<str:new_status>/",
        views.update_status,
        name="update_status",
    ),
    path("report/", views.generate_report, name="generate_report"),
    path("resume/<int:app_id>/", views.view_resume, name="view_resume"),
    path("edit/<int:job_id>/", views.edit_job, name="edit_job"),
    path("delete/<int:job_id>/", views.delete_job, name="delete_job"),
]
