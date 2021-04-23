from django import forms
from .models import Internship, InternshipApplication


class InternshipForm(forms.ModelForm):
    class Meta:
        model = Internship
        fields = [
            'company_name',
            'company_logo',
            'start_by',
            'duration',
            'about',
            'location',
            'stipend',
            'no_of_internships',
            'apply_by',
            'meet_link',
        ]


class ApplicationForm(forms.ModelForm):
    domain = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    class Meta:
        model = InternshipApplication
        fields = [
            'domain',
            'resume',
        ]
