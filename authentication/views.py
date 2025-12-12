# authentication/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import SignUpForm
from student.models import Student


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # ROLE-BASED REDIRECT
            if user.role == "student":
                return redirect("student:profile")
            elif user.role == "admin":
                return redirect("placement_officer:dashboard")  # OFFICER DASHBOARD
            else:
                return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "authentication/register.html", {"form": form})
