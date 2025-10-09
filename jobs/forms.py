from django.utils import timezone
from django import forms
from .models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "title",
            "description",
            "company_name",
            "eligibility_criteria",
            "deadline",
            "status",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Job Title"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Job Description",
                }
            ),
            "company_name": forms.TextInput(attrs={"class": "form-control"}),
            "eligibility_criteria": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "e.g., CGPA > 7.0, Branch: CS",
                }
            ),
            "deadline": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "status": forms.Select(attrs={"class": "form-control"}),
        }

    def clean_deadline(self):
        deadline = self.cleaned_data["deadline"]
        if deadline < timezone.now().date():
            raise forms.ValidationError("Deadline must be in the future.")
        return deadline
