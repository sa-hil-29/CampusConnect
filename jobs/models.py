from django.db import models


class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    company_name = models.CharField(max_length=100)
    eligibility_criteria = models.TextField(
        blank=True
    )  # e.g., "CGPA > 7.0, Branch: CS"
    deadline = models.DateField()
    status = models.CharField(max_length=20, default="open")

    def __str__(self):
        return self.title
