from django.db import models
from accounts.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    roll_number = models.CharField(max_length=20, unique=True)
    cgpa = models.FloatField()
    branch = models.CharField(max_length=50)
    resume_url = models.FileField(upload_to="resumes/", blank=True)
    skills = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
