from django import forms
from .models import Internship, InternshipApplication, Domains


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
    # domain = forms.ModelMultipleChoiceField(
    #     required=False,
    #     widget=forms.CheckboxSelectMultiple,
    #     queryset=Domains.objects.all(),
    # )
    class Meta:
        model = InternshipApplication
        fields = [
            'domain',
            'resume',
        ]
