# application/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from job.models import Job
from .models import Application
from datetime import date


@login_required
def apply(request, job_id):
    if request.user.role != "student":
        messages.error(request, "Only students can apply.")
        return redirect("home")

    job = get_object_or_404(Job, id=job_id, status="OPEN", deadline__gte=date.today())
    student = request.user.student_profile

    if not job.validate_eligibility(student.cgpa, student.branch):
        messages.error(request, "You are not eligible for this job.")
        return redirect("student:job_detail", job_id=job.id)

    if Application.objects.filter(student=student, job=job).exists():
        messages.warning(request, "Already applied.")
        return redirect("student:job_detail", job_id=job.id)

    Application.objects.create(student=student, job=job)
    messages.success(request, f"Applied to {job.title}!")
    return redirect("student:dashboard")
