from django.db import models
from authentication.models import User
from student.models import Student
from job.models import Job


class OfficerDashboard(models.Model):
    officer = models.OneToOneField(User, on_delete=models.CASCADE)
    total_jobs_posted = models.IntegerField(default=0)
    total_applications = models.IntegerField(default=0)
    total_selections = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.officer.name}'s Dashboard"
