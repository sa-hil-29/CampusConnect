from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .forms import JobForm
from .models import Job


def is_admin(user):
    return user.is_authenticated and user.role == "admin"


@login_required
@user_passes_test(is_admin)
def job_create(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save()
            messages.success(request, f'Job "{job.title}" created successfully!')
            return redirect("job_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = JobForm()
    return render(request, "jobs/create.html", {"form": form})


def job_list(request):
    jobs = Job.objects.filter(
        status="open", deadline__gte=timezone.now().date()
    ).order_by("-created_at")
    return render(request, "jobs/list.html", {"jobs": jobs})


@login_required
@user_passes_test(is_admin)
def job_edit(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, f'Job "{job.title}" updated!')
            return redirect("job_list")
    else:
        form = JobForm(instance=job)
    return render(request, "jobs/edit.html", {"form": form, "job": job})
