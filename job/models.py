# job/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date

User = get_user_model()
BRANCH_CHOICES = [
    ("CSE", "Computer Science"),
    ("IT", "Information Technology"),
    ("ECE", "Electronics & Communication"),
    ("EEE", "Electrical & Electronics"),
    ("MECH", "Mechanical"),
    ("CIVIL", "Civil"),
    ("CHEM", "Chemical"),
]


class Branch(models.Model):
    code = models.CharField(max_length=10, choices=BRANCH_CHOICES, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.get_code_display()

    class Meta:
        db_table = "branches"


class Job(models.Model):
    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("CLOSED", "Closed"),
        ("FILLED", "Filled"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    company_name = models.CharField(max_length=200)

    ctc = models.DecimalField(
        default=0.00, max_digits=10, decimal_places=2, help_text="CTC in LPA"
    )
    min_cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Minimum CGPA required",
    )
    eligible_branches = models.ManyToManyField(
        Branch, related_name="eligible_jobs", blank=True
    )

    deadline = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="OPEN")
    posted_by = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={"role": "admin"}
    )

    def __str__(self):
        return f"{self.title} - {self.company_name}"

    def validate_eligibility(self, student_cgpa, student_branch_code):
        cgpa_ok = student_cgpa >= self.min_cgpa
        branch_ok = (
            self.eligible_branches.all().filter(code=student_branch_code).exists()
        )
        return cgpa_ok and branch_ok

    @property
    def is_expired(self):
        return timezone.now().date() > self.deadline

    def save(self, *args, **kwargs):
        # Auto-close if deadline passed
        if self.is_expired and self.status == "OPEN":
            self.status = "CLOSED"
        super().save(*args, **kwargs)

    class Meta:
        db_table = "jobs"
