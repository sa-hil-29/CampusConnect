from django import forms
from job.models import Job, Branch


class JobForm(forms.ModelForm):
    eligible_branches = forms.ModelMultipleChoiceField(
        queryset=Branch.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        help_text="Select eligible branches for this job.",
    )

    class Meta:
        model = Job
        fields = [
            "title",
            "company_name",
            "description",
            "ctc",
            "min_cgpa",
            "eligible_branches",
            "deadline",
        ]
        widgets = {
            "deadline": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 4}),
            "ctc": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "min_cgpa": forms.NumberInput(
                attrs={"step": "0.01", "min": "0", "max": "10"}
            ),
        }
        labels = {
            "title": "Job Title",
            "company_name": "Company Name",
            "description": "Job Description",
            "ctc": "CTC (in LPA)",
            "min_cgpa": "Minimum CGPA Required",
            "deadline": "Application Deadline",
        }
