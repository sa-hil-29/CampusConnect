# placement_officer/views.py
import io
import os
import matplotlib.pyplot as plt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)
from .forms import JobForm
from job.models import Job
from application.models import Application
from student.models import Student


@login_required
def update_status(request, app_id, new_status):
    if not getattr(request.user, "is_placement_officer", False):
        messages.error(request, "Access denied.")
        return redirect("home")

    app = get_object_or_404(Application, id=app_id)
    new_status = new_status.upper()

    if new_status not in dict(Application.STATUS_CHOICES):
        messages.error(request, "Invalid status.")
        return redirect("placement_officer:dashboard")

    old_status = app.status
    app.status = new_status
    app.save()

    # Send email only once for final status
    if not getattr(app, "email_sent", False) and new_status in ["SELECTED", "REJECTED"]:
        subject = f"Application Status: {new_status}"
        message = (
            f"Dear {app.student.user.get_full_name() or app.student.user.username},\n\n"
            f"Your application for the position of {app.job.title}\n"
            f"at {getattr(app.job, 'company_name', 'the company')} has been updated to:\n\n"
            f"→ {new_status} ←\n\n"
            f"Thank you for applying!\n\n"
            f"Regards,\nPlacement Cell"
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [app.student.user.email],
            fail_silently=False,
        )
        app.email_sent = True  # assuming you have this field
        app.save()

    messages.success(request, f"Status updated to {new_status}")
    return redirect("placement_officer:dashboard")


@login_required
def officer_dashboard(request):
    if not getattr(request.user, "is_placement_officer", False):
        messages.error(request, "Access denied!")
        return redirect("home")

    total_jobs = Job.objects.filter(posted_by=request.user).count()
    total_applications = Application.objects.filter(job__posted_by=request.user).count()
    total_selections = Application.objects.filter(
        job__posted_by=request.user, status="SELECTED"
    ).count()

    selection_rate = (
        round(total_selections / total_applications * 100, 1)
        if total_applications > 0
        else 0
    )

    # Bar chart data
    job_stats = (
        Job.objects.filter(posted_by=request.user)
        .annotate(apps=Count("application"))
        .values("title", "apps")
        .order_by("-apps")[:10]  # Top 10 jobs
    )
    chart_labels = [
        (j["title"][:20] + "..." if len(j["title"]) > 20 else j["title"])
        for j in job_stats
    ]
    chart_data = [j["apps"] for j in job_stats]

    jobs = Job.objects.filter(posted_by=request.user).order_by("-id")
    applications = (
        Application.objects.filter(job__posted_by=request.user)
        .select_related("student__user", "job")
        .order_by("-application_date")
    )

    context = {
        "total_jobs": total_jobs,
        "total_applications": total_applications,
        "total_selections": total_selections,
        "selection_rate": selection_rate,
        "chart_labels": chart_labels,
        "chart_data": chart_data,
        "jobs": jobs,
        "applications": applications,
    }
    return render(request, "placement_officer/dashboard.html", context)


@login_required
def post_job(request):
    if not getattr(request.user, "is_placement_officer", False):
        return redirect("home")

    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            form.save_m2m()
            messages.success(request, "Job posted successfully!")
            return redirect("placement_officer:dashboard")
    else:
        form = JobForm()
    return render(request, "placement_officer/post_job.html", {"form": form})


@login_required
def edit_job(request, job_id):
    if not getattr(request.user, "is_placement_officer", False):
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


@login_required
def delete_job(request, job_id):
    if not getattr(request.user, "is_placement_officer", False):
        return redirect("home")

    job = get_object_or_404(Job, id=job_id, posted_by=request.user)
    if request.method == "POST":
        job.delete()
        messages.success(request, "Job deleted permanently.")
        return redirect("placement_officer:dashboard")
    return render(request, "placement_officer/delete_job.html", {"job": job})


@login_required
def generate_report(request):
    if not getattr(request.user, "is_placement_officer", False):
        messages.error(request, "Access denied.")
        return redirect("home")

    total_jobs = Job.objects.count()
    total_applications = Application.objects.count()
    total_students = Student.objects.count()

    selected_count = Application.objects.filter(status="SELECTED").count()
    rejected_count = Application.objects.filter(status="REJECTED").count()
    shortlisted_count = Application.objects.filter(status="SHORTLISTED").count()

    placement_rate = (
        round(selected_count / total_applications * 100, 1) if total_applications else 0
    )

    # Job-wise stats
    job_stats = (
        Job.objects.annotate(
            apps=Count("application"),
            selected=Count("application", filter=Q(application__status="SELECTED")),
        )
        .values("title", "company_name", "ctc", "apps", "selected")
        .order_by("-selected")
    )

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4, topMargin=0.8 * inch, bottomMargin=0.8 * inch
    )
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph("CAMPUSCONNECT PLACEMENT REPORT", styles["Title"]))
    story.append(
        Paragraph(
            f"Generated: {timezone.now().strftime('%d %B %Y, %I:%M %p')}",
            styles["Normal"],
        )
    )
    story.append(Spacer(1, 20))

    # Summary
    data = [
        ["Metric", "Value"],
        ["Total Jobs", str(total_jobs)],
        ["Total Applications", str(total_applications)],
        ["Total Students", str(total_students)],
        ["Shortlisted", str(shortlisted_count)],
        ["Selected", str(selected_count)],
        ["Rejected", str(rejected_count)],
        ["Placement Rate", f"{placement_rate}%"],
    ]
    table = Table(data, colWidths=[3.5 * inch, 1.5 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 1, colors.grey),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 30))

    # Bar Chart
    chart_jobs = Job.objects.annotate(apps=Count("application")).values(
        "title", "apps"
    )[:10]
    if chart_jobs:
        labels = [
            (j["title"][:20] + "...") if len(j["title"]) > 20 else j["title"]
            for j in chart_jobs
        ]
        values = [j["apps"] for j in chart_jobs]

        plt.figure(figsize=(10, 6))
        bars = plt.bar(labels, values, color="#3498db")
        plt.title("Top 10 Jobs by Applications")
        plt.xlabel("Job")
        plt.ylabel("Applications")
        plt.xticks(rotation=45, ha="right")
        for bar in bars:
            h = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2, h + 0.3, str(int(h)), ha="center"
            )
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=150)
        buf.seek(0)
        story.append(Paragraph("Applications per Job", styles["Heading2"]))
        story.append(Image(buf, width=6.5 * inch, height=4 * inch))
        plt.close()

    # Job Table
    story.append(Paragraph("Job-wise Summary", styles["Heading2"]))
    table_data = [["Title", "Company", "CTC", "Applicatio", "Selected"]]
    for j in job_stats:
        table_data.append(
            [
                j["title"],
                j.get("company_name") or "N/A",
                f"₹{j['ctc'] or 0}",
                str(j["apps"]),
                str(j["selected"]),
            ]
        )
    if len(table_data) > 1:
        t = Table(
            table_data,
            colWidths=[2.2 * inch, 1.4 * inch, 0.9 * inch, 0.9 * inch, 0.9 * inch],
        )
        t.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ]
            )
        )
        story.append(t)

    doc.build(story)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="placement_report.pdf"'
    return response


@login_required
def view_resume(request, app_id):
    if not getattr(request.user, "is_placement_officer", False):
        messages.error(request, "Access denied.")
        return redirect("home")

    app = get_object_or_404(Application, id=app_id)
    resume_path = app.student.resume.path

    if not os.path.exists(resume_path):
        messages.error(request, "Resume not found.")
        return redirect("placement_officer:dashboard")

    with open(resume_path, "rb") as f:
        response = HttpResponse(f.read(), content_type="application/pdf")
        response["Content-Disposition"] = (
            f'inline; filename="{app.student.roll_number}_resume.pdf"'
        )
        return response
