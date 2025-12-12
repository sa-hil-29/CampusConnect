# student/views.py
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import StudentProfileForm
from .models import Student
from job.models import Job
from application.models import Application
from django.contrib import messages


# student/views.py
@login_required
def dashboard(request):
    if request.user.role != "student":
        return redirect("home")

    try:
        student = request.user.student_profile
    except:
        return redirect("student:profile")
    open_jobs = Job.objects.filter(status="OPEN", deadline__gte=date.today())
    eligible_jobs = [
        job
        for job in open_jobs
        if job.validate_eligibility(student.cgpa, student.branch.code)
    ]

    context = {"student": student, "jobs": eligible_jobs}
    return render(request, "student/dashboard.html", context=context)


@login_required
def profile(request):
    if request.user.role != "student":
        return redirect("home")

    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        student = None

    if request.method == "POST":
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            student.user = request.user
            student.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("student:dashboard")
    else:
        form = StudentProfileForm(instance=student)

    return render(request, "student/profile.html", {"form": form})


@login_required
def job_detail(request, job_id):
    if request.user.role != "student":
        return redirect("home")

    job = get_object_or_404(Job, id=job_id, status="OPEN")
    student = request.user.student_profile

    already_applied = Application.objects.filter(student=student, job=job).exists()
    eligible = job.validate_eligibility(student.cgpa, student.branch.code)

    context = {
        "job": job,
        "already_applied": already_applied,
        "eligible": eligible,
    }
    return render(request, "student/job_detail.html", context)
