from django.db import models
from profiles.models import Student
from jobs.models import Job


class Application(models.Model):
    STATUS_CHOICES = (
        ("applied", "Applied"),
        ("shortlisted", "Shortlisted"),
        ("selected", "Selected"),
        ("rejected", "Rejected"),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="applied")
    application_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.job.title}"
