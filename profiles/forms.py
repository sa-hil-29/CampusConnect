from django import forms
from .models import Student


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["roll_number", "cgpa", "branch", "resume_url", "skills"]
        widgets = {
            "roll_number": forms.TextInput(attrs={"class": "form-control"}),
            "cgpa": forms.NumberInput(
                attrs={"class": "form-control", "min": 0, "max": 10, "step": 0.01}
            ),
            "branch": forms.TextInput(attrs={"class": "form-control"}),
            "resume_url": forms.FileInput(
                attrs={"class": "form-control", "accept": ".pdf"}
            ),
            "skills": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "e.g., Python, Django",
                }
            ),
        }

    def clean_cgpa(self):
        cgpa = self.cleaned_data["cgpa"]
        if cgpa < 0 or cgpa > 10:
            raise forms.ValidationError("CGPA must be between 0 and 10.")
        return cgpa
