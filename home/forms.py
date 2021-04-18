from django import forms
from .models import Internship, InternshipApplication


class InternshipForm(forms.ModelForm):
    class Meta:
        model = Internship
        fields = [
            'field_of_internship',
            'duration',
            'about',
            'location',
            'stipend',
            'skills_required',
            'no_of_internships',
            'perks',
            'who_should_apply',
            'apply_by',
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
        ]
