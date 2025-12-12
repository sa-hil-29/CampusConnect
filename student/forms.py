from django import forms
from .models import Student
from job.models import Branch


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["roll_number", "cgpa", "branch", "resume", "skills"]
        widgets = {
            "skills": forms.Textarea(attrs={"rows": 3}),
            "resume": forms.FileInput(attrs={"accept": ".pdf"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["branch"].empty_label = "Select your branch"
        self.fields["branch"].queryset = Branch.objects.all()

    def clean_resume(self):
        resume = self.cleaned_data.get("resume")
        if resume:
            if resume.size > 2 * 1024 * 1024:  # 2 MB
                raise forms.ValidationError("Resume must be < 2 MB")
            if not resume.name.lower().endswith(".pdf"):
                raise forms.ValidationError("Only PDF files are allowed")
        return resume
