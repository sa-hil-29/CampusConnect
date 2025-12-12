# student/models.py
from django.db import models
from authentication.models import User
from django.core.validators import FileExtensionValidator
from job.models import Branch


class Student(models.Model):
    BRANCH_CHOICES = [("CSE", "CSE"), ("ECE", "ECE"), ("ME", "ME"), ("CE", "CE")]
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="student_profile"
    )
    roll_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, null=True, blank=True)
    resume = models.FileField(
        upload_to="resumes/",
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        blank=True,
        null=True,
        help_text="Upload PDF only. Max 2MB.",
    )
    skills = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.name or self.user.email} - {self.roll_number or 'No Roll'}"

    class Meta:
        db_table = "students"
