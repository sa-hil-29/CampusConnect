from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(
        choices=[
            ("student", "Student"),
            ("admin", "Placement Officer"),
            ("company", "Company"),
        ],
        required=True,
    )

    class Meta:
        model = User
        fields = ("email", "name", "role", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.name = self.cleaned_data["name"]
        user.role = self.cleaned_data["role"]
        if commit:
            user.save()
        return user
