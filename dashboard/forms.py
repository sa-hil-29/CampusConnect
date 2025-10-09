# No dedicated forms for dashboard (uses queries and HTML tables for display).
# Placeholder for future extensions, e.g., a search form.

from django import forms


class DashboardSearchForm(forms.Form):
    search_term = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Search applications by student or job",
            }
        ),
    )
    branch_filter = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Filter by branch"}
        ),
    )
