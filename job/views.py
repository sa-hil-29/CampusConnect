from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Job
from .forms import JobForm


def officer_required(u):
    return u.is_placement_officer


@login_required
@user_passes_test(officer_required)
def dashboard(request):
    if request.user.role != "admin":
        return redirect("home")
    jobs = Job.objects.all()
    return render(request, "job/officer_dashboard.html", {"jobs": jobs})


@login_required
@user_passes_test(officer_required)
def post_job(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            form.save_m2m()
            messages.success(request, "Job posted!")
            return redirect("job:officer_dashboard")
    else:
        form = JobForm()
    return render(request, "job/post_job.html", {"form": form})


@login_required
def edit_job(request, job_id):
    if not request.user.is_placement_officer:
        return redirect("home")

    job = get_object_or_404(Job, id=job_id, posted_by=request.user)
    if job.status == "CLOSED":
        messages.error(request, "Cannot edit a closed job.")
        return redirect("placement_officer:dashboard")

    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated successfully!")
            return redirect("placement_officer:dashboard")
    else:
        form = JobForm(instance=job)
    return render(
        request, "placement_officer/edit_job.html", {"form": form, "job": job}
    )
