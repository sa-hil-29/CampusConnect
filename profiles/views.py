from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentProfileForm
from .models import Student


@login_required
def profile_update(request):
    if request.user.role != "student":
        messages.error(request, "Access denied. Students only.")
        return redirect("dashboard")

    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        student = Student(user=request.user)

    if request.method == "POST":
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("job_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = StudentProfileForm(instance=student)

    return render(request, "profiles/update.html", {"form": form})
