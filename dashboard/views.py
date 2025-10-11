from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Q
from django.http import JsonResponse
import json
from applications.models import Application
from jobs.models import Job
from profiles.models import Student


def is_admin(user):
    return user.is_authenticated and user.role == "admin"


@login_required
@user_passes_test(is_admin)
def dashboard(request):
    total_applications = Application.objects.count()
    open_jobs = Job.objects.filter(status="open").count()
    selected_applications = Application.objects.filter(status="selected").count()
    total_students = Student.objects.count()

    context = {
        "total_applications": total_applications,
        "open_jobs": open_jobs,
        "selected_applications": selected_applications,
        "total_students": total_students,
    }
    return render(request, "dashboard/index.html", context)


@login_required
@user_passes_test(is_admin)
def dashboard_applications(request):
    applications = Application.objects.select_related("student__user", "job").order_by(
        "-application_date"
    )
    return render(
        request, "dashboard/applications.html", {"applications": applications}
    )


@login_required
@user_passes_test(is_admin)
def analytics(request):
    placement_data = (
        Student.objects.values("branch")
        .annotate(
            selected_count=Count(
                "applications", filter=Q(applications__status="selected")
            )
        )
        .order_by("-selected_count")
    )

    labels = [item["branch"] for item in placement_data]
    data = [item["selected_count"] for item in placement_data]

    # Ensure valid JSON string (escape properly)
    chart_data = json.dumps(
        {
            "labels": labels,
            "data": data,
        }
    )

    return render(request, "dashboard/analytics.html", {"chart_data": chart_data})
