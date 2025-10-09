from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ApplicationForm
from .models import Application
from profiles.models import Student
from jobs.models import Job


@login_required
def apply_job(request, job_id):
    if request.user.role != "student":
        messages.error(request, "Access denied. Students only.")
        return redirect("job_list")

    job = get_object_or_404(Job, id=job_id, status="open")
    student = get_object_or_404(Student, user=request.user)

    # Simple eligibility check (enhance with parsing library like regex for criteria)
    if job.eligibility_criteria:
        criteria = job.eligibility_criteria.lower()
        if "cgpa >" in criteria and student.cgpa <= float(
            criteria.split(">")[1].split()[0]
        ):
            messages.error(request, "You do not meet the eligibility criteria (CGPA).")
            return redirect("job_list")
        # Add branch check: if 'branch: cs' in criteria and student.branch.lower() != 'cs': ...

    application, created = Application.objects.get_or_create(student=student, job=job)
    if created:
        messages.success(request, f'Application submitted for "{job.title}"!')
        # Optional: Send notification
        send_mail(
            "Application Submitted",
            f"Your application for {job.title} at {job.company_name} has been submitted.",
            settings.DEFAULT_FROM_EMAIL,
            [request.user.email],
            fail_silently=True,
        )
    else:
        messages.info(request, "Application already exists.")
    return redirect("job_list")


@login_required
@user_passes_test(lambda u: u.role == "admin")
def update_application(request, app_id):
    app = get_object_or_404(Application, id=app_id)
    if request.method == "POST":
        form = ApplicationForm(request.POST, instance=app)
        if form.is_valid():
            old_status = app.status
            form.save()
            new_status = app.status
            messages.success(
                request,
                f"Application status updated from {old_status} to {new_status}.",
            )
            # Send notification if status changed
            if new_status != old_status:
                send_mail(
                    "Application Status Update",
                    f"Your application for {app.job.title} is now {new_status}.",
                    settings.DEFAULT_FROM_EMAIL,
                    [app.student.user.email],
                    fail_silently=True,
                )
            return redirect("dashboard_applications")
    else:
        form = ApplicationForm(instance=app)
    return render(
        request, "applications/update.html", {"form": form, "application": app}
    )
