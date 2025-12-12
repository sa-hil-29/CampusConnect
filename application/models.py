# application/models.py
from django.db import models
from student.models import Student
from job.models import Job
from datetime import date


class Application(models.Model):
    STATUS_CHOICES = [
        ("APPLIED", "Applied"),
        ("SHORTLISTED", "Shortlisted"),
        ("SELECTED", "Selected"),
        ("REJECTED", "Rejected"),
    ]
    FINAL_STATUSES = ["SELECTED", "REJECTED", "SHORTLISTED"]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="APPLIED")
    application_date = models.DateField(default=date.today)
    last_updated = models.DateTimeField(auto_now=True)
    email_sent = models.BooleanField(default=False)

    class Meta:
        unique_together = ("student", "job")
        db_table = "applications"

    def __str__(self):
        return f"{self.student} → {self.job}"

    def is_final(self):
        return self.status in self.FINAL_STATUSES

    def can_update_status(self, new_status):
        if self.is_final():
            return False
        if new_status in self.FINAL_STATUSES:
            return True
        return True
